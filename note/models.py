from core.db import Base
from sqlalchemy import Column, String, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import inspect


class Note(Base):
    __tablename__ = "note"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    title = Column(String(length=20))
    description = Column(String(length=100))
    is_archive = Column(Boolean, default=False)
    is_trash = Column(Boolean, default=False)
    reminder = Column(DateTime, nullable=True)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    user = relationship("User", back_populates="notes")

    def to_dict(self):
        return {x.key: getattr(self, x.key) for x in inspect(self).mapper.column_attrs}
