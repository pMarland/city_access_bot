from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from app.dependencies.db import get_db
from app.models.poi import POI
from app.schemas.poi import POISchema

router = APIRouter(prefix="/poi", tags=["POI"])

@router.post("")
def create_poi(data: POISchema, db: Session = Depends(get_db)):
    geom = from_shape(Point(data.lon, data.lat), srid=4326)
    poi = POI(
        user_id=data.user_id,
        geometry=geom,
        description=data.description
    )
    db.add(poi)
    db.flush()
    return {"id": poi.id}

@router.get("/")
def get_poi():
    return []