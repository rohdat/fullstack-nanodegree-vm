import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine

Base = declarative_base()



class Shelter:
	__tablename__ = 'shelter'
	name = Column(String(88), nullable=False)
	address = Column(String(250))
	city = Column(String(88))
	state = Column(String(88))
	zipCode = Column(Integer)
	website = Column(String(100))
	id = Column(Integer, primary_key=True)



class Puppy:
	__tablename__ = 'puppy'
	name = Column(String(88), nullable=False)
	dob = Column(Date)
	gender = Column(String(1))
	weight = Column(Float)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	#shelter = relationship(Shelter)


engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)

