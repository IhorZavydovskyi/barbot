import json
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = "8403382934:AAGyDrinBc_mjz0waMC7ph-MQ_RAO-kD6Pw"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

START_WORK = 10
LATE_MINUTES = 5

# ===== база барменов =====
try:
    with open("barmen.json", "r", encoding="utf-8") as f:
        barmen = json.load(f)
except:
    barmen = {}

def save():
    with open("barmen.json", "w", encoding="utf-8") as f:
        json.dump(barmen, f, ensure_ascii=False, indent=2)

# ===== кнопки =====
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("Я пришёл"))
kb.add(KeyboardButton("Я ушёл"))
kb.add(KeyboardButton("Статус"))

# ===== старт =====
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    uid = str(msg.from_user.id)

    if uid not in barmen:
        barmen[uid] = {
            "name": msg.from_user.first_name,
            "start": None
        }
        save()
        await msg.answer(f"{msg.from_user.first_name} добавлен в систему 🍸", reply_markup=kb)
    else:
        await msg.answer("Ты уже в системе", reply_markup=kb)

# ===== пришёл =====
@dp.message_handler(lambda m: m.text == "Я пришёл")
async def arrived(msg: types.Message):
    uid = str(msg.from_user.id)

    if uid not in barmen:
        await msg.answer("Напиши /start сначала")
        return

    now = datetime.now()
    barmen[uid]["start"] = now.strftime("%H:%M")
    save()

    # проверка опоздания
    if now.hour > START_WORK or (now.hour == START_WORK and now.minute > LATE_MINUTES):
        await msg.answer("ТЫ ОПОЗДАЛ. ШТРАФ — 1 КГ СТЫДА 😈")
    else:
        await msg.answer("Красавчик. Вовремя пришёл 🫡")

# ===== ушёл =====
@dp.message_handler(lambda m: m.text == "Я ушёл")
async def left(msg: types.Message):
    uid = str(msg.from_user.id)

    if uid not in barmen or not barmen[uid]["start"]:
        await msg.answer("Ты даже не отмечался сегодня 🤡")
        return

    start_time = datetime.strptime(barmen[uid]["start"], "%H:%M")
    now = datetime.now()
    worked = now - start_time

    hours = worked.seconds // 3600
    minutes = (worked.seconds % 3600) // 60

    barmen[uid]["start"] = None
    save()

    await msg.answer(f"Смена закрыта\nОтработал: {hours}ч {minutes}мин")

# ===== статус =====
@dp.message_handler(lambda m: m.text == "Статус")
async def status(msg: types.Message):
    uid = str(msg.from_user.id)

    if uid not in barmen:
        await msg.answer("Ты не зарегистрирован")
        return

    start = barmen[uid]["start"]

    if start:
        await msg.answer(f"Ты на смене с {start}")
    else:
        await msg.answer("Ты сейчас не на смене")

# ===== запуск =====
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

