# Tools

# Development tools

## Clearing models and migrations 

If you want to clear all models and migrations, use the `redbean clear` command.

It is helpful during development to recreate models based on database content. 

For example, when we switch from one test database to another.

```bash
# before
redbean.setup(dsn=False)

# now
redbean.setup('postgresql+psycopg://postgres:pass@localhost/postgres')
```

```bash
redbean clear_models
```

By default, the model's directory is `redbean`. But it can be overridden by

```bash
redbean clear_models --directory my_module/my_redbean
```

or via environment variable:

```bash
REDBEAN_DIRECTORY=my_module/my_redbean redbean clear_models
```

## Nuke

Nuke, as their name suggests, is a tool for destroying everything.

Nuke is a helpful command in the early stage of development. It removes all models and migrations and clears the whole database.

:warning: For security reasons, `nuke` may only be fired against the localhost or local container database. Running a nuke against the remote database is not possible.

### Usage:

```bash
redbean nuke --dsn postgresql+psycopg://postgres:pass@localhost/postgres
```
Or via environment variables:
```bash
REDBEAN_DB_DSN=postgresql+psycopg://postgres:pass@localhost/postgres redbean nuke
```

:information: If any `--dsn` nor `REDBEAN_DB_DSN` environment variable is provided, then the test base (created by `setup(dsn=False)`) will be removed.

#
 
By default, the namespace and models directory are `redbean`. But can be overridden by

```bash
redbean nuke --dsn postgresql+psycopg://postgres:pass@localhost/postgres --namespace my_module --directory my_module/my_redbean
```

Or via environment variables:

```bash
REDBEAN_DB_DSN=postgresql+psycopg://postgres:pass@localhost/postgres REDBEAN_NAMESPACE=my_module REDBEAN_DIRECTORY=my_module/my_redbean redbean nuke
```

#
# ___
