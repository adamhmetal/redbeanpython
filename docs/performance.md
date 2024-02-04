# Performance

## Introduction

**Most** of the operations in RedBeanPython work with **similar complexity as SQLAlchemy**. However, RedBeanPython specification makes few operations more complex than SQLAlchemy equivalents.

### Operations with more extensive complexity

- Store/Add. Complexity `2x` regarding SQLAlchemy.
- Update. Complexity `2x` regarding SQLAlchemy.

## Performance improvements

For most cases where RedBeanPython is dedicated, performance will be more than enough.

But when you start to work on the scale, you can use some of these tips:

- Add indexes to your tables. RedBeanPython does not automatically add indexes (it is planned in the following versions).
- Replace bulk operations with Hybrid Mode equivalents (see [Bulk operations](bulk_operations.md)).
- Replace joined loading with Hybrid Mode equivalents (see [Joined load](joined_load.md)).

#
# ___