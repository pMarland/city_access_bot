from pydantic import BaseModel

class ConsentSchema(BaseModel):
    telegram_id: int
