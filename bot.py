from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime

TOKEN = "8403382934:AAGyDrinBc_mjz0waMC7ph-MQ_RAO-kD6Pw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Барный контролёр активирован.")

async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    now = datetime.now().strftime("%H:%M")

    await update.message.reply_text(
        f"🚨 {user} отмечен в {now}\n"
        f"Если ты опоздал — бар это запомнит."
    )

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    now = datetime.now().strftime("%H:%M")

    await update.message.reply_text(
        f"🍺 {user} ушёл в {now}\n"
        f"Бар выжил. Смена закрыта."
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("in", checkin))
app.add_handler(CommandHandler("out", checkout))

print("Бот запущен...")
app.run_polling()
