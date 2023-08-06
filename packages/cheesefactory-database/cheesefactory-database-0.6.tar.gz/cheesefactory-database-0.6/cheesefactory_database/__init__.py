# __init__.py

import logging
import pandas.io.sql as psql
from typing import Any

logger = logging.getLogger(__name__)


class CfDatabase:

    def __init__(self, host: str = '127.0.0.1', port: str = '5432', database: str = None, user: str = None,
                 password: str = None):
        """Interact with a database.

        Args:
            host: Database server hostname or IP.
            port: Database server port.
            database: Database name.
            user: Database server account username.
            password: Database server account password.
        """

        self.connection = None
        self.cursor = None

        if None in (host, port, database, user, password):
            message = 'Connection string cannot contain None: database://'
            message += 'None:' if user is None else '[hidden]:'
            message += 'None' if password is None else '[hidden]'
            message += f'@{host}:{port}/{database}'
            raise ValueError(message)

    def execute(self, query: str, dataframe: bool = False, fetchall: bool = True) -> Any:
        """Execute a SQL query

        Args:
            query: SQL query to execute.
            dataframe: Output the results as a dataframe?
            fetchall: Perform a fetchall() and return the results?

        Returns:
            SQL query results as array or dataframe (if dataframe == True).
        """
        if query is None:
            raise ValueError('query should not be None!')
        logger.debug(f'Executing query:\n\n{query}')

        if dataframe is True:
            return psql.read_sql_query(query, self.connection)
        else:
            self.cursor.execute(query)
            if fetchall is True:
                return self.cursor.fetchall()
            else:
                return None

    def __del__(self):
        """Class destructor. Clean up we want to be explicit about."""

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.commit()
            self.connection.close()
