import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import State, StatesGroup


from config import BOT_TOKEN
from api import give_consent, start_track, add_point, finalize_track
from keyboards import consent_keyboard, main_keyboard
from states import TrackState


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# --- /start ---
@dp.message(F.text == "/start")
async def start_cmd(message: Message):
    await message.answer(
        "Здравствуйте. Бот собирает геолокацию только с вашего согласия.",
        reply_markup=consent_keyboard()
    )


# --- consent ---
@dp.message(F.text == "Я согласен")
async def consent(message: Message):
    give_consent(message.from_user.id)
    await message.answer(
        "Согласие принято. Вы можете начать маршрут.",
        reply_markup=main_keyboard()
)


# --- start track ---
@dp.message(F.text == "Начать маршрут")
async def start_track_handler(message: Message, state: FSMContext):
    response = start_track(message.from_user.id)
    await state.set_state(TrackState.active)
    await state.update_data(session_id=response["id"])
    await message.answer("Маршрут начат. Включите трансляцию геолокации.")


# --- receive live location ---
@dp.message(F.location)
async def handle_location(message: Message, state: FSMContext):
    data = await state.get_data()
    if "session_id" not in data:
        return
    loc = message.location
    add_point(data["session_id"], loc.latitude, loc.longitude)


# --- stop track ---
@dp.message(F.text == "Завершить маршрут")
async def stop_track_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    if "session_id" not in data:
        await message.answer("Маршрут не активен")
        return
    result = finalize_track(data["session_id"])
    await state.clear()
    await message.answer(
        f"Маршрут завершён. Длина: {result['length_m']:.1f} м, "
        f"ср. скорость: {result['avg_speed_mps']:.2f} м/с"
    )


# --- POI: ожидание описания и фото ---
from aiogram.types import PhotoSize


class POIState(StatesGroup):
    waiting_location = State()
    waiting_description = State()
    waiting_photo = State()


@dp.message(F.text == "Добавить точку")
async def start_poi(message: Message, state: FSMContext):
    await state.set_state(POIState.waiting_location)
    await message.answer("Отправьте геометку точки интереса")


@dp.message(POIState.waiting_location, F.location)
async def poi_location(message: Message, state: FSMContext):
    await state.update_data(
        lat=message.location.latitude,
        lon=message.location.longitude
    )
    await state.set_state(POIState.waiting_description)
    await message.answer("Добавьте текстовое описание точки")


@dp.message(POIState.waiting_description, F.text)
async def poi_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(POIState.waiting_photo)
    await message.answer("Прикрепите фотографию точки (или напишите 'пропустить')")

@dp.message(POIState.waiting_photo, F.photo)
async def poi_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo: PhotoSize = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"


    import requests
    requests.post(
        f"{API_BASE_URL}/poi",
         json={
            "user_id": message.from_user.id,
            "lat": data["lat"],
            "lon": data["lon"],
            "description": data["description"],
             "photo_url": file_url
        }
    )
    await state.clear()
    await message.answer("Точка с фотографией сохранена")

@dp.message(POIState.waiting_photo, F.text.lower() == "пропустить")
async def poi_skip_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    import requests
    requests.post(
        f"{API_BASE_URL}/poi",
        json={
            "user_id": message.from_user.id,
            "lat": data["lat"],
            "lon": data["lon"],
            "description": data["description"]
        }
    )
    await state.clear()
    await message.answer("Точка сохранена без фотографии")

@dp.message(F.text == "/status")
async def status(message: Message):
    await message.answer("Бот активен. Вы можете записывать маршруты и точки интереса")

@dp.message(F.text == "/help")
async def help_cmd(message: Message):
    await message.answer(
        "Команды:"
        "Начать маршрут"
        "Завершить маршрут — окончание записи"
        "Добавить точку — POI с описанием"
    )

# --- entry point ---
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())