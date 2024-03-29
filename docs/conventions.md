# Conventions

### Via Facade (recommended):

You can use RedBeanPython via the facade instance initialized in the `redbeanpython` package. This way is recommended because it will provide consistent usage of the same engine throughout the whole project.

Just import the `redbeanpython` package and call the `setup` method to use it.

```python
from redbeanpython import redbean

redbean.setup(dsn=False)
user = redbean.load('user', '1234')
```

Or, if you prefer, as a short alias:

```python
from redbeanpython import r

r.setup(dsn=False)
user = r.load('user', '1234')
```

Both usages will use a facade that proves consistent usage of the same engine in the project.

### Directly:

The third way is to use the `RedBean` class directly. This way can be helpful:
- if you want to use it in your own dependency manager,
- if you want to connect to multiple databases in one project,
- in automatic tests.

```python
from redbeanpython import RedBean

redbean = RedBean(dsn=False)
user = redbean.load('user', '1234')
```

## Naming

Allowed names (for beans and its properties):

- have to be proper identifiers. (It can contain only letters, digits, and underscores and can not start with a digit.)
- have to be _snake_case_.
- must not start with an underscore.

Examples:

```python
# allowed
bean = Bean('user')
bean = Bean('admin_user')
bean.id = "..."
bean.name = "..."
bean.other_name_2 = "..."

# not allowed
bean = Bean('User')
bean = Bean('adminUser')
bean.name = "..."
bean.Name = "..."
```

## Id

Every bean has **`id`** property. It has to be a string (or `Id` class). If it is not set during object creation, then it is, by default, an autogenerated UUID4 string.

The decision to resign from the autoincrement integer was taken for security reasons: it is not possible to guess other objects' id, and it is not possible to iterate over all objects. For example, in case of potential problems with proper user authorization, the user can not steal other users' data just by asking for their next/previous IDs.  


## Restricted keywords:
 
- **`keys`** can not be used as a property name (because is used internally by Python during casting bean object to dict `dict(bean)`)

#
# ___