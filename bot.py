import asyncio
from aiogram import Bot, Dispatcher, types
from datetime import datetime

TOKEN = "8403382934:AAGyDrinBc_mjz0waMC7ph-MQ_RAO-kD6Pw"
GROUP_ID = -1000  # сюда вставим id группы позже

bot = Bot(token=TOKEN)
dp = Dispatcher()

# база смен (пока простая в памяти)
shifts = {}

# список барменов (добавим)
staff = {
    1015564310: "Игорь",
    111111111: "Антон",
    222222222: "Даня",
    333333333: "Володя",
}

# время смены
SHIFT_START = 10
SHIFT_END = 23

@dp.message()
async def scan_handler(message: types.Message):
    user_id = message.from_user.id

    if user_id not in staff:
        await message.answer("❌ Ты не в списке барменов")
        return

    name = staff[user_id]
    now = datetime.now()

    # если бармен уже на смене = это уход
    if user_id in shifts:
        start_time = shifts[user_id]
        worked = now - start_time
        hours = worked.seconds // 3600
        mins = (worked.seconds % 3600) // 60

        text = (
            f"🔴 {name} ушёл со смены\n"
            f"Отработал: {hours}ч {mins}м"
        )

        await bot.send_message(GROUP_ID, text)
        del shifts[user_id]
        return

    # это приход
    shifts[user_id] = now

    status = "🟢 вовремя"
    if now.hour > SHIFT_START or (now.hour == SHIFT_START and now.minute > 5):
        status = "🔴 ОПОЗДАЛ"

    text = (
        f"🟢 {name} пришёл на смену\n"
        f"Время: {now.strftime('%H:%M')}\n"
        f"Статус: {status}"
    )

    await bot.send_message(GROUP_ID, text)
    await message.answer("Смена зафиксирована")

async def main():
    print("Бар-бот запущен 🍸")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
