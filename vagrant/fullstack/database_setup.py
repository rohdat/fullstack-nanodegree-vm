import sys
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
#from database_setup import Base, Restaurant, Menu

Base = declarative_base()

## CODE HERE

def test():
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	myFirstRestaurant = Restaurant(name = "Pizza Palace")
	session.add(myFirstRestaurant)
	session.commit()
	session.query(Restaurant).all()
	cheesepizza = MenuItem(name = "Cheese Pizza")

	session.query(MenuItem).all()
	firstResult = session.query(Restaurant).first()

class Restaurant(Base):
	__tablename__ = 'restaurant'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key=True)


class MenuItem(Base):
	__tablename__ = 'menu_item'
	name 		= Column(String(80),nullable=False)
	id 			= Column(Integer, primary_key=True)
	course 		= Column(String(250))
	description = Column(String(250))
	price 		= Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant 	= relationship(Restaurant)












## END OF FILE

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)