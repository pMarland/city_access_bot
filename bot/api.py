import requests
from config import API_BASE_URL


def give_consent(telegram_id: int):
    return requests.post(f"{API_BASE_URL}/users/consent", json={
        "telegram_id": telegram_id
    })


def start_track(user_id: int):
    return requests.post(f"{API_BASE_URL}/tracks/start", params={
        "user_id": user_id
    }).json()


def add_point(session_id: int, lat: float, lon: float):
    return requests.post(f"{API_BASE_URL}/tracks/point", json={
        "session_id": session_id,
        "lat": lat,
        "lon": lon
    })


def finalize_track(session_id: int):
    return requests.post(f"{API_BASE_URL}/tracks/finalize", params={
        "session_id": session_id
    }).json()