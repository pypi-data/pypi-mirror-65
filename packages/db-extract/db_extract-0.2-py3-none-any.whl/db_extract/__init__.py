import appdirs
import copy
import inspect
import itertools
import logging
import math
import networkx as nx
import os
import pyodbc
import pandas as pd
import re
import sqlite3
from collections import defaultdict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype

from . import constants as c
from . import utilities as u
from .models import DatasetMetadata, TableMetadata, ColumnMetadata, TableRelationship, Base

session = None


class DBSetup():
    def __init__(self, dataset_name, in_memory=False):
        '''
        This class is used to setup a dataset for later consumption by DBExtractor. Here, the user will identify
        where the source is, if they want to store a local copy in a SQLite database, set up foreign keys between
        tables, and assign custom names to columns.

        :param str dataset_name: user-defined identifier that will be used for all future modifications/extractions.
            Highly suggest using the same name as the folder (if the source is files), or the SQL database.
        '''

        global session

        self.dataset_name = dataset_name
        if session is None:
            start_session(in_memory=in_memory)

        self.dataset_metadata = session.query(DatasetMetadata).filter(
            DatasetMetadata.dataset_name == dataset_name
        ).first()

        if self.dataset_metadata is None:
            logging.info(f'{dataset_name} was not found in the metadata database, '
                         'you will need to run create_metadata()')
        else:
            logging.info(f'{dataset_name} was found in the metadata database, '
                         'only removal, customization, or linking is allowed.')

    def create_metadata(self, data_folder_path=None, data_file_extension='csv', delimiter=',', dump_to_data_db=False,
                        sql_server=None, sql_db=None, schema=None,  analyze_percentage=50, analyze_min_rows=1000,
                        analyze_max_rows=10000, ignore_table_substrings=[], min_records_to_add=0):
        '''
        Main function for setting up the dataset. Must be the first method run before anything else.
        Adds Dataset/Table/Column metadata to file specified by s.METADATA_DB.

        If the source will be from a group of files (or one file), provide the following:
        :param str data_folder_path: absolute path to the folder containing the files.
        :param str data_file_extension: identifier for files that contain actual data.
        :param str delimiter: how is a new column identified within a row (usually a comma or tab).
        :param bool dump_to_data_db: store data in a SQLite DB in the data_folder_path, specified by s.DATA_DB.

        If the source is MS SQL Server, provide the following:
        :param str sql_server: just the name, not the address
        :param str sql_db: just the name
        :param str schema
        :param analyze_percentage: determine series metadata using this percentage of the total rows
        :param analyze_min_rows: use at least this many rows in calculating series metadata
        :param analyze_max_rows: use no more than this many rows in calculating series metadata
        :param ignore_table_substrings: ignore tables that contain any of these substrings. FUTURE: allow regex.
        :param min_records_to_add: if a table does not have at least this many rows, then ignore it completely.
        '''

        if self.dataset_metadata is not None:
            raise Exception(f"Dataset {self.dataset_metadata.dataset_name} has already been initialized. "
                            "Please run remove_db() first on this instance if you want to start over.")

        duplicated_folder = session.query(DatasetMetadata).filter(
            DatasetMetadata.data_folder_path == data_folder_path
        ).first()

        if duplicated_folder is not None:
            raise Exception(f"Data folder path {data_folder_path} has already been put into the metadata db "
                            f"under dataset name {duplicated_folder.dataset_name}.")

        if data_folder_path is not None:
            if sql_server is not None or sql_db is not None or schema is not None:
                raise Exception("If providing data_folder_path (indicating that source is from files), "
                                "cannot provide parameters sql_server/sql_db/schema as this would indicate that the "
                                "source is from a SQL database.")
        else:
            if sql_server is None or sql_db is None or schema is None:
                raise Exception("If providing sql information, you must provide all parameters "
                                "sql_server, sql_db, and schema")

        if sql_server is not None and sql_db is None:
            raise Exception("If sql_server is provided, then sql_db must also be provided.")

        if sql_db is not None and sql_server is None:
            raise Exception("If sql_db is provided, then sql_server must also be provided.")

        if data_folder_path is not None:
            data_file_names = u.find_file_types(data_folder_path, data_file_extension)
            if dump_to_data_db:
                data_conn = sqlite3.connect(os.path.join(data_folder_path, f'{c.DEFAULT_DATADB_NAME}'))

            for data_file_name in data_file_names:
                logging.info(f'Loading {data_file_name}')
                idx = data_file_name.rfind('.')
                table_name = data_file_name[:idx]
                df = pd.read_csv(os.path.join(data_folder_path, data_file_name))
                self.add_table_metadata(table_name, num_records=len(df), num_analyzed=len(df),
                                        file=data_file_name, commit=False)
                if dump_to_data_db:
                    logging.info(f'Writing {table_name}')
                    db_location = f'{table_name}'
                    df.to_sql(db_location, con=data_conn, index=False)

                for column in df.columns:
                    x = calculate_series_metadata(df[column])
                    if x['num_non_null'] > 0:
                        self.add_column_metadata(table_name, column_source_name=column, column_custom_name=column,
                                                 is_many=x['is_many'], num_non_null=x['num_non_null'],
                                                 series_data_type=x['series_data_type'], commit=False)
                    else:
                        logging.warning(f'No non-null data found in {table_name}.{column}, ignoring')
        else:
            query = f"SELECT t.name FROM sys.tables t WHERE schema_name(t.schema_id) = '{schema}' "
            for ignore_substring in ignore_table_substrings:
                query += f"AND t.name NOT LIKE '%{ignore_substring}%' "
            query += "ORDER BY name"

            tables = execute_sql_query(query=query, sql_server=sql_server, sql_db=sql_db, disable_timeout=True)
            logging.info(f"{len(tables['name'])} tables found")

            # https://blogs.msdn.microsoft.com/martijnh/2010/07/15/sql-serverhow-to-quickly-retrieve-accurate-row-count-for-table/
            query = ("SELECT tbl.name, MAX(CAST(p.rows AS int)) AS rows FROM sys.tables AS tbl INNER JOIN "
                     "sys.indexes AS idx ON idx.object_id = tbl.object_id and idx.index_id < 2 INNER JOIN "
                     "sys.partitions AS p ON p.object_id=CAST(tbl.object_id AS int) AND p.index_id=idx.index_id ")
            if schema is not None:
                query += f"WHERE (SCHEMA_NAME(tbl.schema_id)='{schema}') "
            query += "GROUP BY tbl.name "

            num_rows_df = execute_sql_query(query=query, sql_server=sql_server, sql_db=sql_db, disable_timeout=True)

            for table_name in tables['name']:
                num_rows_in_db = int(num_rows_df[num_rows_df['name'] == table_name].iloc[0]['rows'])
                if num_rows_in_db == 0:
                    logging.warning(f'0 rows for {table_name}, will ignore it')
                    continue
                logging.info(f"Writing metadata for {table_name}")
                by_percentage = math.ceil(analyze_percentage / 100 * num_rows_in_db)
                if by_percentage < analyze_min_rows:
                    num_rows = analyze_min_rows
                elif by_percentage > analyze_max_rows:
                    num_rows = analyze_max_rows
                else:
                    num_rows = by_percentage
                query = f"SELECT TOP {num_rows} * FROM {table_name} "

                try:
                    df = execute_sql_query(query=query, sql_server=sql_server, sql_db=sql_db)
                    if len(df) == 0:
                        logging.warning(f'No data found in {table_name}, will ignore it.')
                        continue
                    if len(df) < min_records_to_add:
                        logging.warning(f'Only {len(df)} records in {table_name} which is below the set threshold '
                                        f'of {min_records_to_add}, will ignore it.')
                        continue
                    for column in df.columns:
                        x = calculate_series_metadata(df[column])
                        if x['num_non_null'] > 0:
                            self.add_column_metadata(table_name, column_source_name=column, column_custom_name=column,
                                                     is_many=x['is_many'], num_non_null=x['num_non_null'],
                                                     series_data_type=x['series_data_type'], commit=False)
                        else:
                            logging.warning(f'No non-null data found in {table_name}.{column}, ignoring')
                    self.add_table_metadata(table_name, num_records=num_rows_in_db,
                                            num_analyzed=len(df), file=None, commit=False)
                    session.commit()
                except Exception as e:
                    logging.error(f'Unable to write table {table_name}.')
                    logging.error(e)
                    session.rollback()

        self.dataset_metadata = DatasetMetadata(
            dataset_name=self.dataset_name,
            data_folder_path=data_folder_path,
            sql_server=sql_server,
            sql_db=sql_db,
            schema=schema,
            stored_in_data_db=dump_to_data_db
        )
        session.add(self.dataset_metadata)
        session.commit()
        logging.info("Done writing metadata")

    def add_table_metadata(self, table_name, num_records, num_analyzed, file=None, commit=False):
        '''
        Add table metadata to the metadata db

        :param str table_name
        :param int num_records: total number of rows in the table.
        :param int num_analyzed: number of rows that were analyzed in the table.
        :param str file: if source is from a set of files, this is the name of the file itself (not an absolute path).
        :param bool commit: go ahead and finalize the metadata db after adding this row.
            Defaults to false because oftentimes this method will be run for multiple tables,
            and should be finalized after all have been added.
        '''
        table_metadata = TableMetadata(
            dataset_name=self.dataset_name,
            num_records=num_records,
            num_analyzed=num_analyzed,
            table_name=table_name,
            file=file
        )
        session.add(table_metadata)
        if commit:
            session.commit()

    def add_column_metadata(self, table_name, column_source_name, is_many, num_non_null,
                            series_data_type, column_custom_name=None, commit=False):
        '''
        Add column metadata to the metadata db

        :param str table_name
        :param str column_source_name: name of the column from the file or server
        :param bool is_many: column has non-unique values
        :param num_non_null: number of non-null records in the column
        :param series_data_type: one of DISCRETE, CONTINUOUS, BOOLEAN, or DATETIME
        :param column_custom_name: end-user defined name for the column
            :type column_custom_name: str or None (uses column_source_name)
        '''
        if column_custom_name is None:
            column_custom_name = column_source_name

        column_metadata = ColumnMetadata(
            dataset_name=self.dataset_name,
            table_name=table_name,
            column_source_name=column_source_name,
            column_custom_name=column_custom_name,
            num_non_null=num_non_null,
            is_many=is_many,
            data_type=series_data_type
        )
        session.add(column_metadata)
        if commit:
            session.commit()

    def remove_db(self):
        '''
        Purge metadata and delete data from local SQLite db (if user provided dump_to_data_db=True during
        create_db_metadata step)
        '''

        logging.warning(f'Will remove metadata for {self.dataset_name}. The source data will remain untouched.')
        try:
            os.remove(os.path.join(self.dataset_metadata.data_folder_path, c.DEFAULT_DATADB_NAME))
            logging.info(f'Deleted SQLite copy of dataset that was created by this module.')
        except FileNotFoundError:
            pass

        session.query(TableMetadata).filter(
            TableMetadata.dataset_name == self.dataset_name
        ).delete()

        session.query(ColumnMetadata).filter(
            ColumnMetadata.dataset_name == self.dataset_name
        ).delete()

        session.query(TableRelationship).filter(
            TableRelationship.dataset_name == self.dataset_name
        ).delete()

        session.query(DatasetMetadata).filter(
            DatasetMetadata.dataset_name == self.dataset_name
        ).delete()

        session.commit()

        self.dataset_metadata = None

        logging.info(f'Done removing metadata for {self.dataset_name}')

    def use_source_fks_to_link(self):
        '''
        If source is MS SQL SERVER, then use the already defined foreign keys to create links between tables
        '''

        # https://stackoverflow.com/questions/483193/how-can-i-list-all-foreign-keys-referencing-a-given-table-in-sql-server

        query = ("SELECT  obj.name AS FK_NAME, "
                 "sch.name AS [schema_name], "
                 "tab1.name AS [table], "
                 "col1.name AS [column], "
                 "tab2.name AS [referenced_table], "
                 "col2.name AS [referenced_column] "
                 "FROM sys.foreign_key_columns fkc "
                 "INNER JOIN sys.objects obj "
                 "ON obj.object_id = fkc.constraint_object_id "
                 "INNER JOIN sys.tables tab1 "
                 "ON tab1.object_id = fkc.parent_object_id "
                 "INNER JOIN sys.schemas sch "
                 "ON tab1.schema_id = sch.schema_id "
                 "INNER JOIN sys.columns col1 "
                 "ON col1.column_id = parent_column_id AND col1.object_id = tab1.object_id "
                 "INNER JOIN sys.tables tab2 "
                 "ON tab2.object_id = fkc.referenced_object_id "
                 "INNER JOIN sys.columns col2 "
                 "ON col2.column_id = referenced_column_id AND col2.object_id = tab2.object_id ")
        if self.dataset_metadata.schema is not None:
            query += f"WHERE sch.name='{self.dataset_metadata.schema}' "

        df_fks = execute_sql_query(query, self.dataset_metadata.sql_server, self.dataset_metadata.sql_db,
                                   disable_timeout=True)

        for idx, row in df_fks.iterrows():
            table_1 = row['table']
            table_2 = row['referenced_table']
            column_1 = row['column']
            column_2 = row['referenced_column']

            logging.info(f'Linking {table_1}.{column_1} --> {table_2}.{column_2}')

            self.add_fk(table_1, column_1, table_2, column_2, commit=False)
        session.commit()

    def get_common_column_names(self):
        '''
        Get a list of names that are found in more than one table.
        This may indicate that it is a column used to join tables.

        :return: list of common column names, ordered starting with those found in the fewest # of tables
        '''

        all_column_metadata = session.query(ColumnMetadata).filter(
            ColumnMetadata.dataset_name == self.dataset_name
        ).all()

        column_counts = defaultdict(int)
        for column_metadata in all_column_metadata:
            column_counts[column_metadata.column_source_name] += 1
        common_columns = [(k, v) for k, v in column_counts.items() if v > 1]
        common_columns = sorted(common_columns, key=lambda x: x[1])
        common_columns = [x[0] for x in common_columns]
        return common_columns

    def get_column_metadata(self, table, column):
        '''
        Get data from metadata db re: column from table

        :param str table
        :param str column - (source name)
        '''
        return session.query(ColumnMetadata).filter(
            ColumnMetadata.dataset_name == self.dataset_name,
            ColumnMetadata.table_name == table,
            ColumnMetadata.column_source_name == column
        ).first()

    def get_table_relationship(self, table_1, table_2, connectable_only=False):
        '''
        Get data from metadata db re: relationship between two tables

        :param str table_1
        :param str table_2
        :param bool connectable_only: if True, only return relationship if
            one of the tables is a parent to the other (many-to-one relationship)
            one of the tables is a sibling to the other (one-to-one relationship)
            DO not return a relationship if they are step-siblings (many-to-many relationship)
        '''
        x = session.query(TableRelationship).filter(
            TableRelationship.dataset_name == self.dataset_name,
            ((TableRelationship.reference_table == table_1) & (TableRelationship.other_table == table_2)) |
            ((TableRelationship.reference_table == table_2) & (TableRelationship.other_table == table_1))
        )

        if connectable_only:
            x = x.filter(
                (TableRelationship.reference_table_role == c.ROLE_CHILD) |
                (TableRelationship.reference_table_role == c.ROLE_PARENT) |
                (TableRelationship.reference_table_role == c.ROLE_SIBLING)
            )  # noqa: E712

        tr = x.first()
        return tr

    def add_global_fk(self, column):
        '''
        If column name is found in a table, use it to create links to all other tables that also have that column name.
        Calls add_fk() with column_1 == column_2 == column provided by user

        :param str column
        '''

        # Find all tables that have this column name, then run add_fk to all combos
        tables_found = [x[0] for x in session.query(ColumnMetadata.table_name).filter(
            ColumnMetadata.dataset_name == self.dataset_name,
            ColumnMetadata.column_source_name == column
        ).all()]

        logging.info(f'{column} found in {len(tables_found)} tables: {tables_found}')

        for table_combination in itertools.combinations(tables_found, 2):
            self.add_fk(table_combination[0], column, table_combination[1], column, commit=False)
        session.commit()

    def add_fk(self, table_1, column_1, table_2, column_2, commit=True):
        '''
        Create link between two tables on specified columns.
        Function will determine which table is parent/child/sibling/step-sibling

        :param str table_1
        :param str column_1
        :param str table_2
        :param str column_2
        '''

        column_1_metadata = self.get_column_metadata(table_1, column_1)
        column_2_metadata = self.get_column_metadata(table_2, column_2)

        if column_1_metadata is None:
            logging.error(f"Cannot find {table_1}.{column_1} metadata")
            return
        if column_2_metadata is None:
            logging.error(f"Cannot find {table_2}.{column_2} metadata")
            return

        if column_1_metadata.is_many:
            if column_2_metadata.is_many:
                self.add_step_sibling_link(step_sibling_1_table=table_1, step_sibling_1_column=column_1,
                                           step_sibling_2_table=table_2, step_sibling_2_column=column_2)
                if commit:
                    session.commit()
                return

        tr = self.get_table_relationship(table_1, table_2, connectable_only=True)
        if tr is not None:
            logging.warning(f'Relationship already exists between {table_1} and {table_2} '
                            f'on {tr.reference_key}->{tr.other_key}. Cannot assign additional foreign key '
                            f'{column_1}->{column_2} between these tables.')  # serves as a safety check.
        else:
            # if we are going to join these tables together,
            # then the joining columns should be distinct and not continuous
            if column_1_metadata.data_type != c.SERIES_TYPE_DISCRETE:
                column_1_metadata.data_type = c.SERIES_TYPE_DISCRETE
            if column_2_metadata.data_type != c.SERIES_TYPE_DISCRETE:
                column_2_metadata.data_type = c.SERIES_TYPE_DISCRETE

            if column_1_metadata.is_many and not column_2_metadata.is_many:
                self.add_parent_child_link(parent_table=table_1, parent_column=column_1, child_table=table_2,
                                           child_column=column_2, commit=False)

            elif not column_1_metadata.is_many:
                if column_2_metadata.is_many:
                    self.add_parent_child_link(parent_table=table_2, parent_column=column_2, child_table=table_1,
                                               child_column=column_1, commit=False)

                elif not column_2_metadata.is_many:
                    self.add_sibling_link(sibling_1_table=table_1, sibling_1_column=column_1, sibling_2_table=table_2,
                                          sibling_2_column=column_2, commit=False)
        if commit:
            session.commit()

    def add_parent_child_link(self, parent_table, parent_column, child_table, child_column, commit=False):
        '''
        Create a many-to-one relationship between tables using specified columns for joining.
        Parent table/column has the is_many attribute (non-unique values).
        Child table/column does not have the is_many attribute (only unique values).
        In joining these tables together, the parent table would be the left-most table.

        :param str parent_table
        :param str parent_column
        :param str child_table
        :param str child_column
        :param bool commit: if True, then finalize metadata db at the end of this function.
        '''

        parent_row = TableRelationship(
            dataset_name=self.dataset_name,
            reference_table=parent_table,
            other_table=child_table,
            reference_table_role=c.ROLE_PARENT,
            reference_key=parent_column,
            other_key=child_column
        )

        child_row = TableRelationship(
            dataset_name=self.dataset_name,
            reference_table=child_table,
            other_table=parent_table,
            reference_table_role=c.ROLE_CHILD,
            reference_key=child_column,
            other_key=parent_column
        )

        session.add(parent_row)
        session.add(child_row)
        if commit:
            session.commit()

    def add_sibling_link(self, sibling_1_table, sibling_1_column, sibling_2_table, sibling_2_column, commit=False):
        '''
        Create a one-to-one relationship between tables using specified columns for joining
        Both tables/columns do not have the is_many attribute (only unique values).
        In joining these tables together, either one could be the left-most table.

        :param str sibling_1_table
        :param str sibling_1_column
        :param str sibling_2_table
        :param str sibling_2_column
        :param bool commit: if True, then finalize metadata db at the end of this function.
        '''
        sibling_1_row = TableRelationship(
            dataset_name=self.dataset_name,
            reference_table=sibling_1_table,
            other_table=sibling_2_table,
            reference_table_role=c.ROLE_SIBLING,
            reference_key=sibling_1_column,
            other_key=sibling_2_column,
        )
        sibling_2_row = TableRelationship(
            dataset_name=self.dataset_name,
            reference_table=sibling_2_table,
            other_table=sibling_1_table,
            reference_table_role=c.ROLE_SIBLING,
            reference_key=sibling_2_column,
            other_key=sibling_1_column,
        )

        session.add(sibling_1_row)
        session.add(sibling_2_row)
        if commit:
            session.commit()

    def add_step_sibling_link(self, step_sibling_1_table, step_sibling_1_column, step_sibling_2_table,
                              step_sibling_2_column, commit=False):
        '''
        Create a many-to-many relationship between tables using specified columns.
        Both tables/columns have the is_many attribute (non-unique values).
        For now, there is no support for joining these two directly to each other.

        :param str step_sibling_1_table
        :param str step_sibling_1_column
        :param str step_sibling_2_table
        :param str step_sibling_2_column
        :param bool commit: if True, then finalize metadata db at the end of this function.
        '''
        step_sibling_1_row = TableRelationship(
            dataset_name=self.dataset_name,
            reference_table=step_sibling_1_table,
            other_table=step_sibling_2_table,
            reference_table_role=c.ROLE_STEP_SIBLING,
            reference_key=step_sibling_1_column,
            other_key=step_sibling_2_column,
        )
        step_sibling_2_row = TableRelationship(
            dataset_name=self.dataset_name,
            reference_table=step_sibling_2_table,
            other_table=step_sibling_1_table,
            reference_table_role=c.ROLE_STEP_SIBLING,
            reference_key=step_sibling_2_column,
            other_key=step_sibling_1_column,
        )

        session.add(step_sibling_1_row)
        session.add(step_sibling_2_row)

        if commit:
            session.commit()

    def remove_all_relationships(self):
        '''
        Purge all links between tables for this dataset
        '''
        logging.warning(f'Will remove all links for dataset {self.dataset_name}')
        session.query(TableRelationship).filter(
            TableRelationship.dataset_name == self.dataset_name
        ).delete()
        session.commit()

    def rename_column(self, reference_table, original_name, new_name):
        '''
        Add a custom name to the column. Apply this to columns in other tables when this column is used
        to join to other tables.

        :param str reference_table
        :param str original_name: used to lookup in the db, equivalent to the source name
        :param str new_name
        '''
        found_row = self.get_column_metadata(reference_table, original_name)
        try:
            found_row.column_custom_name = new_name
        except AttributeError:
            e = f'Cannot find {reference_table}->{original_name}'
            logging.error(e)
            raise AttributeError(e)

        # Then look for where this column serves as a relationship to other tables
        found_related_table_rows = session.query(TableRelationship).filter(
            TableRelationship.dataset_name == self.dataset_name,
            TableRelationship.reference_table == reference_table,
            TableRelationship.reference_key == original_name
        ).all()

        for related_table_row in found_related_table_rows:
            related_table = related_table_row.other_table
            related_column = related_table_row.other_key
            found_related_row = session.query(ColumnMetadata).filter(
                ColumnMetadata.dataset_name == self.dataset_name,
                ColumnMetadata.table_name == related_table,
                ColumnMetadata.column_source_name == related_column
            ).first()
            try:
                found_related_row.column_custom_name = new_name
            except AttributeError:
                e = f'Cannot find {related_table}->{related_column}'
                logging.error(e)
                raise AttributeError(e)

        session.commit()

    def change_column_visibility(self, table, column, visible):
        '''
        Change column visibility. Apply this to columns in other tables when this column is used
        to join to other tables

        :param str table
        :param str column
        :param bool visible
        '''

        found_row = self.get_column_metadata(table, column)
        try:
            found_row.visible = visible
        except AttributeError:
            e = f'Cannot find {table}->{column}'
            logging.error(e)
            raise AttributeError(e)

        # Then look for where this column serves as a relationship to other tables
        found_related_table_rows = session.query(TableRelationship).filter(
            TableRelationship.dataset_name == self.dataset_name,
            TableRelationship.reference_table == table,
            TableRelationship.reference_key == column
        ).all()

        for related_table_row in found_related_table_rows:
            related_table = related_table_row.other_table
            related_column = related_table_row.other_key
            found_related_row = session.query(ColumnMetadata).filter(
                ColumnMetadata.dataset_name == self.dataset_name,
                ColumnMetadata.table_name == related_table,
                ColumnMetadata.column_source_name == related_column
            ).first()

            try:
                found_related_row.visible = visible
            except AttributeError:
                e = f'Cannot find {related_table}->{related_column}'
                logging.error(e)
                raise AttributeError(e)

        session.commit()

    def get_custom_column_name(self, reference_table, original_name):
        '''
        Retrieve the end-user defined custom name

        :param str reference_table
        :param str original_name: equivalent to the source name
        '''

        try:
            found_row = self.get_column_metadata(reference_table, original_name)
            return found_row.column_custom_name
        except AttributeError:
            e = f'Cannot find {reference_table}->{original_name}'
            logging.error(e)
            raise AttributeError(e)

    def get_table_columns(self):
        '''
        Get all tables and columns for the dataset

        :return: dictionary with k = table_name, and v = list of dictionaries with column metadata
        '''
        column_metadatas = session.query(ColumnMetadata).filter(
            ColumnMetadata.dataset_name == self.dataset_name
        ).all()
        table_columns = defaultdict(list)
        for x in column_metadatas:
            table_columns[x.table_name].append({
                'column_id': x.id,
                'column_source_name': x.column_source_name,
                'column_custom_name': x.column_custom_name,
                'visible': x.visible
            })

        return table_columns


class DBExtractor():
    def __init__(self, dataset_name, in_memory=False):
        '''
        Used to perform data extraction and manipulation on provided dataset.
        Must have been setup already using DBSetup(dataset_name).
        Creates a directed graph using networkx, with rules as follows:

        Tables that are linked together in a parent-child == many-to-one relationship are: parent -> child.
        Tables that are linked together in a sibling == one-to-one relationship are:      sibling <-> sibling.

        :param str dataset_name

        :attr G: the directed graph generated by networkx
        :attr dataset_metadata: pulled from metadata db
        :attr storage_type: define whether to pull data from MS SQL Server, SQLite DB, or a set of files
        :attr data_conn: if data is stored in a SQLite DB, establish connection to it.
        '''
        # path-finding, get data out
        global session

        self.dataset_name = dataset_name
        if session is None:
            start_session(in_memory=in_memory)

        self.dataset_metadata = session.query(DatasetMetadata).filter(
            DatasetMetadata.dataset_name == self.dataset_name
        ).first()

        if self.dataset_metadata is None:
            raise Exception(f"Dataset {dataset_name} has not been initialized. You must call an instance of "
                            f"DBSetup('{dataset_name}'), then run create_metadata() on it, then add links as necessary")

        # three options
        # 1) Stored locally in a SQLite db created by this application. Highest priority
        # 2) Stored remotely in a SQL Server that the user has supplied (details in dataset metadata)
        # 3) Stored in files

        if not self.dataset_metadata.stored_in_data_db:
            if self.dataset_metadata.sql_server is None:
                if self.dataset_metadata.data_folder_path is None:
                    raise Exception('Cannot figure out where the data is actually stored for this dataset.')
                self.storage_type = c.STORAGE_TYPE_FILES
            else:
                self.storage_type = c.STORAGE_TYPE_MSSQL
        else:
            self.storage_type = c.STORAGE_TYPE_SQLITE
            self.data_conn = sqlite3.connect(os.path.join(self.dataset_metadata.data_folder_path,
                                                          f'{c.DEFAULT_DATADB_NAME}'), check_same_thread=False)

        self.G = nx.DiGraph()
        table_metadata = session.query(TableMetadata).filter(
            TableMetadata.dataset_name == self.dataset_name
        ).all()

        for x in table_metadata:
            self.G.add_node(x.table_name, num_records=x.num_records)

        trs = session.query(TableRelationship).filter(
            TableRelationship.dataset_name == self.dataset_name
        ).all()

        for tr in trs:
            if tr.reference_table_role == c.ROLE_PARENT:
                self.G.add_edge(tr.reference_table, tr.other_table)
            elif tr.reference_table_role == c.ROLE_CHILD:
                self.G.add_edge(tr.other_table, tr.reference_table)
            elif tr.reference_table_role == c.ROLE_SIBLING:
                self.G.add_edge(tr.reference_table, tr.other_table)
                self.G.add_edge(tr.other_table, tr.reference_table)

    def find_paths_multi_tables(self, list_of_tables, search_depth=5):
        '''
        Given a list of tables, find all paths that include every one of those tables.
        Algorithm uses the concept that if any table (even not in list_of_tables) has a path
        that goes to all of list_of_tables, then this is a valid path.

        :param list(str) list_of_tables
        :param int search_depth: cutoff for networkx, setting this too high can be very computationally expensive/long.

        :return: list of paths (each path is also a list) such as (for list_of_tables=[A, C])
        [
            [(A, B), (B, C)],
            [(A, D), (D, C)]
        ]
        This is equivalent to saying
        path 1 = start with A, join B to A, join C to B
        path 2 = start with A, join D to A, join C to D
        '''

        if len(list_of_tables) == 1:
            return [list_of_tables]

        all_tables = list(self.G.nodes)

        # if given list [A, B, C], and all tables are [O, A, B, C],
        # then valid paths are when A-->B AND A-->C, or B-->A AND B-->C, or C-->A AND C-->B,
        # or O-->A AND O-->B AND O-->C
        path_combos_to_check = []
        for table in all_tables:
            list_copy = copy.copy(list_of_tables)
            try:
                list_copy.remove(table)
            except ValueError:
                pass
            path_combos_to_check.append([(table, i) for i in list_copy])

        # now I have a list that's like [ [(A, B), (A, C)],  [(B, A), (B, C)],  [(C, A), (C, B)].

        valid_paths = []
        for path_combo in path_combos_to_check:  # [(A, B), (A, C)]
            partial_paths = []
            still_valid = True
            for path_to_check in path_combo:  # (A, B), then (B, C)
                simple_paths = self._paths_between_tables(path_to_check[0], path_to_check[1], search_depth=search_depth)
                if len(simple_paths) == 0:
                    still_valid = False
                    break
                partial_paths.append(simple_paths)
            if still_valid:
                # partial_paths is now a triple-nested list like:
                # [ [ [(A, D), (D, B)], [(A, E), (E, B)] ], [(A, F), (F, C)], [(A, G), (G, C)] ]
                # inner-most is a single path from A-->B
                # next level out is all single paths from A-->B
                # next level out is all single paths from A-->B, and A-->C
                for i in itertools.product(*partial_paths):  # take cartesian product of the second level
                    valid_paths.append([item for sublist in i for item in sublist])
        '''
        now within each valid path, there may be duplicate pairs so get rid of them
        # [
            [(A, B), (B, E), (A, B), (E, C)] --> [(A, B), (B, E), (E, C)]
            [(A, B), (B, C)] --> no change
        # ]
        '''
        valid_paths_dedup = []
        for path in valid_paths:
            current_path = []
            for pair in path:
                if pair not in current_path:
                    current_path.append(pair)
            valid_paths_dedup.append(current_path)

        valid_paths_no_redundants = sorted(valid_paths_dedup, key=lambda x: len(set([i for i in u.flatten(x)])))

        '''
        sort paths by fewest tables
        then for subsequent paths, if a valid path has been added to final list that has tables that are fully
        contained within this path, don't add this new path because it may reduce data
        [
            [(A, B), (B, C), (C, D)] --> tables are A, B, C, D. Add since it's the first one
            [(A, E), (E, B), (B, C), (C, D)] --> tables are A, B, C, D, E. This path contains ABCD which has already
            been accounted for, so discard this one

            [(A, B), (B, E), (E, D)] --> tables are A, B, D, E. This does NOT contains ABCD, so keep this one
        ]
        '''

        valid_paths_unique = []
        for check_path in valid_paths_no_redundants:
            is_valid = True
            this_path_traversed_tables = set()
            for pair in check_path:
                this_path_traversed_tables.add(pair[0])
                this_path_traversed_tables.add(pair[1])
            for verified_path in valid_paths_unique:
                if check_path != verified_path:
                    valid_path_traversed_tables = set()
                    for pair in verified_path:
                        valid_path_traversed_tables.add(pair[0])
                        valid_path_traversed_tables.add(pair[1])
                    if len(valid_path_traversed_tables - this_path_traversed_tables) == 0:
                        logging.debug(f'Path {check_path} is redundant to {verified_path}')
                        is_valid = False
                        break
            if is_valid:
                logging.debug(f'Adding path {check_path}')
                valid_paths_unique.append(check_path)

        return valid_paths_unique

    def _paths_between_tables(self, start_table, destination_table, search_depth=5):
        '''
        Get all simple paths that directly connect start_table and destination_table in self.G
        Used as helper function for find_paths_multi_tables

        :param str start_table
        :param str destination_table
        :param int search_depth: cutoff for networkx, setting this too high can be very computationally expensive/long.

        :return: list of paths
        '''

        all_paths = sorted(nx.all_simple_paths(self.G, start_table, destination_table,
                           cutoff=search_depth), key=lambda x: len(x))
        # reduce all_paths: Any simple path that contains all the tables in a prior simple path can be eliminated
        # because this path can only have the same amount or less of data than that prior path
        # (e.g. A-->C will always be at least as good as A-->B-->C)
        reduced_paths = []
        for check_path in all_paths:
            this_path_traversed_tables = set(check_path)
            is_valid = True
            for added_path in reduced_paths:
                added_path_traversed_tables = set(added_path)
                if len(added_path_traversed_tables - this_path_traversed_tables) == 0:
                    is_valid = False
                    break
            if is_valid:
                reduced_paths.append(check_path)

        pairwise_paths = [list(u.pairwise(x)) for x in reduced_paths]
        return pairwise_paths

    def find_still_joinable_tables(self, list_of_tables):
        '''
        Given a list_of_tables that must be in a valid path, determine which other tables in the dataset can be
        joined in as well.

        Algorithm: iterate through all tables (X) to figure out if there are paths between
        each table in list_of_tables and X.

        :param list(str) list_of_tables
        '''

        all_tables = self.G.nodes
        if len(list_of_tables) == 0:
            return sorted(list(all_tables), key=lambda x: x.upper())

        # First make sure that there is a path between these tables in the first place
        accessible_tables = set()

        valid_initial_paths = self.find_paths_multi_tables(list_of_tables)

        if len(valid_initial_paths) == 0:
            return []

        # any table in these valid paths is automatically accessible
        for path in valid_initial_paths:
            for pair in path:
                accessible_tables.add(pair[0])
                accessible_tables.add(pair[1])

        for check_if_accessible_table in all_tables:
            if check_if_accessible_table not in accessible_tables:
                for origin_table in all_tables:
                    is_valid = True
                    valid_paths = []
                    for check_path_to_table in list_of_tables + [check_if_accessible_table]:
                        # must have valid path to all of the tables in list_of_tables,
                        # and this check_if_accessible_table
                        try:
                            path = nx.shortest_path(self.G, origin_table, check_path_to_table)
                            valid_paths.append(path)
                        except nx.NetworkXNoPath:
                            is_valid = False
                            break
                    if is_valid:
                        for path in valid_paths:
                            for table in path:
                                accessible_tables.add(table)

        return sorted(list(accessible_tables), key=lambda x: x.upper())

    def get_table_df(self, table, select_columns=None, limit_rows=None, filters=[]):
        '''
        Get dataframe for single table

        :param str table
        :param list(str) select_columns: if provided, then choose only these columns
        :param limit_rows: select x rows
            :type limit_rows: int or None (no limit)
        :param list(Filter) filters: apply provided filters to the dataframe before returning it

        :return: pandas DataFrame
        '''

        if self.storage_type == c.STORAGE_TYPE_FILES:
            table_metadata = session.query(TableMetadata).filter(
                TableMetadata.dataset_name == self.dataset_name,
                TableMetadata.table_name == table
            ).first()

            df = pd.read_csv(os.path.join(self.dataset_metadata.data_folder_path, table_metadata.file))
            for filter in filters:
                if filter.filter_type == c.FILTER_TYPE_RANGE:
                    if filter.range_min is not None:
                        df = df[df[filter.column] >= filter.range_min]
                    if filter.range_max is not None:
                        df = df[df[filter.column] <= filter.range_max]
                elif filter.filter_type == c.FILTER_TYPE_SELECTION:
                    df = df[df[filter.column].isin(filter.selection)]

            if select_columns is not None:
                df = df[select_columns]
        else:
            sql_statement = "SELECT "
            if limit_rows is not None and self.storage_type == c.STORAGE_TYPE_MSSQL:
                sql_statement += f'TOP {limit_rows} '
            if select_columns is not None:
                sql_statement += ', '.join(select_columns) + ' '
            else:
                sql_statement += ' * '

            sql_statement += f"FROM {table} "
            sql_statement = self._add_filters_to_sql(sql_statement, table, filters, is_first_clause=True)

            if limit_rows is not None and self.storage_type == c.STORAGE_TYPE_SQLITE:
                sql_statement += f'LIMIT {limit_rows} '

            if self.storage_type == c.STORAGE_TYPE_SQLITE:
                df = pd.read_sql(sql_statement, con=self.data_conn)
            else:
                df = execute_sql_query(query=sql_statement, sql_server=self.dataset_metadata.sql_server,
                                       sql_db=self.dataset_metadata.sql_db, db_location=self.storage_type)

        return df

    def get_linked_tables_dfs(self, list_of_tables, filters={}, select_table_columns={}, limit_rows=None,
                              search_depth=5):
        '''
        Given a list of tables with filters, find all paths connecting all tables,
        and return all dataframes resulting from these paths

        :param list(str) list_of_tables
        :param dict{str k: list v} filters: pass-through to get_df_from_path
        :param dict{str k: list v} select_table_columns: pass-through to get_df_from_path
        :param int limit_rows: pass-through to get_df_from_path
        :param int search_depth: pass-through to find_paths_multi_tables
        '''

        # filters is a dict with k: v = table: [list of filters]
        # select_table_columns is a dict with k: v = table: [list of columns]
        if len(list_of_tables) == 1:
            select_columns = select_table_columns.get(list_of_tables[0], None)
            filters = filters.get(list_of_tables[0], [])
            df = self.get_df_table(list_of_tables[0], select_columns=select_columns,
                                   limit_rows=limit_rows, filters=filters)

            df.columns = [f'{list_of_tables[0]}_{x}' for x in df.columns]
            return [df]
        # need to add in capability if columns have different names,
        # using table relationships with reference_key, other_key
        dfs = []
        all_paths = self.find_paths_multi_tables(list_of_tables, search_depth=search_depth)
        logging.debug(f'All paths for {list_of_tables}: {all_paths}')
        for path in all_paths:
            dfs.append(self.get_df_from_path(path, select_table_columns=select_table_columns,
                       limit_rows=limit_rows, filters=filters))
        return [x for x in dfs if len(x) > 0]

    def get_df_from_path(self, path, filters={}, select_table_columns={}, limit_rows=None, disable_timeout=False):
        '''
        Given a path in form [(A, B), (B, C)], return dataframe resulting from these joins

        :param list(tuple) path
        :param dict{str k: list v} filters: apply list of filters,
            dictionary is k: v = table: [list of filters]
            e.g. {table_1: [Filter_1, Filter_2], table_2: [Filter_3]}

        :param dict{str k: list v} select_table_columns: only select tables and columns specified,
            dictionary is k: v = table: [list of columns]
            e.g. {table_1: [col_1, col_2], table_2: [col_3]}

        :param limit_rows: select x rows
            :type limit_rows: int or None (no limit)
        :param disable_timeout

        :return: dataframe resulting from joining these tables together
        '''
        all_tables = list(set(list(u.flatten(path))))
        if self.storage_type == c.STORAGE_TYPE_FILES:
            df_lookup_dict = {}
            for table in all_tables:
                table_df = self.get_table_df(table, limit_rows=limit_rows)
                table_df.columns = [f'{table}_{x}' for x in table_df.columns]
                df_lookup_dict[table] = table_df

            first_table = path[0][0]
            joined_tables = set()
            joined_tables.add(first_table)
            df = df_lookup_dict[first_table]

            for pair in path:
                if pair[1] not in joined_tables:
                    try:
                        left_key, right_key = self.get_joining_keys(pair[0], pair[1])
                    except TypeError as e:
                        logging.error(f'Path {path} is invalid. Unable to join {pair[0]} to {pair[1]}')
                        raise(TypeError(e))

                    df = df.merge(df_lookup_dict[pair[1]], left_on=f'{pair[0]}_{left_key}',
                                  right_on=f'{pair[1]}_{right_key}')

            for table, filter_list in filters.items():
                for filter in filter_list:
                    column_name = f'{table}_{filter.column}'
                    if filter.filter_type == c.FILTER_TYPE_RANGE:
                        if filter.range_min is not None:
                            df = df[df[column_name] >= filter.range_min]
                        if filter.range_max is not None:
                            df = df[df[column_name] <= filter.range_max]
                    elif filter.filter_type == c.FILTER_TYPE_SELECTION:
                        df = df[df[column_name].isin(filter.selection)]
            if len(select_table_columns) > 0:
                table_column_names = []
                for table, column_list in select_table_columns.items():
                    for column in column_list:
                        table_column_names.append(f'{table}_{column}')
                df = df[table_column_names]
        else:
            sql_statement = 'SELECT '
            if limit_rows is not None and self.storage_type == c.STORAGE_TYPE_MSSQL:
                sql_statement += f'TOP {limit_rows} '

            if len(select_table_columns) > 0:
                for table, column_list in select_table_columns.items():
                    for column in column_list:
                        sql_statement += f'{table}.{column} AS {table}_{column}, '
                sql_statement = sql_statement.strip(', ') + ' '
            else:
                column_metadata_list = session.query(
                    ColumnMetadata.table_name, ColumnMetadata.column_source_name
                ).filter(
                    ColumnMetadata.dataset_name == self.dataset_name,
                    ColumnMetadata.table_name.in_(all_tables)
                ).all()

                for x in column_metadata_list:
                    sql_statement += f'{x.table_name}.{x.column_source_name} AS {x.table_name}_{x.column_source_name}, '
                sql_statement = sql_statement.strip(', ') + ' '
            previous_table = path[0][0]
            sql_statement += f'FROM {previous_table} '
            joined_tables = set()
            joined_tables.add(previous_table)
            for pair in path:
                # the first part of the pair will always have already been included in the path,
                # and so can be safely ignored. Will not have a situation like [(A, B), (C, D)].
                # Must always be like [(A, B), (A, __)] or [(A, B), (B, __)]
                if pair[1] not in joined_tables:
                    try:
                        left_key, right_key = self.get_joining_keys(pair[0], pair[1])
                    except TypeError as e:
                        logging.error(f'Path {path} is invalid. Unable to join {pair[0]} to {pair[1]}')
                        raise(TypeError(e))
                    sql_statement += f'JOIN {pair[1]} ON {pair[0]}.{left_key} = {pair[1]}.{right_key} '

                    joined_tables.add(pair[1])

            first_filter_added = False
            for table, filters in filters.items():
                if first_filter_added:
                    sql_statement = self._add_filters_to_sql(sql_statement, table, filters, is_first_clause=False)
                else:
                    sql_statement = self._add_filters_to_sql(sql_statement, table, filters, is_first_clause=False)
                    first_filter_added = True

            if limit_rows is not None and self.storage_type == c.STORAGE_TYPE_SQLITE:
                sql_statement += f'LIMIT {limit_rows}'

            if self.storage_type == c.STORAGE_TYPE_SQLITE:
                df = pd.read_sql(sql_statement, con=self.data_conn)
            else:
                df = execute_sql_query(query=sql_statement, sql_server=self.dataset_metadata.sql_server,
                                       sql_db=self.dataset_metadata.sql_db, db_location=self.storage_type,
                                       disable_timeout=disable_timeout)

        return df

    def get_joining_keys(self, table_1, table_2):
        '''
        Get the TableRelationship linking the two tables.
        Order matters (table_1 should be the parent in a parent-child relationship, doesn't really matter if siblings)

        :param str table_1
        :param str table_2
        '''
        # order matters here
        return session.query(TableRelationship.reference_key, TableRelationship.other_key).filter(
            TableRelationship.dataset_name == self.dataset_metadata.dataset_name,
            TableRelationship.reference_table == table_1,
            TableRelationship.other_table == table_2,
            (
                (TableRelationship.reference_table_role == c.ROLE_PARENT) |
                (TableRelationship.reference_table_role == c.ROLE_SIBLING)
            )
        ).first()  # noqa: E712

    def aggregate_df(self, df_original, groupby_columns, numeric_as_discrete_columns=[], column_bins={},
                     aggregate_column=None, aggregate_fxn=c.AGGREGATE_FXN_COUNT):
        '''
        Given a dataframe, perform groupbys and aggregations

        :param pd.DataFrame df_original: dataframe to manipulate
        :param list(str) groupby_columns: choose which columns to groupby
        :param list(str) numeric_as_discrete_columns: if column is provided and has numeric data, treat it
        as discrete data instead. Useful if categorical data is identified with numbers.
        :param dict{str k: int v}: for numerical groupby_columns, divide it into this many bins.
        :param str aggregate_column: name of the column to aggregate on
        :param enum aggregate_fxn: function to apply. Refer to constants.py for AGGREGATE_FXN options

        :return: aggregated pandas dataframe
        '''
        df = df_original.copy(deep=True)
        df = df.dropna()

        keep_columns = [x for x in df.columns if x in groupby_columns or x == aggregate_column]
        df = df[keep_columns]

        for column in df.columns:
            if (is_numeric_dtype(df[column]) and column in groupby_columns and column != aggregate_column
                    and column not in numeric_as_discrete_columns):

                num_bins = column_bins.get(column, 1)
                bin_cuts = self._get_bin_cuts(df[column].min(), df[column].max(), num_bins)
                bin_labels = [str(x) for x in u.pairwise(bin_cuts)]
                bin_labels = [x.replace(')', ']') for x in bin_labels]
                df[column] = pd.cut(df[column], bin_cuts, include_lowest=True, labels=bin_labels).dropna()

        if len(df) > 0:
            if aggregate_column is None:
                # just get the counts then
                df = df.groupby(groupby_columns).size()
                if len(groupby_columns) > 1:
                    df = df.unstack(fill_value=0).sort_index(axis=1).stack()
                df = df.reset_index(name=c.AGGREGATE_FXN_COUNT)
            else:
                g = df.groupby(groupby_columns, observed=True)

                if aggregate_fxn == c.AGGREGATE_FXN_COUNT:
                    df = g[aggregate_column].value_counts().unstack(fill_value=0)

                elif aggregate_fxn == c.AGGREGATE_FXN_PERCENT:
                    df = (g[aggregate_column].value_counts(normalize=True) * 100).round(1).unstack(fill_value=0)

                elif aggregate_fxn == c.AGGREGATE_FXN_SUM:
                    df = (g[aggregate_column].sum()).round(2).unstack(fill_value=0).stack()
                    df = df.reset_index(name=c.AGGREGATE_FXN_SUM)

                elif aggregate_fxn == c.AGGREGATE_FXN_MEAN:
                    df = (g[aggregate_column].mean()).round(2).unstack(fill_value=0).stack()
                    df = df.reset_index(name=c.AGGREGATE_FXN_MEAN)

                elif aggregate_fxn == c.AGGREGATE_FXN_MEDIAN:
                    df = (g[aggregate_column].median()).round(2).unstack(fill_value=0).stack()
                    df = df.reset_index(name=c.AGGREGATE_FXN_MEDIAN)

                else:
                    raise Exception('Invalid aggregate function supplied. Please use a value from constants.py.')

        return df

    def _add_filters_to_sql(self, sql_statement, table, filters, is_first_clause):
        '''
        Helper function to build part of SQL query. Adds filters for a single table.
        Can be run multiple times to add more tables.

        :param str sql_statement: add clause to this.
        :param str table: the table to filter on
        :param list(Filter) filters: list of Filter objects for this table
        :param bool is_first_clause: indicate whether this is the first filter added to the SQL query
            (use WHERE instead of AND)

        '''
        for idx, filter in enumerate(filters):
            if idx == 0 and is_first_clause:
                sql_statement += "WHERE "
            else:
                sql_statement += "AND "

            if filter.filter_type == c.FILTER_TYPE_RANGE:
                if filter.range_min is not None and filter.range_max is not None:
                    sql_statement += (f"{table}.{filter.column} >= {filter.range_min} AND "
                                      f"{table}.{filter.column} <= {filter.range_max} ")
                elif filter.range_min is not None and filter.range_max is None:
                    sql_statement += f"{table}.{filter.column} >= {filter.range_min} "
                elif filter.range_min is None and filter.range_max is not None:
                    sql_statement += f"{table}.{filter.column} <= {filter.range_max} "
            elif filter.filter_type == c.FILTER_TYPE_SELECTION:
                str_repr = str(tuple(filter.selection)) if len(filter.selection) > 1 else f"('{filter.selection[0]}')"
                sql_statement += f"{table}.{filter.column} IN {str_repr} "

        return sql_statement

    def _get_bin_cuts(self, min, max, num_bins):
        '''
        Divide a range of numerical data into equidistant bins

        :param float min
        :param float max
        :param int num_bins

        :return: list(float) of dividing points
        '''
        min = float(min)
        max = float(max)
        step_size = (max - min) / num_bins
        current_cut = min
        bin_cuts = []
        while len(bin_cuts) < num_bins:
            current_cut = u.reduce_precision(current_cut, precision=2)
            bin_cuts.append(float(current_cut))
            current_cut += step_size
        bin_cuts.append(float(max))  # added in case there are rounding errors

        bin_cuts = sorted(list(set(bin_cuts)))
        if len(bin_cuts) == 1:
            bin_cuts = [bin_cuts[0], bin_cuts[0]]

        return bin_cuts


class Filter():
    def __init__(self, filter_type, column, range_min=None, range_max=None, selection=[]):
        '''
        User-defined filter for a table. A table can have multiple filters for a single column

        :param enum filter_type: refer to constants.py for FILTER_TYPE options
        :param str column: name of the column to apply filter to
        :param float range_min: for numeric data, choose data >= range_min
        :param float range_max: for numeric data, choose data <= range_max
        :param selection: for discrete data, choose data that is in this selection
        '''

        self.filter_type = filter_type
        self.column = column

        if filter_type == c.FILTER_TYPE_RANGE:
            if range_min is None and range_max is None:
                raise Exception(f'You must provide at least one of range_min and/or range_max if you choose '
                                f'filter_type={c.FILTER_TYPE_RANGE}')

            self.range_min = range_min
            self.range_max = range_max
        elif filter_type == c.FILTER_TYPE_SELECTION:
            if len(selection) == 0:
                raise Exception(f'You must provide at least one item in selection=[] if you choose '
                                f'filter_type={c.FILTER_TYPE_SELECTION}.')

            self.selection = selection


def execute_sql_query(query, sql_server, sql_db, odbc_driver_version=17, disable_timeout=False,
                      test_timeout=10, query_timeout=100,
                      db_location=c.STORAGE_TYPE_MSSQL):
    '''
    Execute a SQL query on either a Microsoft SQL Server database or a SQLite database.

    :param str query: SQL statement
    :param str sql_server: name of the server
    :param str sql_db: name of the database
    :param odbc_driver_version: for MS SQL Server, which ODBC driver has been installed and can be used.
        :type odbc_driver_version: int or str
    :param bool disable_timeout: if True, then ignore test_timeout/query_timeout
    :param int test_timeout: do an initial test (get one row) to ensure that query will not take forever to run and
        hang the process. This is how many seconds to allow the test query to run for. Usually not modified by user.

    :param int query_timeout: how many seconds to allow query to run before timing out.
    :param enum db_location: Indicate the STORAGE_TYPE. Refer to constants.py.

    :return: dataframe of query results
    '''

    df = None
    cnxn = None

    def handle_sql_variant_as_string(value):
        return value.decode('utf-16le')

    try:
        cnxn = pyodbc.connect("DRIVER={ODBC DRIVER " + str(odbc_driver_version) +
                              " for SQL Server};SERVER=" + sql_server + ";DATABASE=" + sql_db +
                              ";Trusted_Connection=yes;)")
        # First let's see if we can just get one row in a very short period of time.
        # This will fail if the path doesn't actually join things together nicely and we can save some time
        if not disable_timeout:
            if db_location == c.STORAGE_TYPE_MSSQL:
                # need to match the following:
                # "SELECT TOP 50 column_1..."
                # "SELECT TOP 50 * FROM "
                # "SELECT column_1 FROM"
                # "SELECT * FROM"
                query_test = re.sub(r'^\s*SELECT(\s+\S+\s+(FROM|\d+)\s+|\s+)', 'SELECT TOP 1 ', query)
            else:
                query_test = re.sub(r'LIMIT\s+\d+', 'LIMIT 1', query)

            cnxn.timeout = test_timeout
            logging.debug(f'Executing TEST SQL query to {sql_server}.{sql_db}: {query_test}')
            cnxn.cursor().execute(query_test).fetchone()
            logging.debug(f'TEST SQL query passed!')

        if disable_timeout:
            cnxn.timeout = 0
        else:
            cnxn.timeout = query_timeout

        cnxn.add_output_converter(-155, handle_sql_variant_as_string)

        logging.info(f'Executing SQL query to {sql_server}.{sql_db}: {query}')
        df = pd.read_sql_query(query, cnxn)
        logging.info(f'SQL query completed!')

    except pd.io.sql.DatabaseError as e:
        # e.args[0] will be something like
        # "Execution failed on sql '...': ('HYT00', '[HYT00] [Microsoft][ODBC Driver 17 for SQL Server]
        # Query timeout expired (0) (SQLExecDirectW)')"
        error_code = e.args[0].split(': (')[-1].split(',')[0].replace("'", '')
        if error_code in ('HYT00', 'HYT01'):
            logging.error('SQL query timed out')
        else:
            logging.error(e.args[0])

    except (pyodbc.OperationalError, pyodbc.ProgrammingError) as e:
        logging.error(e)

    except Exception as e:
        # https://stackoverflow.com/questions/1095601/find-module-name-of-the-originating-exception-in-python
        logging.error('Uncaught exception')
        frm = inspect.trace()[-1]
        mod = inspect.getmodule(frm[0])
        logging.error(f'Thrown from {mod.__name__}')
        logging.error(e)
        raise(e)

    finally:
        # ensures that connection never remains open
        if cnxn is not None:
            cnxn.close()
        logging.debug('CLOSED CONNECTION')
        if df is None:
            df = pd.DataFrame()

    return df


def calculate_series_metadata(series):
    '''
    Get vital information about a pandas series

    :param series: a pandas series to analyze
    :return: dictionary of data about this series
        :series_data_type: is the series DISCRETE, CONTINUOUS, or DATETIME
        :is_many: if the series has non-unique values, then this is True.
        :num_non_null: size of series after removing null values
        :unique_values: if DISCRETE, this is a list of unique values in the series
        :min: actual minimum if not DISCRETE
        :max: actual maximum if not DISCRETE
    '''

    dropna_series = series.dropna()
    dropna_len = len(dropna_series)
    unique_values = list(dropna_series.unique())
    dropna_unique_len = len(unique_values)

    if dropna_len > dropna_unique_len:
        is_many = True
    else:
        is_many = False

    if is_datetime64_any_dtype(dropna_series):
        series_data_type = c.SERIES_TYPE_DATETIME
        unique_values = []
    elif is_numeric_dtype(dropna_series):
        if dropna_unique_len == 2:
            if 0 in dropna_series.unique() and 1 in dropna_series.unique():
                series_data_type = c.SERIES_TYPE_DISCRETE
            else:
                series_data_type = c.SERIES_TYPE_CONTINUOUS
        elif dropna_unique_len == 1:
            if 1 in dropna_series.unique():
                series_data_type = c.SERIES_TYPE_DISCRETE
            else:
                series_data_type = c.SERIES_TYPE_CONTINUOUS
                unique_values = []
        else:
            series_data_type = c.SERIES_TYPE_CONTINUOUS
            unique_values = []
    elif is_datetime64_any_dtype(pd.to_datetime(dropna_series, errors='ignore')):
        series_data_type = c.SERIES_TYPE_DATETIME
        unique_values = []
    else:
        series_data_type = c.SERIES_TYPE_DISCRETE

    if series_data_type == c.SERIES_TYPE_DISCRETE:
        min = None
        max = None
    elif series_data_type == c.SERIES_TYPE_DATETIME:
        min = dropna_series.min()
        max = dropna_series.max()
    else:
        min = float(dropna_series.min())
        max = float(dropna_series.max())

    return {
        'series_data_type': series_data_type,
        'is_many': is_many,
        'num_non_null': dropna_len,
        'unique_values': unique_values,
        'min': min,
        'max': max
    }


def start_session(in_memory=False):
    global session

    if in_memory:
        url = 'sqlite://'
    else:
        user_data_dir = appdirs.user_data_dir(appname='db_extract', appauthor='db_extract')
        metadata_db_location = os.path.join(user_data_dir, c.DEFAULT_METADATA_NAME)
        url = 'sqlite:///' + metadata_db_location

        if not database_exists(url):
            logging.info(f'Metadata database was not found at {url}, maybe because this is the first import '
                         'of db_extract. Will initialize it now.')
            try:
                os.mkdir(user_data_dir)
            except FileExistsError:
                logging.info(f'User data directory {user_data_dir} has already been created, '
                             'probably from prior import.')

            metadata_db_location = os.path.join(user_data_dir, c.DEFAULT_METADATA_NAME)

            url = 'sqlite:///' + metadata_db_location

    engine = create_engine(url)

    if in_memory or not database_exists(url):
        logging.info(f'Creating blank metadata db at {url}')
        session = sessionmaker()
        session.configure(bind=engine)

        Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()


def get_datasets(in_memory=False):
    global session

    if session is None:
        start_session(in_memory=in_memory)
    return sorted([x.dataset_name for x in session.query(DatasetMetadata).all()], key=lambda x: x.upper())


def get_column_metadata_from_id(column_id, as_dict=True, in_memory=False):
    global session

    if session is None:
        start_session(in_memory=in_memory)
    x = session.query(ColumnMetadata).filter(ColumnMetadata.id == column_id).first()

    if as_dict:
        try:
            return x.__dict__
        except AttributeError:
            return None
    return x
