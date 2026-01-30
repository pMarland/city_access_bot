from sqlalchemy import ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from datetime import datetime
from app.database import Base

class TrackSession(Base):
    __tablename__ = "track_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    end_time: Mapped[datetime | None] = mapped_column(DateTime)

    geometry: Mapped[str | None] = mapped_column(
        Geometry("LINESTRING", srid=4326), nullable=True
    )
    length_m: Mapped[float | None] = mapped_column(Float)
    avg_speed_mps: Mapped[float | None] = mapped_column(Float)

    points = relationship(
        "TrackPoint",
        back_populates="session",
        cascade="all, delete-orphan"
    )


class TrackPoint(Base):
    __tablename__ = "track_points"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("track_sessions.id", ondelete="CASCADE"),
        index=True
    )

    geometry: Mapped[str] = mapped_column(
        Geometry("POINT", srid=4326)
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session = relationship("TrackSession", back_populates="points")
