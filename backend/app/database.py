from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from geoalchemy2 import Geometry

DATABASE_URL = "postgresql://myuser:mypassword@db:5432/geodb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    population = Column(Integer)
    elevation = Column(Float)
    geom = Column(Geometry('POINT', srid=4326))  # PostGIS geometry type
    #country_id = Column(Integer) 
    country_id = Column(Integer, ForeignKey('country.id'))  # Assuming you have a Country model

    # Relationship to the Country model (if needed)
    country = relationship("Country", back_populates="locations")


class Country(Base):
    __tablename__ = "country"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True)


Country.locations = relationship("Location", back_populates="country")

Base.metadata.create_all(bind=engine)
