from sqlalchemy.orm import declarative_base


class BaseModel:
    ...


Model = declarative_base(cls=BaseModel)
