from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "user"

    index = Column(Integer, primary_key=True)
    id = Column(String)
    password = Column(String)

class Talklist(Base):
    __tablename__ = "talklist"

    index = Column(Integer, primary_key = True)
    id = Column(String)
    user = Column(String)
    talk = Column(String)
    time = Column(String)
    oppo = Column(String)
    owner_index = Column(Integer, ForeignKey("user.index", ondelete="CASCADE"))
    owner = relationship("User")

class Friendlist(Base):
    __tablename__ = "friendlist"

    index = Column(Integer, primary_key = True)
    id = Column(String)
    owner_index = Column(Integer, ForeignKey("user.index", ondelete="CASCADE"))
    owner = relationship("User")