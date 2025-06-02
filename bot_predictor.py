from aiogram import Bot, Dispatcher, types, executor
import logging
import joblib
from datetime import datetime
import pandas as pd
from predict_weather import predict_weather
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

news_model = joblib.load("news_category_model.joblib")
usd_model, usd_start_date = joblib.load("usd_model.joblib")

user_mode = {}

def predict_category(text: str) -> str:
    return news_model.predict([text])[0]

def predict_usd(date_str: str) -> float:
    try:
        target_date = pd.to_datetime(date_str.strip(), format="%Y-%m-%d")
        days = (target_date - usd_start_date).days
        df = pd.DataFrame({"days_since_start": [days]})
        predicted = usd_model.predict(df)[0]
        return round(predicted, 2)
    except Exception as e:
        print("Xatolik:", e)
        return None

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        "Yangilik toifasini aniqlash",
        "USD kursini bashorat qilish",
        "Harorat bashorati"
    )
    await message.answer("Xush kelibsiz!\nQuyidagi funksiyalardan birini tanlang:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text in [
    "Yangilik toifasini aniqlash",
    "USD kursini bashorat qilish",
    "Harorat bashorati"
])
async def handle_choice(message: types.Message):
    chat_id = message.chat.id
    user_mode[chat_id] = message.text
    if message.text == "Yangilik toifasini aniqlash":
        await message.answer("Yangilik matnini yuboring:")
    elif message.text == "USD kursini bashorat qilish":
        await message.answer("USD kursini bashorat qilish uchun sanani yuboring (yyyy-mm-dd formatda):")
    elif message.text == "Harorat bashorati":
        await message.answer("Haroratni bashorat qilish uchun sanani yuboring (yyyy-mm-dd formatda):")


@dp.message_handler()
async def handle_input(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in user_mode:
        await message.answer("Iltimos, /start tugmasini bosing va xizmatni tanlang.")
        return

    mode = user_mode[chat_id]
    user_input = message.text.strip()

    if mode == "Yangilik toifasini aniqlash":
        if len(user_input) < 20:
            await message.answer("Matn juda qisqa. To'liq yangilik matnini yuboring.")
            return
        category = predict_category(user_input)
        await message.answer(f"Taxminiy turkum: *{category}*", parse_mode="Markdown")

    elif mode == "USD kursini bashorat qilish":
        result = predict_usd(user_input)
        if result is None:
            await message.answer("Sana noto'g'ri formatda. Masalan: 2025-07-01")
        else:
            await message.answer(f"{user_input} uchun bashorat qilingan USD kursi: *{result}*", parse_mode="Markdown")

    elif mode == "Harorat bashorati":
        result = predict_weather(user_input)
        if result is None:
            await message.answer("Sana noto'g'ri formatda. Masalan: 2025-07-01")
        else:
            await message.answer(f"{user_input} uchun taxminiy harorat: *{result} °C*", parse_mode="Markdown")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
