# Bulk operations

Bulk operations are designed to decrease the number of requests sent to databases.

With many records to store or update, you should consider using bulk operations.

Bulk operations are out of the scope of RedBeanPython by design, as if we have such use cases, hybrid mode and SQLAlchemy should be used directly in such places.

## Bulk store

A bulk store is used to store many beans at once (with single request).

```python
from sqlalchemy import insert

with redbean.session_maker() as session:
    session.execute(
         insert(User),
         [
             {"id": "a", "name": "Adam", "age": 42},
             {"id": "i", "name": "Ivona", "age": 42},
             {"id": "h", "name": "Hanna", "age": 10},
             {"id": "e", "name": "Eva", "age": 7},
         ],
    )
    session.commit()
```

## Bulk update

A bulk update is used to update many beans at once (with a single request).

```python
from sqlalchemy import update

with redbean.session_maker() as session:
    session.execute(
         update(User),
         [
             {"id": "a", "name": "Adam", "age": 43},
             {"id": "i", "name": "Ivona", "age": 43},
             {"id": "h", "name": "Hanna", "age": 11},
             {"id": "e", "name": "Eva", "age": 8},
         ],
    )
    session.commit()
```

#
# ___
