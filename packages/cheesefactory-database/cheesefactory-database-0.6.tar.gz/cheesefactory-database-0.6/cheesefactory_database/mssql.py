# mssql.py

import logging
import pyodbc

logger = logging.getLogger(__name__)


class CfMssql:

    def __init__(self, host: str = '127.0.0.1', port: str = '5432', database: str = None, user: str = None,
                 password: str = None, driver: str = None):
        """Interact with a MSSQL database.

        host: Database server hostname or IP.
        port: Database server port.
        database: Database name.
        username: Database server account username.
        password: Database server account password.
        driver: Database client driver ("{MSSQLSERVER}, {ODBC Driver 17 for SQL Server}, etc.").
        """

        super().__init__(host=host, port=port, database=database, user=user, password=password)

        logger.debug(f'Connecting: postgresql://[hidden]:[hidden]@{host}:{port}/{database}')

        connection_string = f'DRIVER={driver};SERVER={host};DATABASE={database};UID={user};PWD={password}'

        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()
        logger.debug('MSSQL database connection established.')
