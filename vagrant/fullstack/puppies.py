from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import func
import logging
Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximumCapacity = Column(Integer)
    currentCapacity = Column(Integer)


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))


# class PuppyProfile(Base):
#     __tablename__ = 'profile'
#     website = Column(String(250), nullable=False, ForeignKey('shelter.website'))
#     description = Column(String(250), nullable = False)
#     shelter = relationship(Shelter)
#     special_needs = Column(String(250))

def checkIn (pup, session):
    shelters = session.query(Shelter).order_by(Shelter.zipCode)
    p = pup
    for s in shelters:
        if s.id == p.shelter_id:
            if s.currentCapacity >= s.maximumCapacity:
                
                logging.error ("Shelter is at capacity. Try shelter_id " )
            else:
                s.currentCapacity = s.currentCapacity - 1
                session.add(p)
                session.commit()
                print "Puppy checked in"




engine = create_engine('sqlite:///puppyshelter.db')
 

Base.metadata.create_all(engine)

experiments = """
puppies = session.query(Puppy).order_by(Puppy.name)
for p in puppies:
    print p.name
today = datetime.date.today()
sixMonthsAgo = 30*6
oldestPuppy = today - datetime.timedelta(days=sixMonthsAgo)
puppies = session.query(Puppy).order_by(Puppy.dateOfBirth).filter(Puppy.dateOfBirth <= oldestPuppy)
puppies_grouped_by_shelter = session.query(func.count(Puppy.shelter_id), Puppy.shelter_id).group_by(Puppy.shelter_id)

"""