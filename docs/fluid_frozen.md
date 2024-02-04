# Fluid, Frozen mode

By default, in development mode, RedBeanPython is in fluid mode. 

It means it will create new columns in the database if they are absent. It will also add new fields to the model. And take care of all migrations in the background.

Fluid mode is very convenient for development, but it is not recommended for production.

On production, you should use frozen mode. In frozen mode, RedBeanPython will not modify anything in the database.

Because RedBeanPython will create alembic migrations automatically during development (in fluid mode), all that needs to be done is to run alembic migrations on production. 

# Freezing database

To freeze the database, add `frozen=True` to `redbean.setup()` call like:

```python
redbean.setup(dsn=False, frozen=True)
```

Or use `REDBEAN_DB_FROZEN` environment variable:

```
REDBEAN_DB_FROZEN=1
```


Since then, **no automatic changes** have been made to the database.

In addition, there will be no automatic model changes. Models existing in the code base will be used without modifications.

Because of that behaviour, we have **full control over the database and models in the production environment**.

# Running migrations

Alembic migrations are created by default in the namespace directory.

Example directory structure:
```
migrations
    versions 
        1706519938318070_.py
        1706519970704551_.py
    env.py 
models
    user.py
```

Migrations (on production) can be executed by running alembic migrations:

```bash
cd redbean/migrations 
DB_DSN="postgresql+psycopg://user:pass@host/dbname" alembic upgrade head
```

#
# ___
