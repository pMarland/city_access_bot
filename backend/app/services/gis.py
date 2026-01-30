from sqlalchemy.orm import Session
from sqlalchemy import text

def build_linestring(db: Session, session_id: int):
    return db.execute(text("""
        SELECT ST_MakeLine(geometry ORDER BY timestamp)
        FROM track_points
        WHERE session_id = :sid
    """), {"sid": session_id}).scalar()

def track_length_m(db: Session, session_id: int) -> float:
    return db.execute(text("""
        SELECT ST_Length(
            ST_Transform(
                ST_MakeLine(geometry ORDER BY timestamp),
                3857
            )
        )
        FROM track_points
        WHERE session_id = :sid
    """), {"sid": session_id}).scalar() or 0.0

def avg_speed_mps(db: Session, session_id: int) -> float:
    return db.execute(text("""
        SELECT
            ST_Length(
                ST_Transform(
                    ST_MakeLine(geometry ORDER BY timestamp),
                    3857
                )
            ) /
            NULLIF(EXTRACT(EPOCH FROM (MAX(timestamp) - MIN(timestamp))), 0)
        FROM track_points
        WHERE session_id = :sid
    """), {"sid": session_id}).scalar() or 0.0
