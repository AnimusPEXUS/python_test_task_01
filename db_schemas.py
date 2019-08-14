
from sqlalchemy import Integer, String, Column, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_valid = Column(Boolean)


class Entity(Base):
    __tablename__ = 'entities'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Email(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer)
    email = Column(String)


class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer)
    phone = Column(String)
    is_mobile = Column(Boolean)


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer)
    name = Column(String)
    is_main = Column(Boolean)
    available_from = Column(DateTime)
    available_to = Column(DateTime)
