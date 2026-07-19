import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackQueryHandler
from telegram.request import HTTPXRequest
from commands.ping import ping
from commands.shellexecution import shell
from commands.status import status, status_callback
from commands.screenshot import screenshot, watch, stopwatch
from commands.powermanagement import shutdown, shutdown_callback

load_dotenv()
token = os.getenv("TOKEN")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARN)
logger = logging.getLogger(__name__)

requests = HTTPXRequest(
        connect_timeout=300,
        read_timeout=300,
        write_timeout=300,
        pool_timeout=300
    )

application = Application.builder().token(token).request(requests).build()
logger.info(f"Running bot with {len(application.handlers)} handlers")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("wagwan me bredda")

def main():
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CallbackQueryHandler(status_callback))
    application.add_handler(CallbackQueryHandler(shutdown_callback))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("shell", shell))
    application.add_handler(CommandHandler("screenshot", screenshot))
    application.add_handler(CommandHandler("watch", watch))
    application.add_handler(CommandHandler("stopwatch", stopwatch))
    application.add_handler(CommandHandler("shutdown", shutdown))


    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()