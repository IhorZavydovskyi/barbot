import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import datetime

TOKEN = "8403382934:AAGyDrinBc_mjz0waMC7ph-MQ_RAO-kD6Pw"

logging.basicConfig(level=logging.INFO)

# время начала смены
WORK_TIME = datetime.time(10, 0)

# допустимое опоздание (минут)
WARNING_DELAY = 2
HARD_DELAY = 5

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Барный контроль активирован. Сканируй QR и не позорься.")

async def handle_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    now = datetime.datetime.now().time()

    delay_minutes = (datetime.datetime.combine(datetime.date.today(), now) -
                     datetime.datetime.combine(datetime.date.today(), WORK_TIME)).total_seconds() / 60

    if delay_minutes <= WARNING_DELAY:
        await update.message.reply_text(f"{user} пришёл вовремя. Невероятно. Даже уважение появилось.")
    elif WARNING_DELAY < delay_minutes < HARD_DELAY:
        await update.message.reply_text(f"{user}, ты почти опоздал. Еще чуть-чуть и был бы позором бара.")
    else:
        await update.message.reply_text(
            f"{user} ОПЯТЬ ОПОЗДАЛ 🤡\n"
            f"Бар уже работает, гости пьют, а ты где был?\n"
            f"Соберись. Ты бармен, а не декорация."
        )

async def off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"{user} ушёл с работы. Надеюсь не бухать за углом.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("off", off))

    # любое сообщение = отметка прихода (QR)
    app.add_handler(MessageHandler(filters.TEXT, handle_qr))

    print("BOT STARTED")
    app.run_polling()

if __name__ == "__main__":
    main()
