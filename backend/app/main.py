from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import database
from pydantic import BaseModel, validator  
from typing import List
from geoalchemy2.shape import to_shape
from shapely import wkt
from geoalchemy2 import Geometry
from sqlalchemy.sql import func
from shapely.geometry import Point 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from geoalchemy2.elements import WKTElement
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="server.log",  # Save logs to a file
    filemode="a"  # Append to the log file
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files from the 'static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the index.html file when accessing the root URL
@app.get("/")
async def root():
    return FileResponse("static/index.html")

# Pydantic model for Location response
class LocationBase(BaseModel):
    id: int
    name: str
    population: int
    elevation: float
    geom: str  

    class Config:
        orm_mode = True  # Tells Pydantic to work with SQLAlchemy models

    @validator("geom", pre=True)
    def convert_geom_to_wkt(cls, v):
        # Convert WKB (Well-Known Binary) to WKT (Well-Known Text)
        if v:
            try:
                # Convert WKB to WKT (Well-Known Text)
                return to_shape(v).wkt  # WKT conversion
            except Exception as e:
                raise ValueError(f"Error converting WKB to WKT: {e}")
        return v

@app.get("/locations", response_model=List[LocationBase])
def get_locations(db: Session = Depends(database.get_db)):
    logger.info("Fetcing function")
    return db.query(database.Location).all()




@app.post("/locations")
def create_location(location_data: dict, db: Session = Depends(database.get_db)):
    
    logger.info(f"Received location data: {location_data}")

    db_location = database.Location(
        name=location_data["name"],
        population=location_data["population"],
        elevation=location_data["elevation"],
        geom=WKTElement(location_data["geom"], srid=4326),  # The Geometry object from WKT
        country_id=1  # implement frontend later
    )

    logger.info("created db_location")

    db.add(db_location)
    db.commit()

    logger.info("added db_location")


    return db_location