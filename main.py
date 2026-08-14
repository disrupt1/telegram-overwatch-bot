import logging
import os
import ctypes
import subprocess
from dotenv import load_dotenv
import ctypes
from httpx import PoolTimeout
from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackQueryHandler, InlineQueryHandler
from telegram.request import HTTPXRequest
from commands.ping import ping
from commands.shellexecution import shell
from commands.status import status, get_ram, get_disk, get_all, get_cpu, inlinebuttons, status_inline
from commands.screenshot import screenshot, watch, stopwatch
from commands.powermanagement import lock, restart, shutdown

load_dotenv()
token = os.getenv("TOKEN")
api_base = os.getenv("BOT_API_BASE")

thread_hold = 0x80000000
thread_sleep = 0x00000001
thread_display = 0x00000002

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARN)
logger = logging.getLogger(__name__)

requests = HTTPXRequest(
        connect_timeout=300,
        read_timeout=300,
        write_timeout=300,
        pool_timeout=300
    )

builder = Application.builder().request(requests).token(token)

if api_base:
    builder.base_url(api_base)

application = builder.build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("wagwan me bredda")

async def keepawake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Please specifiy with on or off if you want to keep the computer awake.\ne.g /keepawake on OR /keepawake off")
    elif len(context.args) > 1:
        await update.message.reply_text("Please specifiy with on or off if you want to keep the computer awake.\ne.g /keepawake on OR /keepawake off")

    if len(context.args) == 1:
        if context.args[0].lower() == "on":
            try:
                ctypes.windll.kernel32.SetThreadExecutionState(thread_hold | thread_sleep | thread_display)
                print("turned on keepawake")
            except Exception as e:
                print("some shit went wrong")
                print(e)
            await update.message.reply_text("Keep awake has been turned on. The computer screen will not turn off nor go into sleep.")
        elif context.args[0].lower() == "off":
            ctypes.windll.kernel32.SetThreadExecutionState(thread_hold)
            await update.message.reply_text("Keep awake has been turned off. Note that if the computer screen turns off or goes into sleep you will no longer be able to monitor your system.")
        else:
            await update.message.reply_text("Please specifiy with on or off if you want to keep the computer awake.\ne.g /keepawake on OR /keepawake off")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_cpu":
        await query.edit_message_text(text=get_cpu(), reply_markup=inlinebuttons())
    elif query.data == "get_ram":
        await query.edit_message_text(text=get_ram(), reply_markup=inlinebuttons())
    elif query.data == "get_disk":
        await query.edit_message_text(text=get_disk(), reply_markup=inlinebuttons())
    elif query.data == "get_all":
        await query.edit_message_text(text=get_all(), reply_markup=inlinebuttons())

    if query.data == "confirm_shut":
        await query.edit_message_text("The computer will shutdown momentarily...")
        subprocess.run(
            "shutdown /s /f"
        )
    elif query.data == "cancel_shut":
        await query.edit_message_text("Aborted operation.")
    if query.data == "confirm_restart":
            await query.edit_message_text("The computer will reboot momentarily...")
            subprocess.run(
                "shutdown /r /f"
            )
    elif query.data == "cancel_restart":
        await query.edit_message_text("Aborted operation.")
    if query.data == "confirm_lock":
            await query.edit_message_text("The computer will lock down momentarily...")
            ctypes.windll.user32.LockWorkStation()
    elif query.data == "cancel_lock":
        await query.edit_message_text("Aborted operation.")

def main():
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(InlineQueryHandler(status_inline))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("shell", shell))
    application.add_handler(CommandHandler("screenshot", screenshot))
    application.add_handler(CommandHandler("watch", watch))
    application.add_handler(CommandHandler("stopwatch", stopwatch))
    application.add_handler(CommandHandler("shutdown", shutdown))
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("lock", lock))
    application.add_handler(CommandHandler("keepawake", keepawake))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()