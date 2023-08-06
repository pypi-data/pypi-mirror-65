# cheesefactory-database

-----------------

##### A wrapper for psycopg2.
[![PyPI Latest Release](https://img.shields.io/pypi/v/cheesefactory-database.svg)](https://pypi.org/project/cheesefactory-database/)
[![PyPI status](https://img.shields.io/pypi/status/cheesefactory-database.svg)](https://pypi.python.org/pypi/cheesefactory-database/)
[![PyPI download month](https://img.shields.io/pypi/dm/cheesefactory-database.svg)](https://pypi.python.org/pypi/cheesefactory-database/)
[![PyPI download week](https://img.shields.io/pypi/dw/cheesefactory-database.svg)](https://pypi.python.org/pypi/cheesefactory-database/)
[![PyPI download day](https://img.shields.io/pypi/dd/cheesefactory-database.svg)](https://pypi.python.org/pypi/cheesefactory-database/)

## Main Features

* Built on psycopg2.
* Pandas dataframe support.
* Test table existence.
* Test field existence.

**Note:** _This package is still in beta status. As such, future versions may not be backwards compatible and features may change._

## Installation
The source is hosted at https://bitbucket.org/hellsgrannies/cheesefactory-database


```sh
pip install cheesefactory-database
```

## Dependencies

* [psycopg2](https://www.psycopg.org/)
  
## License

## Parameters

class **CfPostgres**(host: str = 127.0.0.1, port: int = 5432, user: str = None, password: str = None, database: str = None)

Handles the connection to a PostgreSQL database.

* _host_: PostgreSQL server hostname/IP.
* _port_: PostgreSQL server port.
* _user_: Username for authentication.
* _password_: Password for authentication.
* _database_: Database for connection

## Examples

**Connect to the remote SFTP server**


```python
from cheesefactory-database.postgresql import CfPostgres

# Establish connection
db = CfPostgres(host='myhostname', user='myusername', password='mypassword', database='mydatabase')

# Execute query
results = db.execute("SELECT first_name, last_name FROM person WHERE last_name = 'Smith'")

```
