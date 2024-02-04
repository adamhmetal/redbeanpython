# Connection

RedBeanPython works with PostgreSQL, MySQL/MariaDB and SQLite.

# Setup via ENV

A typical pattern for setting up a RedBeanPython connection is setting the environment variable `REDBEAN_DB_DSN`.

F.e. for PostgreSQL:

`REDBEAN_DB_DSN=postgresql+psycopg://user:pass@host/dbname`

If `REDBEAN_DB_DSN` is set, it will be used as DSN for database connection just by calling:

```python
from redbeanpython import redbean
redbean.setup() # (1)
```

1. `dsn=os.environ.get('REDBEAN_DB_DSN')` => `postgresql+psycopg://user:pass@host/dbname`

# Test database

To connect to an SQLite testing database, use:

```python
from redbeanpython import redbean
redbean.setup(dsn=False)
```

It will create SQLite **test** database `redbean.sqlite`  in the system's temporary directory and connect to it.

:warning: Remember that, in most operating systems, this database will be deleted after the system reboots.

# Real database connection

## PostgreSQL (recommended)

PostgreSQL is the recommended database for production use. RedBeanPython performs best with it.

DSN (consistent with SQLAlchemy):

```python
redbean.setup('postgresql+psycopg://user:pass@host/dbname')
```

### Example

Run dockerized PostgreSQL:

```bash
docker run -p 5432:5432 -e POSTGRES_PASSWORD=pass -d postgres
```

and connect to it:

```python   
from redbeanpython import redbean
redbean.setup('postgresql+psycopg://postgres:pass@localhost/postgres')
```

## MySQL/MariaDB

MySQL (because of how it supports TEXT type) performs worse than PostgreSQL but is still a good choice for production use.

DSN (consistent with SQLAlchemy):

```python
redbean.setup('mysql+pymysql://user:pass@host/dbname')
```

### Example

Run dockerized MySQL:

```bash
docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pass -e MYSQL_DATABASE=db -d mysql
```

or MariaDB:


```bash
docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pass -e MYSQL_DATABASE=db -d mariadb
```

and connect to it:

```python
from redbeanpython import redbean
redbean.setup('mysql+pymysql://root:pass@localhost/db')
```

## SQLite

SQLite is a good choice for system/cli applications but is not recommended for web applications.  

DSN (consistent with SQLAlchemy):

```python
redbean.setup('sqlite:///path/to/database.db')
```

### Switching to another database during time of development

:warning:  If we switch to other database during development, we must synchronize the database schema with the code.

The fastest solution in the development environment is to remove models and migrations from the directory.

It can be done manually or by using the `clear_models` command:

```bash
redbean clear_models
```

Alternatively, instead of recreating models, we can run migrations against the new database:

For example, if we switch from `db` to `new_db` database:

```bash
cd redbean/migrations 
DB_DSN="mysql+pymysql://root:pass@localhost/new_db" alembic upgrade head
```

:warning: New database must not contain `alembic_version` table or any previously created by RedBeanPython.

## SQLite limitations

Limited types are supported by SQLite: datetime, date, decimal, and boolean are stored in SQLite in broad data types and made programmatically by the database engine.

From your perspective, internal types do not affect your code; everything works like other databases, and you do not need to consider any code changes.

With one exception, as SQLite  `Decimals` (emulated) are limited to `precision+scale <= 10`, you must consider switching to Postgres or Mysql if your use cases exceed that limit.  

In addition, remember that it is a file-based database; because of that, SQLite's ability to work with more than one connection simultaneously is minimal. (Remember this if you are using the async code.) Even if the Python SQLite library should take care of locking inside one Python process, it will be a problem when more processes are running independently. (i.e., a few different workers trying to access the same SQLite database.  
Because of that, it is suggested to use it only for development or, if you are sure, our app will be single-process only. (You **should not** use SQLite, for example, for web applications (asynchronous by idea).    

#
# ___