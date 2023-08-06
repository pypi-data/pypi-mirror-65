# postgresql.py

import logging
import psycopg2
import psycopg2.extras
import psycopg2.extensions
from typing import List, Tuple
from . import CfDatabase

logger = logging.getLogger(__name__)


class CfPostgresql(CfDatabase):

    def __init__(self, host: str = '127.0.0.1', port: str = '5432', database: str = None, user: str = None,
                 password: str = None, autocommit: bool = False, dictionary_cursor: bool = False,
                 encoding: str = 'utf8'):
        """Interact with a PostgreSQL database.

        Args:
            host: Database server hostname or IP.
            port: Database server port.
            database: Database name.
            user: Database server account username.
            password: Database server account password.
            autocommit: Use autocommit on changes?
            dictionary_cursor: Return the results as a dictionary?
            encoding: Database client encoding ("utf8", "latin1", "usascii")
        """
        super().__init__(host=host, port=port, database=database, user=user, password=password)

        logger.debug(f'Connecting: postgresql://[hidden]:[hidden]@{host}:{port}/{database}')
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
            client_encoding=encoding
        )

        if autocommit is True:
            self.connection.autocommit = True

        if dictionary_cursor is True:
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        else:
            self.cursor = self.connection.cursor()

        # Todo: Some functions need to know how to interpret the results of a query. Knowing if it's a DictRow helps.
        self.dictionary_cursor = dictionary_cursor

        logger.debug('Database connection established.')

    def connection_status(self) -> str:
        """Return psycopg2 connection status.

        Returns:
            Connection status
        """
        results = self.execute('SELECT version()')
        if 'PostgreSQL' in results[0]['version']:
            return 'OK'
        else:
            return 'Error'

    @staticmethod
    def split_table_path(table_path: str = None) -> Tuple[str, str]:
        """Split table_path into it's schema and table parts.

        Args:
            table_path: Table name in the form <schema>.<table>
        Returns:
            schema, table
        """
        if table_path is None:
            raise ValueError('warehouse_table cannot be None.')

        schema = table_path.split('.')[0]
        try:
            table = table_path.split('.')[1]
        except IndexError:  # A missing period result in no second value, throwing an IndexError.
            raise ValueError(f'table_path not in proper <schema>.<table> format: {table_path}')

        return schema, table

    def database_exists(self, database_name: str = None) -> bool:
        """Test for the existence of a database.

        Args:
            database_name: Name of the database to search for.
        Returns:
            True, if database exists. False, if not.
        """
        results = self.execute(f'''
                    SELECT EXISTS(
                      SELECT 1
                      FROM pg_catalog.pg_database
                      WHERE datname = '{database_name}'
                    );
                ''')

        if results[0][0] is not True:
            return False
        else:
            return True

    def schema_exists(self, schema_name: str = None) -> bool:
        """Test for the existence of a schema.

        Args:
            schema_name: Name of the schema to search for.
        Returns:
            True, if schema exists. False, if not.
        """
        results = self.execute(f'''
                    SELECT EXISTS(
                      SELECT 1
                      FROM information_schema.schemata
                      WHERE schema_name = '{schema_name}'
                    );
                ''')

        if results[0][0] is not True:
            return False
        else:
            return True

    def table_exists(self, table_path: str = None) -> bool:
        """Test for the existence of a schema table.

        Args:
            table_path: Table name in the form <schema>.<table>
        Returns:
            True, if table exists. False, if not.
        """
        schema, table = self.split_table_path(table_path)

        results = self.execute(f'''
            SELECT EXISTS(
              SELECT 1
              FROM pg_catalog.pg_tables
              WHERE schemaname = '{schema}'
              AND tablename = '{table}'
            );
        ''')

        if results[0][0] is not True:
            return False
        else:
            return True

    def fields_exist(self, table_path: str = None, table_fields: List = None) -> bool:
        """Test for the existence of table fields.

        Args:
            table_path: Table name in the form <schema>.<table>
            table_fields: A list of fields to check.
        Returns:
            True, if all fields are present in the table. False, if not.
        """
        schema, table = self.split_table_path(table_path)

        # Get table columns and data types
        results = self.execute(f'''
            SELECT column_name
            FROM information_schema.columns
            WHERE 
              table_schema = '{schema}'
              AND table_name = '{table}';
        ''')

        live_table_fields = []

        # todo: FIX -- This only works if dict_cursor = True
        for result in results:
            live_table_fields.append(result['column_name'])

        all_fields_present = True
        for table_field in table_fields:
            if table_field not in live_table_fields:
                logger.warning(f'field ({table_field}) not in live table {table_path}.')
                all_fields_present = False

        return all_fields_present

    def get_primary_keys(self, table_path: str = None) -> List[str]:
        """Get a table's primary key(s).

        Args:
            table_path: Table name in the form <schema>.<table>
        Returns:
            A list of primary keys.
        """
        results = self.execute(f'''
            SELECT pg_attribute.attname, format_type(pg_attribute.atttypid, pg_attribute.atttypmod) AS data_type
            FROM pg_index
            JOIN pg_attribute 
              ON pg_attribute.attrelid = pg_index.indrelid AND pg_attribute.attnum = ANY(pg_index.indkey)
            WHERE pg_index.indrelid = '{table_path}'::regclass
            AND pg_index.indisprimary;
        ''')

        keys = []
        if self.dictionary_cursor is True:
            for result in results:  # Result is a psycopg2.extras.DictRow, which can be used as a list or dictionary.
                keys.append(result['attname'])
            return keys

        # Todo: Add a non-dict cursor return
