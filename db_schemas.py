
from sqlalchemy import Integer, String, Column, Boolean, DateTime


class Message:
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_valid =Column(Boolean)

class Entity:
    __tablename__ = 'entities'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Email:
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer)
    email = Column(String)


class Phone:
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer)
    phone = Column(String)
    is_mobile = Column(Boolean)


class Service:
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer)
    name = Column(String)
    is_main = Column(Boolean)
    available_from = Column(DateTime)
    available_to = Column(DateTime)
