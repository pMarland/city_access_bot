from pydantic import BaseModel

class POISchema(BaseModel):
    user_id: int
    lat: float
    lon: float
    description: str
