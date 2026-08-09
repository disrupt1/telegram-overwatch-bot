import logging
import psutil
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

def inlinebuttons() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("🧠 CPU", callback_data="get_cpu"),
            InlineKeyboardButton("🖥 RAM", callback_data="get_ram"),
            InlineKeyboardButton("💾 Disk", callback_data="get_disk")
        ],
        [InlineKeyboardButton("🔄 Update All", callback_data="get_all")],
    ]
    return InlineKeyboardMarkup(buttons)


def get_cpu() -> str:
    cpu = psutil.cpu_percent(interval=1)
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    return f"🧠 CPU Usage: {cpu}%\nNumber of cores: {cores}\nNumber of threads: {threads}"

def get_ram() -> str:
    ram = psutil.virtual_memory()
    used_gb = ram.used / (1024 ** 3)
    total_gb = ram.total / (1024 ** 3)
    free_mem = ram.available / (1024 ** 3)
    return f"🖥 RAM Usage: {used_gb:.1f}GB Out of {total_gb:.1f}GB\nAvailable memory: {free_mem:.1f}GB"

def get_disk() -> str:
    disk = psutil.disk_usage("/")
    used_disk = disk.used / (1024 ** 3)
    total_gb = disk.total / (1024 ** 3)
    free_gb = disk.free / (1024 ** 3)
    return f"💾 Current Disk Usage: {used_disk:.1f}GB Out of {total_gb:.1f}GB\nFree Space: {free_gb:.1f}GB"

def get_all() -> str:
    return "\n\n".join([get_cpu(), get_ram(), get_disk()])

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_all()
    await update.message.reply_text(text, reply_markup=inlinebuttons(), parse_mode="Markdown")

async def status_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = [
        InlineQueryResultArticle(
            id="1",
            title="Get the status of the computer",
            input_message_content=InputTextMessageContent(get_all())
        )
    ]
    await update.inline_query.answer(result)