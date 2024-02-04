from functools import wraps
from typing import Any
from typing import Callable
from typing import Iterator

import sqlalchemy

from redbeanpython.bean.bean import Bean
from redbeanpython.bean.id import Id
from redbeanpython.errors import InitializationError
from redbeanpython.errors import NotInitializedError
from redbeanpython.redbean import RedBean


class _Guard:
    @staticmethod
    def is_initialized(fn: Callable) -> Any:
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            if not self._initialized:
                raise NotInitializedError("RedBean is not initialized")
            return fn(self, *args, **kwargs)

        return wrapper


class Facade:
    def __init__(self):
        self._initialized: bool = False
        self._dsn: str | None = None
        self._directory: str | None = None
        self._namespace: str | None = None
        self._red_bean: RedBean | None = None
        self._frozen: bool | None = None

    def setup(self, dsn=None, *, frozen=False, directory: str = None, namespace: str = None) -> None:
        """
        RedBeanPython works with PostgreSQL, MySQL/MariaDB and SQLite.

        Setup via ENV
        A typical pattern for setting up a RedBeanPython connection is setting the environment variable REDBEAN_DB_DSN.

        F.e. for PostgreSQL:
        > REDBEAN_DB_DSN=postgresql+psycopg://user:pass@host/dbname
        If REDBEAN_DB_DSN is set, it will be used as DSN for database connection just by calling:

        > from redbeanpython import redbean
        > redbean.setup()

        Test database

        To connect to an SQLite testing database, use:
        > redbean.setup(dsn=False)
        It will create SQLite test database redbean.sqlite in the system's temporary directory and connect to it.

        Remember that, in most operating systems, this database will be deleted after the system reboots.

        Real database connection

        PostgreSQL (recommended)
        PostgreSQL is the recommended database for production use. RedBeanPython performs best with it.

        DSN (consistent with SQLAlchemy):
        > redbean.setup('postgresql+psycopg://user:pass@host/dbname')

        MySQL/MariaDB
        MySQL (because of how it supports TEXT type) performs worse than PostgreSQL
        but is still a good choice for production use.

        DSN (consistent with SQLAlchemy):
        > redbean.setup('mysql+pymysql://user:pass@host/dbname')

        SQLite
        SQLite is a good choice for system/cli applications but is not recommended for web applications.

        DSN (consistent with SQLAlchemy):
        > redbean.setup('sqlite:///path/to/database.db')

        Configuration

        As the idea of RedBeanPython is to be as zero-config ORM, by default, no configuration is needed.

        But you can do it if you want to change the default directory/namespace
        and adjust it to your needs and project structure.

        Directory and namespace configuration
        By default, RedBeanPython will create models in the redbean directory in the app's main directory
        and use the corresponding namespace.

        But it can be changed by calling redbean.setup() with directory and namespace parameters.

        > redbean.setup(
        >    "postgresql+psycopg://...",
        >    directory='my_module/my_redbean',
        >    namespace='my_module.my_redbean'
        > )

        or by setting REDBEAN_DIRECTORY and REDBEAN_NAMESPACE environment variables.

        >REDBEAN_DIRECTORY=my_module/my_redbean
        >REDBEAN_NAMESPACE=my_module.my_redbean

        In the above example, models will be created in my_module/my_redbean directory
        and will be available as my_module.my_redbean namespace.
        """
        self._validate_persistent_setup(dsn=dsn, directory=directory, namespace=namespace, frozen=frozen)
        if not self._initialized:
            self._initialized = True
            self._red_bean = RedBean(dsn=dsn, frozen=frozen, directory=directory, namespace=namespace)
            self._dsn = dsn
            self._directory = directory
            self._namespace = namespace
            self._frozen = frozen

    @_Guard.is_initialized
    def dispense(self, bean_type: str) -> Bean:
        """
        Beans can be created just by passing their type to the Bean class.

        > user = Bean('user')

        And their property can be added just as an object property:
        > user.name = "Adam"
        > user.age = 42

        or via a dictionary-like interface

        > user['name'] = "Adam"
        > user['age'] = 42

        An alternative way to create beans is to use the dispense method on engine object

        > user = redbean.dispense('user')
        > user['name'] = "Adam"
        > user['age'] = 42
        """
        return self._red_bean.dispense(bean_type)

    @_Guard.is_initialized
    def store(self, bean: Bean) -> Id:
        """
        Use redbean.store(bean) to store the bean in the database.

        > user = Bean('user')
        > user.name = "Adam"
        > user.age = 42
        > redbean.store(user)

        By default, id is an autogenerated UUID4 string.

        Optionally id can be overridden.

        > user = Bean('user')
        > user.id = "my_own_id_1234"
        > user.name = "Adam"
        > user.age = 42
        > redbean.store(user)

        If a user with a given id already exists in the database, it will be updated.

        store() operation is idempotent.
        No exception will be thrown if a bean with a given ID already exists in the database.
        """
        return self._red_bean.store(bean)

    @_Guard.is_initialized
    def load(self, bean_type: str, bean_id: str | Id, throw_on_empty: bool = False) -> Bean:
        """
        Load/Read

        > user = redbean.load('user', user_id)
        If a bean with a given id does not exist in the database, it will be created by default.

        Optionally, it may be called with throw_on_empty=True
        to throw NotExistsError if a bean with a given id does not exist in the database.

        > from redbeanpython import NotExistsError
        > try:
        >    user = redbean.load('user', user_id, throw_on_empty=True)
        > except NotExistsError:
        >    ...
        """
        return self._red_bean.load(bean_type, bean_id, throw_on_empty=throw_on_empty)

    @property
    @_Guard.is_initialized
    def engine(self) -> sqlalchemy.engine.Engine:
        """
        Use redbean.engine to access the SQLAlchemy engine object.
        """
        return self._red_bean.engine

    @property
    @_Guard.is_initialized
    def session_maker(self) -> sqlalchemy.orm.sessionmaker:
        """
        Use redbean.session_maker to access the SQLAlchemy session maker object.

        It can be used for directly calling SQLAlchemy.

        F.e.:
        > session = redbean.session_maker() #
        > query = session.query(Customer, Invoice) #
        > query = query.filter(Customer.id == Invoice.customer_id)
        > query = query.filter(Invoice.amount > 10)
        > result = query.all()
        > for customer, invoice in result:
        >     print(customer.name, invoice.amount)
        """
        return self._red_bean.session_maker

    @_Guard.is_initialized
    def exists(self, bean_type: str, *, bean_id: Id | str) -> bool:
        """
        Checking the existence of a bean
        Existence can be checked with the exists method.

        > is_exists: bool = redbean.exists('user', bean_id=user_id)

        It can be safely run against not-existing (at that moment) bean types (tables).
        F.e.:
        > print(redbean.exists('not_existing_yet_in_database', bean_id="some_id"))
        """
        return self._red_bean.exists(bean_type, bean_id=bean_id)

    @_Guard.is_initialized
    def delete(self, *, bean: Bean = None, bean_type: str = None, bean_id: Id | str = None) -> None:
        """
        Delete

        We can delete loaded bean:
        > user = redbean.load('user', user_id)
        > redbean.delete(bean=user)

        or we can delete without loading bean via id and type:

        > redbean.delete(bean_type='user', bean_id=user_id)

        delete() operation is idempotent.
        No exception will be thrown if a bean with the given ID does not exist in the database.
        """
        self._red_bean.delete(bean=bean, bean_type=bean_type, bean_id=bean_id)

    @_Guard.is_initialized
    def count(self, bean_type: str, *, query: str = None, params: dict[str, Any] = None) -> int:
        """
        Counting

        Counting can be done by query and parameters with syntax consistent with SQLAlchemy.

        > count: int = redbean.count(
        >     'user',
        >     query="age > :age and active = :active",
        >     params={"age": 21, "active": True}
        > )

        > count: int = redbean.count('user')

        Count can be safely run against not-existing (at that moment) bean types (tables).

        > redbean.count('not_existing_yet_in_database')

        Alternative syntax

        If you do not want to use a text query with parameters, you can use SQLAlchemy. Hybrid mode.

        > with redbean.session_maker() as session:
        >     query = session.query(User)
        >     query = query.filter(User.age > 21)
        >     query = query.filter(User.active == True)
        >     count: int = query.count()
        """
        return self._red_bean.count(bean_type, query=query, params=params)

    @_Guard.is_initialized
    def find(
        self,
        bean_type: str,
        *,
        query: str = None,
        params: dict[str, Any] = None,
        order: str = None,
        limit: int = None,
        offset: int = None,
    ) -> Iterator[Bean]:
        """
        Finding

        The finding can be done by query and parameters with the syntax consistent with SQLAlchemy.

        > result: Iterator[Bean] = redbean.find(
        >     'user',
        >     query="age > :age and active = :active",
        >     params={"age": 21, "active": True},
        >     order="age desc",
        >     limit=10,
        >     offset=20,
        > )

        > result: Iterator[Bean] = redbean.find(
        >     'user',
        >     query="age > :age and active = :active",
        >     params={"age": 21, "active": True},
        > )

        > result: Iterator[Bean] = redbean.find('user')

        Find can be safely run against not existing (at that moment) bean types (tables).

        > print(list(redbean.find('not_existing_yet_in_database')))

        Alternative syntax

        If you do not want to use a text query with parameters, you can use SQLAlchemy.
        (Hybrid mode). The main difference is that the result object is list[Model], not Iterator[Bean].

        > with redbean.session_maker() as session:
        >     query = session.query(User)
        >     query = query.filter(User.age > 21)
        >     query = query.filter(User.active == True)
        >     query = query.order_by(User.age.desc())
        >     query = query.limit(10)
        >     query = query.offset(20)
        >     result: list[User] = query.all()
        >     for user in result:
        >         print(user.as_dict())
        """
        return self._red_bean.find(bean_type, query=query, params=params, order=order, limit=limit, offset=offset)

    @_Guard.is_initialized
    def dispense_many(self, bean_type: str, *, count: int = None, data: list[dict] = None) -> Iterator[Bean]:
        """
        Create many

        Use Beans() syntactic sugar notation to dispense many beans at once.

        > users = Beans('user', count=10) #

        > users = Beans('user', data=[{"name": "Adam"}, {"name": "Eve"}]) #

        An alternative syntax is to use dispense_many method

        > users = redbean.dispense_many('user', count=10) #

        > users = redbean.dispense_many('user', data=[{"name": "Adam"}, {"name": "Eve"}]) #
        """
        return self._red_bean.dispense_many(bean_type, count=count, data=data)

    @_Guard.is_initialized
    def load_many(self, bean_type: str, beans_ids: list[str | Id], *, throw_on_empty=False) -> Iterator[Bean]:
        """
        Load many

        To load many beans at once, use load_many method of the redbean object

        > users = redbean.load_many('user', [user_id_1, user_id_2, user_id_3])

        > users = redbean.load_many(
        >     'user',
        >     [user_id_1, user_id_2, user_id_3],
        >     throw_on_empty=True,
        > )

        load_many is a syntactic sugar only. It will not load records in bulk.
        It will be enough for most situations,
        but if you need to speed up loading many records at once, use Bulk operations.
        """
        return self._red_bean.load_many(bean_type, beans_ids, throw_on_empty=throw_on_empty)

    @_Guard.is_initialized
    def store_many(self, beans: list[Bean]) -> None:
        """
        Store  many

        > redbean.store_many(users)

        store_many is a syntactic sugar only. It will not store records in bulk.
        It will be enough for most situations,
        but if you need to speed up storing many records at once, use Bulk operations

        Bulk operations

        Bulk operations are designed to decrease the number of requests sent to databases.

        With many records to store or update, you should consider using bulk operations.

        Bulk operations are out of the scope of RedBeanPython by design, as if we have such use cases,
        hybrid mode and SQLAlchemy should be used directly in such places.

        Bulk store

        A bulk store is used to store many beans at once (with single request).

        > from sqlalchemy import insert
        > with redbean.session_maker() as session:
        >     session.execute(
        >          insert(User),
        >          [
        >              {"id": "a", "name": "Adam", "age": 42},
        >              {"id": "i", "name": "Ivona", "age": 42},
        >              {"id": "h", "name": "Hanna", "age": 10},
        >              {"id": "e", "name": "Eva", "age": 7},
        >          ],
        >     )
        >     session.commit()

        Bulk update

        A bulk update is used to update many beans at once (with a single request).

        > from sqlalchemy import update
        > with redbean.session_maker() as session:
        >     session.execute(
        >          update(User),
        >          [
        >              {"id": "a", "name": "Adam", "age": 43},
        >              {"id": "i", "name": "Ivona", "age": 43},
        >              {"id": "h", "name": "Hanna", "age": 11},
        >              {"id": "e", "name": "Eva", "age": 8},
        >          ],
        >     )
        >     session.commit()
        """
        return self._red_bean.store_many(beans)

    def _validate_persistent_setup(self, dsn: str, directory: str, namespace: str, frozen: bool) -> None:
        if self._initialized:
            if dsn != self._dsn:
                raise InitializationError(f"RedBean already initialized with other dsn: {self._dsn} != {dsn}")
            if directory != self._directory:
                raise InitializationError(
                    f"RedBean already initialized with other directory: "
                    f"{self._directory} != {directory}"
                )
            if namespace != self._namespace:
                raise InitializationError(
                    f"RedBean already initialized with other namespace: {self._namespace} != {namespace}"
                )
            if frozen != self._frozen:
                raise InitializationError(f"RedBean already initialized with other frozen: {frozen} != {self._frozen}")


r = redbean = Facade()
