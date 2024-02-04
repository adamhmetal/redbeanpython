# Find, Count, Exists

## Finding

The finding can be done by query and parameters with the syntax [consistent with SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text).

```python
result: Iterator[Bean] = redbean.find(  #(1)
    'user', 
    query="age > :age and active = :active", 
    params={"age": 21, "active": True},
    order="age desc",
    limit=10,
    offset=20,
)

result: Iterator[Bean] = redbean.find(  #(2)
    'user', 
    query="age > :age and active = :active", 
    params={"age": 21, "active": True},
)

result: Iterator[Bean] = redbean.find('user')  #(3)
```

1. Find all records of type `user` with `age > 21` and `active = True` ordered by `age desc` with limit `10` starting from offset `20`.
2. Find all records of type `user` with `age > 21` and `active = True`.
3. Find all records of type `user`.

:information: Find can be safely run against not existing (at that moment) bean types (tables).  

```python
print(list(redbean.find('not_existing_yet_in_database')))
```
```bash
[]
```

### Alternative syntax

If you do not want to use a text query with parameters, you can use SQLAlchemy. (Hybrid mode).
The main difference is that the result object is `list[Model]`, not `Iterator[Bean]`.


```python
with redbean.session_maker() as session:
    query = session.query(User)
    query = query.filter(User.age > 21)
    query = query.filter(User.active == True)
    query = query.order_by(User.age.desc())
    query = query.limit(10)
    query = query.offset(20)
    result: list[User] = query.all()
    for user in result:
        print(user.as_dict())
```

## Counting

Counting can be done by query and parameters with syntax [consistent with SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text).

```python
count: int = redbean.count( #(1)
    'user', 
    query="age > :age and active = :active", 
    params={"age": 21, "active": True}
)

count: int = redbean.count('user') #(2)
```

1. Count records of type `user` with `age > 21` and `active = True`.
2. Count all records of type `user

:information: Count can be safely run against not-existing (at that moment) bean types (tables). 

```python
print(redbean.count('not_existing_yet_in_database'))
```
```bash
0
```

### Alternative syntax

If you do not want to use a text query with parameters, you can use SQLAlchemy. [Hybrid mode](hybrid_mode.md).

```python
with redbean.session_maker() as session:
    query = session.query(User)
    query = query.filter(User.age > 21)
    query = query.filter(User.active == True)
    count: int = query.count()
```



## Checking the existence of a bean

Existence can be checked with the `exists` method.

```python
is_exists: bool = redbean.exists('user', bean_id=user_id)
```

:information: It can be safely run against not-existing (at that moment) bean types (tables).

```python
print(redbean.exists('not_existing_yet_in_database', bean_id="some_id"))
```
```python
False
```

#
# ___



