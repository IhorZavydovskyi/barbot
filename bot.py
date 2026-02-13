
import logging
import random
from datetime import datetime, time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8403382934:AAGyDrinBc_mjz0waMC7ph-MQ_RAO-kD6Pw"

# кто главный (сюда твой telegram id)
BOSS_ID = 000000000   # ← сюда вставлю потом

workers = ["Антон", "Даня", "Володя", "Пан Роман"]

START_WORK = time(10, 0)
LATE_AFTER = time(10, 5)
END_WORK = time(23, 0)

# хранение смен
active = {}
stats = {}

logging.basicConfig(level=logging.INFO)

late_phrases = [
    "Ты опоздал. Это уже стиль жизни.",
    "Время: ты его проиграл.",
    "Бар работает. Ты — нет.",
    "Опоздание зафиксировано. Самоуважение нет.",
    "Сегодня снова позор."
]

ok_phrases = [
    "О, пришёл вовремя. Бывает.",
    "Сегодня без позора. Удивительно.",
    "Записал. Работай.",
]

exit_phrases = [
    "Свободен. Бар выжил.",
    "Иди отдыхай. Завтра попробуй не облажаться.",
    "Смена закрыта.",
]

def late_minutes(now):
    start = datetime.combine(datetime.today(), LATE_AFTER)
    cur = datetime.combine(datetime.today(), now)
    diff = (cur - start).total_seconds() / 60
    return int(diff)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Система контроля бара активна.\n"
        "Сканируй QR:\n"
        "Приход: Имя\n"
        "Уход: Имя"
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    now = datetime.now().time()

    # ПРИХОД
    if text.startswith("Приход:"):
        name = text.replace("Приход:", "").strip()

        if name not in workers:
            await update.message.reply_text("Ты кто вообще?")
            return

        active[name] = datetime.now()

        if now > LATE_AFTER:
            late = late_minutes(now)
            stats.setdefault(name, {"late":0,"hours":0})
            stats[name]["late"] += late

            await update.message.reply_text(
                f"{name}, {random.choice(late_phrases)}\n"
                f"Опоздание: {late} мин"
            )

            # сообщение тебе
            if BOSS_ID != 0:
                await context.bot.send_message(
                    BOSS_ID,
                    f"🚨 {name} опоздал на {late} мин"
                )

        else:
            await update.message.reply_text(f"{name}, {random.choice(ok_phrases)}")

    # УХОД
    elif text.startswith("Уход:"):
        name = text.replace("Уход:", "").strip()

        if name not in workers:
            await update.message.reply_text("Ты кто вообще?")
            return

        if name not in active:
            await update.message.reply_text("Ты даже не работал сегодня.")
            return

        start_time = active[name]
        end_time = datetime.now()
        worked = (end_time - start_time).total_seconds() / 3600

        stats.setdefault(name, {"late":0,"hours":0})
        stats[name]["hours"] += worked

        del active[name]

        await update.message.reply_text(
            f"{name}, {random.choice(exit_phrases)}\n"
            f"Отработал: {round(worked,2)} ч"
        )

# ОТЧЁТ ДЛЯ БОССА
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOSS_ID:
        return

    text = "📊 Отчёт бара:\n\n"

    for w,data in stats.items():
        text += f"{w}\n"
        text += f"Часы: {round(data['hours'],2)}\n"
        text += f"Опоздания: {data['late']} мин\n\n"

    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("report", report))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("BAR CONTROL AI STARTED")
app.run_polling()
