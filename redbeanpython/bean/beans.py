from typing import Iterator, Callable

from redbeanpython.bean.bean import Bean
from redbeanpython.errors import IncorrectValueError


class DispenseMany:
    @staticmethod
    def dispense_many(bean_type: str, *, count: int = None, data: list[dict] = None) -> Iterator[Bean]:
        if data and count:
            raise IncorrectValueError("count and data cannot be provided at the same time")
        if data:
            try:
                for d in data:
                    yield Bean(bean_type, data=d)
                return
            except TypeError:
                raise IncorrectValueError("data must be iterable")
        if count:
            if not isinstance(count, int):
                raise IncorrectValueError("count must be integer")
            if count < 1:
                raise IncorrectValueError("count must be greater than 0")
            for _ in range(count):
                yield Bean(bean_type, data=data)
            return
        raise IncorrectValueError("count or data must be provided")


class BeansMetaclass(type, Callable):
    def __new__(cls, *args, **kwargs) -> Callable[[str], Iterator[Bean]]:
        return DispenseMany.dispense_many


class Beans(metaclass=BeansMetaclass):
    """
    Use `Beans()` syntactic sugar notation to dispense many beans at once.

    users = Beans('user', count=10) # (1)
    1. will dispense ten empty beans

    users = Beans('user', data=[{"name": "Adam"}, {"name": "Eve"}]) # (2)
    2. will dispense beans from the list of dict data
    """
