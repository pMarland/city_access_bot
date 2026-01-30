from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.dependencies.db import get_db

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/poi/geojson")
def export_poi_geojson(db: Session = Depends(get_db)):
    return db.execute(text("""
        SELECT jsonb_build_object(
            'type','FeatureCollection',
            'features',jsonb_agg(feature)
        )
        FROM (
            SELECT jsonb_build_object(
                'type','Feature',
                'geometry',ST_AsGeoJSON(geometry)::jsonb,
                'properties',jsonb_build_object(
                    'id',id,
                    'description',description
                )
            ) AS feature
            FROM poi
        ) f;
    """)).scalar()
