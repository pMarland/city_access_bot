from fastapi import FastAPI
from app.routers import users, tracks,  export # подключаем media
from app.routers import poi as poi_router
from app.database import engine
#from app.models import user, track, media
from app.routers import media as media_router
from app.database import Base

def on_startup():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="GeoBot API")

# Подключаем все роутеры
app.include_router(users.router)
app.include_router(tracks.router)
app.include_router(poi_router.router)
app.include_router(export.router)
app.include_router(media_router.router)  # новый роутер
