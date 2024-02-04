# SQLAlchemy differences

[Hybrid Mode](hybrid_mode.md) is the most efficient way of working with RedBeanPython and SQLAlchemy simultaneously.

But if you want to go further and fully migrate to SQLAlchemy, you should be aware of some differences. 

# Finding/counting

The internal implementation of RedBeanPython is based on SQLAlchemy parametrized text queries.

However, after switching to SQLAlchemy Models, using text queries becomes an antipattern. It would be best if you used SQLAlchemy syntax for model-based syntax.

This RedBeanPython syntax:

```python
count: int = redbean.count(
    'user', 
    query="age > :age and active = :active", 
    params={"age": 21, "active": True}
)
```

It is an equivalent of:

```python
count: int = session.query(User).filter(
    User.age > 21, User.active == True
).count()
```

### Same with find


```python
for u in redbean.find(
    'user',
    query="age > :age and active = :active",
    params={"age": 21, "active": True}
):
    print(dict(u))
```

It is an equivalent of:

```python
for u in (
        session.
        query(User).
        filter(
            User.age > 21,
            User.active == True,
        ).
        all()
):
    print(u.as_dict())
```

## Create

```python
user = Bean('user', {'id': "1", "name": "Adam"})
redbean.store(user)
#(...)
redbean.store(user)
```

In RedBeanPython, this code will work; the second object will replace the first one.

:information: RedBeanPython operations are idempotent by design.

But in SQLAlchemy, this code will throw an exception because of a unique constraint violation.

```python
user = User()
user.id = "3"
user.name = "Hanna"

session.add(user)
session.commit()
#(...)
session.add(user)
session.commit()
```

#
# ___