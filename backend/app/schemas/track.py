from pydantic import BaseModel

class TrackPointSchema(BaseModel):
    session_id: int
    lat: float
    lon: float

