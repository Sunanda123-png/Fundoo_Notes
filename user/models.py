from core.db import Base
from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
# from note.models import collaborator
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    username = Column(String, unique=True)
    firstname = Column(String(length=20))
    lastname = Column(String(length=20))
    password = Column(String(length=250))
    email = Column(String(length=30))
    phone = Column(BigInteger)
    location = Column(String(length=30))
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    notes = relationship("Note", back_populates="user")
    labels = relationship("Labels", back_populates="user")
    notes_m2m = relationship("Note", secondary="collaborator")

    def __str__(self):
        return f"{self.username}"

    def set_password(self, password):
        self.password = pwd_context.hash(password)
