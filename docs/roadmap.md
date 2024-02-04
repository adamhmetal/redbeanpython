# Roadmap

Current version 1.0.0 is production-ready, covered by tests on various databases and package versions, but version 1.0.0 contains only the absolute minimum of features.
As an idea, RedBeanPython will never be as feature-rich as SQLAlchemy, as its goal is different: to work hybrid with SQLAlchemy.
For example, bulk operations or joined loading are not considered to be ever implemented in RedBeanPython, as if we have such cases, hybrid mode and SQLAlchemy [should be used directly](hybrid_mode.md) in such places.
But to be fully functional, three main features are needed: transactions, relations and indexes.
Planned to add the following versions:

- Transactions

```python
with redbean.transaction() as t:
    subscription = Bean('subscription')
    user.price = Decimal('9.99')
    t.store(subscription)
    user = Bean('user')
    user.name = "Adam"
    user.age = 42
    user.subscription_id = subscription.id
    t.store(user)
```

- Relations

```python
subscription = Bean('subscription', ...)

invoices = [
    Bean('invoice', ...),
    Bean('invoice', ...),
]

user = Bean('user')
user.subscription = subscription
user.invoices = invoices 
```

- Indexes

```python
user().index('name', 'age')
```

#
# ___