from sqlalchemy import Column, ${", ".join(sqlalchemy_types)}

from redbeanpython import Model


class ${model_name}(Model):
    """
    ! Do not change content of this file.
    ! It is generated automatically.
    ! It will be overwritten on next schema change (in "fluid" mode).
    ! If you need to extend this model, please use inheritance.

    SQLAlchemy model for bean: ${table_name}.
    """

    __tablename__ = '${table_name}'
    __table_args__ = {'extend_existing': True}

    % for column_name, column in columns.items():
    ${column_name} = ${column.alchemy_definition}
    % endfor

    def __json__(self):
        return self.as_dict()

    def as_dict(self):
        return {
            % for column_name in columns.keys():
            '${column_name}': self.${column_name},
            % endfor
        }
