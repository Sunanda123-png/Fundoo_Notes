from core.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy import inspect


class Labels(Base):
    __tablename__ = "labels"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    name = Column(String(length=20))
    colour_field = Column(String(length=7))
    user_id = Column(BigInteger, ForeignKey('user.id'))
    user = relationship("User", back_populates='labels')

    def to_dict(self):
        return {x.key: getattr(self, x.key) for x in inspect(self).mapper.column_attrs}
