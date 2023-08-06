"""
    DataMaster
    - Handles reading and writing data from/to Bodega
        DataReader:
            obj_r = DataReader('select * from staging.sasha_hf_zip_maps limit 10;')
            df = obj_r.get_result_of_sql_as_df()
            print(df)
        DataWriter:
            obj = DataWriter(data_df=df,
                             fq_table_name='staging.sasha_delete_this',
                             primary_key_list=['dest_zip_code, hellofresh_week'],
                             update_flag=True)
            obj.run_load_to_db()

    DataReader only runs "select" statements from tables us_oa_etl user has
    access to.
    DataWriter is meant to write/update data to tables us_oa_etl user has
    access to. The flow is as follows:
        1. Add/replace timestamp columns
        2. Create intermediary table with the same name as
           the fq_table_name in intermediate_tables schema.
        3. Load data to intermediary table in text only format with no constraints.
        4. Check if production table has primary key. No by default if table
           does not exist.
        5. Create prod table:
           1a. If update_flag=True delete from prod table first based on primary key constraint.
           2a. Create prod table if not exist
           3a. Insert into prod table from stage table
           4a. Create trigger
           5a. Grant privileges
"""
import sys
import io
import pandas as pd
import logging
from hellofresh_data import logging_setup
from datetime import datetime
from hellofresh_data import bodega_connect
from hellofresh_data.parameter_store import get_parameter_store_value
from psycopg2.errors import InvalidTextRepresentation, BadCopyFileFormat
from psycopg2.extras import RealDictCursor

BODEGA_USER = '/Prod/BodegaDB/etl_user'
BODEGA_PASSWORD = '/Prod/BodegaDB/etl_user_password'
DEFAULT_TRIGGER_NAME = 'oa_etl_trigger_set_timestamp'
SOURCE_SCHEMA = 'intermediate_tables'


class DataReader():

    def __init__(self, sql=None):

        self.sql = sql
        self._logger = logging_setup.init_logging('DataReader')

        self.instantiate_bodega_creds()
        self.get_connection()
        self.validate_sql()

    def __del__(self):
        try:
            self.bodega_conn.close()
        except AttributeError:
            self.bodega_conn = None

    def instantiate_bodega_creds(self):
        """
            Retrieve bodega credentials for DDL
        """
        self.bodega_user_path = BODEGA_USER
        self.bodega_password_path = BODEGA_PASSWORD

        self.db_user = get_parameter_store_value(self.bodega_user_path)
        self.db_password = get_parameter_store_value(self.bodega_password_path)

    def get_connection(self):
        """
            Connecting to Bodega
        """

        try:
            conn_obj = bodega_connect.BodegaConnect(self.db_user,
                                                    self.db_password)
            self.bodega_conn = conn_obj.bodega_connect()
        except Exception as err:
            self._logger.error('Failed to connect to DB')
            self._logger.error(err)

    def validate_sql(self):
        """
            Run basic checks on SQL.
            Assert:
                1. Only SELECT and only 1 statement per query
                2. Only one statement per query, meaning no
                    query delimiters present.

            This is more of a foolproof check vs. checking for an
            actual malicious behaviour. This "ensures" we only use this
            class for reading data.
        """
        sql_parts = self.sql.strip().split(' ')
        delimiter_count = self.sql.strip().count(';')

        if sql_parts[0].lower() != 'select':
            self._logger.error('Can only run "select" commands')
            sys.exit(1)

        try:
            delimiter_count = int(delimiter_count)
        except Exception:
            delimiter_count = 0
            pass

        if int(delimiter_count) > 1:
            self._logger.error('Can only execute 1 sql command')
            sys.exit(1)

    def execute_sql(self, sql):
        """
            Execute passed in SQL statement. Rollback on error. Return data if
            available.
        """
        try:
            cur = self.bodega_conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("{sql}".format(sql=sql))
            self.bodega_conn.commit()
        except (InvalidTextRepresentation, BadCopyFileFormat):
            self.bodega_conn.rollback()
        except Exception as err:
            self.bodega_conn.rollback()
            self._logger.warning(err)

        try:
            data = cur.fetchall()
        except Exception:
            data = None
            pass

        return data, cur

    def get_result_of_sql_as_list(self):
        """
            Return SQL result as a list
        """
        data, cur = self.execute_sql(self.sql)
        try:
            col_names = [desc[0] for desc in cur.description]
        except Exception as err:
            self._logger.error(err)
            sys.exit(1)

        return data, col_names

    def get_result_of_sql_as_df(self):
        """
            Return SQL as a Data Frame
        """

        data, col_names = self.get_result_of_sql_as_list()
        df = pd.DataFrame(data, columns=col_names)

        return df


class DataWriter(DataReader):

    def __init__(self,
                 data_df,
                 fq_table_name,
                 primary_key_list=None,
                 update_flag=False,
                 logging_flag=False):

        self.data_df = data_df
        self.fq_table_name = fq_table_name
        self.primary_key_list = primary_key_list
        self.update_flag = update_flag
        self.logging_flag = logging_flag

        logging.basicConfig()
        self._logger = logging

        super().instantiate_bodega_creds()
        super().get_connection()
        self.instantiate_bodega_variables()


    def __del__(self):
        try:
            self.bodega_conn.close()
        except AttributeError:
            self.bodega_conn = None

    def instantiate_bodega_variables(self):
        """
            Initialize DB varibales from config file
        """

        self.table_name = self.fq_table_name.split('.')[1]
        self.schema_name = self.fq_table_name.split('.')[0]

        self.default_trigger_name = DEFAULT_TRIGGER_NAME

        self.source_schema = SOURCE_SCHEMA
        self.stage_fq_table_name = '{}.{}'.format(self.source_schema,
                                                  self.table_name)

        try:
            if self.source_schema in self.schema_name:
                self._logger.error('Cannot use %s schema for prod',
                                   self.source_schema)
                sys.exit(1)
        except IndexError:
            self._logger.error('Make sure you pass in schema.table format')
            self._logger.error('You passed: %s', self.fq_table_name)
            sys.exit(1)

        if self.primary_key_list:
            self.primary_key_list = ', '.join(self.primary_key_list)

    def get_ddl_column_ls(self):
        """
            Create DDL columns
            prod:
                column        text,
                column_number int,
                time_modified timestamp
            stage:
                column         text,
                column_number  text,
                time_modified  text
             stage_to_prod_cast:
                 column::text,
                 column_number::int,
                 time_modified::timestamp
        """
        prod_ddl = []
        stage_ddl = []
        stage_to_prod_cast = []

        df_types = self.data_df.infer_objects().dtypes
        df_column_names = list(self.data_df.columns)

        for i in range(len(df_types)):
            if str(df_types[i]) == 'object':
                data_type = 'text'
            if str(df_types[i]) == 'int64':
                data_type = 'int'
            if str(df_types[i]) == 'float64':
                data_type = 'numeric'
            if str(df_types[i]) == 'bool':
                data_type = 'boolean'
            if str(df_types[i]) == 'datetime64' \
                    or str(df_types[i]) == 'datetime64[ns]':
                data_type = 'timestamp'
            if any(word in df_column_names[i].lower() for
                   word in ['_date', 'date_', ' date']):
                data_type = 'date'

            if ' ' in df_column_names[i]:
                column_name = '"{}"'.format(df_column_names[i])
            else:
                column_name = df_column_names[i]

            prod_ddl.append('{} {}'.format(column_name, data_type))
            stage_ddl.append('{} text'.format(column_name))
            stage_to_prod_cast.append('{}::{}'.format(column_name,
                                                      data_type))

        self.prod_ddl_str = ', '.join(prod_ddl)
        self.stage_ddl_str = ', '.join(stage_ddl)
        self.stage_to_prod_cast_str = ', '.join(stage_to_prod_cast)

    def _get_ddl_for_staging_db(self):
        """
            Create a DDL statement to create a table
            based on DF column names.
        """
        if self.logging_flag is True:
            self._logger.info('Create DDL for staging DB')

        self.staging_ddl_sql = """
                           create table if not exists {fq_table_name}
                          ({stage_ddl_str});
                           """.format(stage_ddl_str=self.stage_ddl_str,
                                      fq_table_name=self.stage_fq_table_name)

    def _add_timestamp_columns(self):
        """
            Add created/updated at timestamps. Drop old ones if exits
        """
        try:
            self.data_df.drop('etl_created_at', 1, inplace=True)
        except Exception:
            pass
        try:
            self.data_df.drop('etl_updated_at', 1, inplace=True)
        except Exception:
            pass

        if self.logging_flag is True:
            self._logger.info('Adding DF timestamps')

        self.data_df['etl_created_at'] = \
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.data_df['etl_updated_at'] = \
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.data_df = self.data_df.astype({'etl_created_at': 'datetime64',
                                            'etl_updated_at': 'datetime64'})

    def _create_intermediary_db_table(self):
        """
            Create table from a predefined DDL statement
        """
        if self.logging_flag is True:
            self._logger.info('Creating table %s', self.stage_fq_table_name)
        super().execute_sql(self.staging_ddl_sql)

    def _get_inserted_count(self, fq_table_name):
        """
            Logs the count of records inserted into the staging table
        """

        sql = 'select count(*) as count from {};'

        try:
            record_count_raw = \
                super().execute_sql(sql.format(fq_table_name))[0][0]
            return record_count_raw['count']
        except Exception:
            return 0
            pass

    def _load_df_to_intermediary(self):
        """
            Loads data into the DB table via COPY command.
            Data is split into chunks and is stored in memory while
            being loaded. Stage table is truncated prior to each exucution.
        """
        if self.logging_flag is True:
            self._logger.info('Inserting data into %s', self.stage_fq_table_name)

        sio = io.StringIO()
        sio.write(self.data_df.to_csv(index=False,
                                      header=False,
                                      na_rep="[NULL]",
                                      chunksize=10000,
                                      mode='a'))
        sio.seek(0)

        if self.logging_flag is True:
            self._logger.info('Inserting %s into table %s',
                              len(self.data_df),
                              self.stage_fq_table_name)

        super().execute_sql("""truncate table {}
                            """.format(self.stage_fq_table_name))

        try:
            cur = self.bodega_conn.cursor()
            cur.copy_expert("""
                            COPY {}
                            FROM STDIN
                            WITH (FORMAT CSV, NULL "[NULL]")
                            """.format(self.stage_fq_table_name), sio)
            self.bodega_conn.commit()
        except (InvalidTextRepresentation, BadCopyFileFormat) as err:
            self.bodega_conn.rollback()
            self._logger.error(err)
            sys.exit(1)

        if self.logging_flag is True:
            self._logger.info('Inserted into bodega table: %s',
                              self.stage_fq_table_name)

    def _primary_key_check(self):
        """
            Run query from information_schema to check
            if a primary key exists. If it does not then
            add one.
        """

        primary_key = super().execute_sql("""
                select constraint_name
                  from information_schema.table_constraints
                 where table_name = '{table_name}'
                   and constraint_schema = '{schema_name}'
                   and constraint_type = 'PRIMARY KEY'
                   """.format(table_name=self.table_name,
                              schema_name=self.schema_name))
        try:
            primary_key[0][0]
            self.primary_key_flag = True
        except IndexError:
            self.primary_key_flag = False
            pass

    def _update_funcs_create_column_name_type_dict(self):
        """
            Update Functions:
                Create column name directory.
                i.e etl_created_at: timestamp
        """

        self.data_dict = {}

        for i, row in enumerate(self.stage_to_prod_cast_str.split(',')):
            key = row.split('::')[0].strip()
            value = row.split('::')[1].strip()
            self.data_dict[key] = value

    def _update_funcs_get_filter_clause_str(self):
        """
            Update Functions:
                Create where filter clause.
                 where inter.key = prod.key
                   and inter.key1 = prod.key1 --if primary_key_list > 1
        """

        filter_clause_list = []
        for key in self.primary_key_list.split(', '):
            filter_clause_list.append("""inter.{}::{} = prod.{}
                                        """.format(key, self.data_dict.get(key), key))

        self.filter_clause_str = ''
        for i, clause in enumerate(filter_clause_list):
            self.filter_clause_str+=("{} {}".format('where' if i == 0 else 'and', clause))

    def _update_create_ddl_template(self):
        """
            Update Functions:
                Template SQL for counting row impact prior to an update and also
                deleting rows for the purpose of running an update.
        """
        self.update_ddl_template = """
          {ddl_sql}
          from {fq_table_name} prod
         where exists (select *
                         from {stage_fq_table_name} inter
                              {filter_clause_list}
                       )
        """

    def _update_check_count_of_rows(self):
        """
            Update Functions:
                Run select to count rows that will be impacted by an
                update.
        """

        records_impact_count = self.update_ddl_template.format(
                ddl_sql='select count(*) as count',
                fq_table_name=self.fq_table_name,
                stage_fq_table_name=self.stage_fq_table_name,
                filter_clause_list=self.filter_clause_str)

        count_updated = super().execute_sql(records_impact_count)
        try:
            count_updated = count_updated[0][0]
            count = count_updated['count']
        except Exception:
            count = 0

        if self.logging_flag is True:
            self._logger.info('Update will impact {} rows'.format(count))

    def _update_create_delete_ddl(self):
        """
            Update Functions:
                Delete rows
        """

        delete_old_records_ddl = self.update_ddl_template.format(
                ddl_sql='delete',
                fq_table_name=self.fq_table_name,
                stage_fq_table_name=self.stage_fq_table_name,
                filter_clause_list=self.filter_clause_str)

        if self.logging_flag is True:
            self._logger.debug(delete_old_records_ddl)

        return delete_old_records_ddl

    def _create_prod_ddl(self):
        """
            Create full prod DDL
        """
        self.prod_ddl_ls = []

        prod_create_ddl_sql = """
             create table
             if not exists {fq_table_name}
                           ({prod_ddl_str});
           """.format(prod_ddl_str=self.prod_ddl_str,
                      fq_table_name=self.fq_table_name)

        if self.primary_key_flag:
            prod_create_primary_key_sql = None
        else:
            prod_create_primary_key_sql = """
                                    alter table {fq_table_name}
                                    add primary key ({constraint});
                                """.format(fq_table_name=self.fq_table_name,
                                           constraint=self.primary_key_list)

        prod_trigger_sql = """
              drop trigger if exists {trigger_name}
                on {fq_table_name};
            create trigger {trigger_name}
            before update
                on {fq_table_name}
               for each row execute procedure
                   {prod_schema}.{trigger_name}();;
                """.format(fq_table_name=self.fq_table_name,
                           trigger_name=self.default_trigger_name,
                           prod_schema=self.fq_table_name.split('.')[0])

        if self.update_flag:
            self._logger.info("""Running in update mode, will
                                 delete old records and insert new ones""")
            self._update_create_ddl_template()
            self._update_funcs_create_column_name_type_dict()
            self._update_funcs_get_filter_clause_str()
            self._update_check_count_of_rows()
            delete_old_records_if_update_sql = self._update_create_delete_ddl()
        else:
            delete_old_records_if_update_sql = None

        prod_insert_ddl_sql = """
            insert into {fq_table_name}
            select {stage_to_prod_cast_str}
              from {stage_fq_table_name}
                on conflict ({constraint})
                do nothing;
                """.format(fq_table_name=self.fq_table_name,
                           stage_to_prod_cast_str=self.stage_to_prod_cast_str,
                           stage_fq_table_name=self.stage_fq_table_name,
                           constraint=self.primary_key_list)

        prod_grant_ddl_sql = """
             grant all privileges on table {fq_table_name} to root;
             grant select on table {fq_table_name} to analyst;
             grant select on table {fq_table_name} to sashap;
                """.format(fq_table_name=self.fq_table_name)

        self.prod_ddl_ls.extend([prod_create_ddl_sql,
                                 prod_create_primary_key_sql,
                                 delete_old_records_if_update_sql,
                                 prod_insert_ddl_sql,
                                 prod_trigger_sql,
                                 prod_grant_ddl_sql])

    def load_df_to_prod(self):
        """
            Loads data into sunflower schema

            Run all of the DDL statements created from _create_prod_ddl.
            Get count prior and after execution to get the number of rows
            inserted.
        """

        old_count = self._get_inserted_count(self.fq_table_name)

        for sql in self.prod_ddl_ls:
            if sql:
                if self.logging_flag is True:
                    self._logger.debug(sql)
                    super().execute_sql(sql)
                else:
                    super().execute_sql(sql)

        new_count = self._get_inserted_count(self.fq_table_name)
        rows_inserted = new_count - old_count

        if self.logging_flag is True:
            self._logger.info('Inserted %s into Prod DB %s',
                              rows_inserted,
                              self.fq_table_name)

    def run_load_to_db(self):
        """
            Run all functions
        """
        self._add_timestamp_columns()
        self.get_ddl_column_ls()
        self._get_ddl_for_staging_db()
        self._create_intermediary_db_table()
        self._load_df_to_intermediary()
        self._primary_key_check()
        self._create_prod_ddl()
        self.load_df_to_prod()
