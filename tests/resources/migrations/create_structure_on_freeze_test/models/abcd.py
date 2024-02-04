from sqlalchemy import Column, String, Text

from redbeanpython.model.model import Model


class Abcd(Model):
    """
    Do not change content of this file.
    It is generated automatically.
    It will be overwritten on next schema change (in "fluid" mode).
    If you need to extend this model, please use inheritance.

    SQLAlchemy model for bean: test.
    """

    __tablename__ = 'abcd'
    __table_args__ = {'extend_existing': True}

    id = Column(String(255), primary_key=True)
    name = Column(Text, nullable=True)

    def __json__(self):
        return self.as_dict()

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
