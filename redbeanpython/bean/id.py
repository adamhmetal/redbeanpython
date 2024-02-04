import uuid


class Id(str):
    """
    Id is a string that is used to identify a bean.

    - have to be proper identifiers.
        (It can contain only letters, digits, and underscores and can not start with a digit.)
    - have to be snake_case.
    - must not start with an underscore.
    """
    @classmethod
    def next_id(cls):
        return cls(uuid.uuid4())
