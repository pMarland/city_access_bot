from sqlalchemy import ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry
from datetime import datetime
from app.database import Base

class POI(Base):
    __tablename__ = "poi"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    geometry: Mapped[str] = mapped_column(
        Geometry("POINT", srid=4326)
    )
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
