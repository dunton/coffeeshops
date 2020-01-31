# Set up the database #

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """Table of Users"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return {
           'id': self.id,
           'name': self.name,
           'email': self.email,
           'picture': self.picture
        }


class CoffeeShop(Base):
    """Coffee Shops"""
    __tablename__ = 'CoffeeShop'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serialized format"""
        return {
            'name': self.name,
            'id': self.id
        }


class MenuItem(Base):
    """Items served at the CoffeeShop"""
    __tablename__ = 'MenuItem'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    coffeeshop_id = Column(Integer, ForeignKey('CoffeeShop.id'))
    coffeeshop = relationship(CoffeeShop)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Returns object data in easily serialized format"""
        return {
           'name': self.name,
           'id': self.id,
           'description': self.description,
           'price': self.price

        }

############# insert at end of file #############

def create_database(database_url):
  engine = create_engine(database_url)
  Base.metadata.create_all(engine)
  print "Database created"

		
		
