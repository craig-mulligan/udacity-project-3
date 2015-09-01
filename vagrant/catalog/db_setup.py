from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
'''
Declare models used in sqlalchemy
'''

class User(Base):
    #User model saves FB info
    __tablename__='user'

    id=Column(Integer, primary_key=True)
    name=Column(String(250), nullable=False)
    email=Column(String(250), nullable=False)
    picture=Column(String(250), nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'id': self.id
        }

class Category(Base):
    # Basic model for classifying items
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    # each category is associated with creator
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'user': self.user_id
        }

class Item(Base):
    # a simple store of name and description, grouped by category
    __tablename__='item'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(5000), nullable=False)
    # each item is associated with category
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    # each item is associated with creator
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'user': self.user_id,
            'category': self.category_id
        }

engine=create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)