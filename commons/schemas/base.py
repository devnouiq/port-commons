
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.inspection import inspect


@as_declarative()
class Base:
    id = None

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_dict(self):
        """
        Convert the SQLAlchemy model instance into a dictionary.
        """
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        """
        Return a string representation of the SQLAlchemy model instance.
        """
        fields = ', '.join(f"{key}={value}" for key,
                           value in self.to_dict().items())
        return f"<{self.__class__.__name__}({fields})>"
