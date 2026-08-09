import time
from telegram import Update
from telegram.ext import ContextTypes

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    starts = time.perf_counter()
    message = await update.message.reply_text("which bomboclatt dog i am")
    end = time.perf_counter()
    latency = (end - starts) * 1000
    await message.edit_text(f"Bot latency in milliseconds: {latency:.1f}ms")