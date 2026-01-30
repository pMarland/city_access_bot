from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from datetime import datetime

from app.dependencies.db import get_db
from app.models.track import TrackSession, TrackPoint
from app.schemas.track import TrackPointSchema
from app.services.gis import build_linestring, track_length_m, avg_speed_mps

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.post("/start")
def start_track(user_id: int, db: Session = Depends(get_db)):
    session = TrackSession(user_id=user_id)
    db.add(session)
    db.flush()
    return {"session_id": session.id}

@router.post("/point")
def add_point(data: TrackPointSchema, db: Session = Depends(get_db)):
    geom = from_shape(Point(data.lon, data.lat), srid=4326)
    point = TrackPoint(session_id=data.session_id, geometry=geom)
    db.add(point)
    return {"status": "ok"}

@router.post("/finalize")
def finalize_track(session_id: int, db: Session = Depends(get_db)):
    session = db.get(TrackSession, session_id)
    if not session:
        raise HTTPException(404, "Track session not found")

    session.geometry = build_linestring(db, session_id)
    session.length_m = track_length_m(db, session_id)
    session.avg_speed_mps = avg_speed_mps(db, session_id)
    session.end_time = datetime.utcnow()

    return {
        "session_id": session.id,
        "length_m": session.length_m,
        "avg_speed_mps": session.avg_speed_mps
    }
