# Idea
    
One of Python's most significant advantages is that we can make applications fast. Boilerplate is low, but we can focus on business logic, quickly deliver value, and make projects production-ready. But even if, with current powerful libraries, "time-to-market" is low, it can be lowered even more.

The idea of RedBeanPython ORM is to decrease the time to market for applications by providing an absolutely zero configuration ORM and, simultaneously, heaving the possibility of zero effort transition to advanced ORM when needed.

[RedBeanPython](https://redbeanpython.org) idea is inspired by the matured [RedBeanPHP ORM](https://www.redbeanphp.com/index.php) (since 2009 and still running).

RedBeanPython ORM's idea is not to replace the more advanced ORMs (we should not reinvent the wheel) but to cooperate with them. Initially, it can be used as only ORM. When projects evolve, both code bases (RedBeanPython and SQLAlchemy) can coexist and, finally, can be swiftly replaced by SQLAlchemy (if needed).

![Tests on PostgreSQL](https://github.com/adamhmetal/redbeanpythondev/actions/workflows/test_postgres.yml/badge.svg) 
![Tests on MySQL](https://github.com/adamhmetal/redbeanpythondev/actions/workflows/test_mysql.yml/badge.svg) 
![Tests on SQLite](https://github.com/adamhmetal/redbeanpythondev/actions/workflows/test_sqlite.yml/badge.svg)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=adamhmetal_redbeanpythondev&metric=coverage)](https://sonarcloud.io/summary/new_code?id=adamhmetal_redbeanpythondev)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=adamhmetal_redbeanpythondev&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=adamhmetal_redbeanpythondev)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=adamhmetal_redbeanpythondev&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=adamhmetal_redbeanpythondev)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=adamhmetal_redbeanpythondev&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=adamhmetal_redbeanpythondev)


# Installation

RedBeanPython is available on PyPI and can be installed with pip:

```bash
pip install redbeanpython
```

[RedBeanPython on PyPI](https://pypi.org/project/redbeanpython/)

# Documentation

Documentation is available on [redbeanpython.org](https://redbeanpython.org/).

## Requirements

RedBeanPython requires

- Python 3.11 or newer.
- SQLAlchemy 2.0 or newer.
- alembic 1.7 or newer.


## Database requirements

For **PostgreSQL** support RedBeanPython requires:

- psycopg2 2.9.9 or newer.

For **MySQL/MariaDB** support RedBeanPython requires:

- PyMySQL 1.0.2 or newer.


# How it works? Let's see an example of a usual project lifecycle.
### Stage 1. **Development**

We are starting a fresh project. We have an Idea, and we want to deliver MVP to production as soon as possible.

We have an empty database (or no database at all at that moment).

Let's store some data:

```python
from datetime import datetime
from decimal import Decimal

from redbeanpython import redbean, Bean

redbean.setup(dsn=False) #(1)

user = Bean('user')
user.name = 'Adam'
user.age = 42
user.subscription_price = Decimal("12.20")
user.subscription_end = datetime.fromisoformat('2024-10-08T16:20:00')

redbean.store(user)
```

1.  For a temporary SQLite database call `redbean.setup(dsn=False)`. 
    For a production database, DSN consistent with SQLAlchemy should be provided. 
    See [connection](https://redbeanpython.org/connection/) for more details. 
    For example, you may run a docker container with PostgreSQL:
    ```bash
    docker run -p 5432:5432 -e POSTGRES_PASSWORD=pass -d postgres
    ```
    And use it:
    ```python
    redbean.setup('postgresql+psycopg://postgres:pass@localhost/postgres')
    ```

And that's all. 

No schema is need to be created, no migrations need to be run, no config files to update.

Just **run the code**, and RedBeanPython will **create everything automatically**. 

If we take a look into db, we will see that table was created:
```postgresql
create table user
(
    age                BIGINT,
    id                 VARCHAR(255) not null primary key,
    name               TEXT,
    subscription_end   DATETIME,
    subscription_price NUMERIC(30, 10)
);
```

In the background, the SQLAlchemy model was created:

```python
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Numeric

from redbeanpython import Model


class User(Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    age = Column(BigInteger, nullable=True)
    id = Column(String(255), primary_key=True)
    name = Column(Text, nullable=True)
    subscription_end = Column(DateTime, nullable=True)
    subscription_price = Column(Numeric(precision=30, scale=10), nullable=True)

    def __json__(self):
        return self.as_dict()

    def as_dict(self):
        return {
            'age': self.age,
            'id': self.id,
            'name': self.name,
            'subscription_end': self.subscription_end,
            'subscription_price': self.subscription_price,
        }
```

We do not need this information now, but it might be helpful later. (See section: [hybrid mode](https://redbeanpython.org/hybrid_mode/))

Let's load it from the database, and as we see, the types are preserved:

```pycon
>>> from redbeanpython import redbean
>>> redbean.setup(dsn=False)
>>> users = list(redbean.find('user'))
>>> user = users[0]
>>> print(dict(user))
{
    'age': 42, 
    'id': '1f0e6e46-6e47-404f-9547-9dc3e9741ec6', 
    'name': 'Adam', 
    'subscription_end': datetime.datetime(2024, 10, 8, 16, 20), 
    'subscription_price': Decimal('12.2000000000')
}
>>> print(type(user.subscription_end), user.subscription_end)
<class 'datetime.datetime'> 2024-10-08 16:20:00
```

#
Let's go on; development continues.

In the early stage of the project, life changes are widespread. Often, we even rewrite the first ideas.

With RedBeanPython, this is no problem; we can change the code and run it again. RedBeanPython will adjust everything automatically.

For example, we decided that the user should have a birthday. We can add in code:

```python
# ...
user.birthday = date.fromisoformat('1981-12-01')
# ...
```

And rerun it. RedBeanPython will adequately adjust the database schema. 

The database schema has been adjusted.

```postgresql
create table user
(
    age                BIGINT,
    id                 VARCHAR(255) not null primary key,
    name               TEXT,
    subscription_end   DATETIME,
    subscription_price NUMERIC(30, 10),
    birthday           DATE  -- (1)
);
```

1. A new column was added.

Same as model:

```python
class User(Model):
    # (...)
    name = Column(Text, nullable=True)
    subscription_end = Column(DateTime, nullable=True) # (1)
    subscription_price = Column(Numeric(precision=30, scale=10), nullable=True)
    # (...)

    def as_dict(self):
        return {
            # (...)
            'name': self.name,
            'subscription_end': self.subscription_end, # (2)
            'subscription_price': self.subscription_price,
        }
```

1. A new property was added.
2. A new property was added.

And alembic migration was created automatically:
```python
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('birthday', sa.Date(), nullable=True))

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('birthday')
```

:information: Migrations will be useful later when the project is production-ready.

#

Now, when we have MVP ready, we can go to production.

### Stage 2: **Production** 

When the project stays production-ready, we would like to [freeze](https://redbeanpython.org/fluid_frozen/) production database to avoid potential unexpected changes. 
No automatic changes will be made to production since that moment. 

To freeze the database, we just need to add one parameter to `redbean.setup()` call:

```python
redbean.setup('...', frozen=True)
```

Or use `REDBEAN_DB_FROZEN=1` environment variable.

And, from that time on production, we can use **alembic** migrations to manage production database schema changes safely.
We fully control how and when the database schema will be changed.

Because alembic migrations are created automatically by RedBeanPython, we can just run:

```bash
cd redbean/migrations 
DB_DSN="sqlite:////tmp/redbean.sqlite" alembic upgrade head
```

on production to apply all changes.

At the same time, everything will work as before in the development environment, and we still have all the benefits from automatic creation. 

### Stage 3: **Project growth**

When the project grows, we may need more performance or more sophisticated database features.
As RedBeanPython is not intended to be a replacement for SQLAlchemy, instead of extending RedBeanPython forever, we can switch to SQLAlchemy ORM and take full advantage of the giants. 

Moreover, we can use both ORMs simultaneously and switch to more advanced ORMs with **zero effort** for specific cases only.

As SQLAlchemy Models has already been created automatically, we can use it. 

Let's see how it works.

```python
from redbean.models.customer import Customer
from redbean.models.invoice import Invoice

redbean.setup(dsn=False)

# redbeanpython code
customer = Bean('customer')
customer.name = 'John'

invoice = Bean('invoice')
invoice.amount = Decimal("12.20")
invoice.customer_id = customer.id

redbean.store_many([invoice, customer])

# sqlalchemy code
session = redbean.session_maker()
query = session.query(Customer, Invoice)
query = query.filter(Customer.id == Invoice.customer_id)
query = query.filter(Invoice.amount > 10)
result = query.all()
for customer, invoice in result:
    print(customer.name, invoice.amount)

query = session.query(
    Invoice.customer_id,
    func.count('*').label('amount'),
    func.sum(Invoice.amount).label('amount'),
)
query = query.group_by(Invoice.customer_id)
for customer_id, invoices_count, invoices_total, in query.all():
    print(f"{customer_id} has: {invoices_count} invoices with a sum: {invoices_total}")

    # redbeanpython code again
    print(customer_id)
    customer = redbean.load('customer', customer_id)
    print(dict(customer))
```

We can freely mix both ORMs in the same code base. This is a [**hybrid mode**](https://redbeanpython.org/hybrid_mode/).

Finally, when our project succeeds, it will be on the market for months or years. Development team grows. Codebase enlarges - we can want to switch to SQLAlchemy ORM entirely.

### Stage 4: **Maturity**

When the project matures and we decide to switch entirely to SQLAlchemy ORM, we can say goodbye to RedBeanPython methods and start to use SQLAlchemy only.

Starting with previously automatically generated Models, we will continue to extend them and work with them in a standard SQLAlchemy way.


And then you can let RedBeanPython go. RedBeanPython did its job. It's time for retirement.

**It was a beautiful journey!**

Check more on [redbeanpython.org](https://redbeanpython.org).

## Licence
Licence: MIT

## Issue tracker
Issue tracker is available on GitHub.

## Contact
Adam Puza: adampuza@redbeanpython.org

#
# ___