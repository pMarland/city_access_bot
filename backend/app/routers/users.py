from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.models.user import User
from app.schemas.user import ConsentSchema

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/consent")
def give_consent(data: ConsentSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(telegram_id=data.telegram_id).first()
    if not user:
        user = User(telegram_id=data.telegram_id, consent_given=True)
        db.add(user)
    else:
        user.consent_given = True
    return {"status": "consent_given"}
