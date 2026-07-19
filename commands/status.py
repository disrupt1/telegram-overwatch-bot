import asyncio
import logging
import psutil
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
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

async def status_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
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