from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.config import settings
import os
from pathlib import Path
from datetime import datetime
import shutil

from app.dependencies.db import get_db
from app.core.config import settings
from app.models.media import Media
from app.models.user import User
from app.models.poi import POI

router = APIRouter(prefix="/media", tags=["Media"])

# --- Папка для хранения файлов ---
Path(settings.MEDIA_DIR).mkdir(parents=True, exist_ok=True)

# ------------------------------
# Загрузка файла
# ------------------------------
@router.post("/upload")
def upload_file(
    user_id: int,
    poi_id: int | None = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Проверяем существование пользователя
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Если указан POI, проверяем его
    if poi_id:
        poi = db.get(POI, poi_id)
        if not poi:
            raise HTTPException(404, "POI not found")
    else:
        poi = None

    # Генерируем уникальное имя файла
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{user_id}_{timestamp}_{file.filename}"
    file_path = os.path.join(settings.MEDIA_DIR, filename)

    # Сохраняем файл
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Определяем тип файла
    ext = file.filename.split(".")[-1].lower()
    if ext in ("jpg", "jpeg", "png", "gif"):
        file_type = "image"
    elif ext in ("mp4", "mov", "avi"):
        file_type = "video"
    elif ext in ("gpx", "kml"):
        file_type = "gpx"
    else:
        file_type = "other"

    # Создаём запись в БД
    media = Media(
        user_id=user_id,
        poi_id=poi_id,
        file_path=file_path,
        file_type=file_type
    )
    db.add(media)
    db.flush()  # чтобы получить media.id

    return {"media_id": media.id, "file_type": file_type, "path": file_path}


# ------------------------------
# Получение файла
# ------------------------------
@router.get("/{media_id}")
def get_media(media_id: int, db: Session = Depends(get_db)):
    media = db.get(Media, media_id)
    if not media:
        raise HTTPException(404, "Media not found")
    if not os.path.exists(media.file_path):
        raise HTTPException(404, "File not found on server")
    return FileResponse(media.file_path, filename=os.path.basename(media.file_path))
