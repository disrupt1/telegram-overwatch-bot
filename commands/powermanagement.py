import subprocess

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def buttons() -> InlineKeyboardMarkup:
    buttonss = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel")
        ]
    ]
    return InlineKeyboardMarkup(buttonss)

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Are you sure you want to shutdown the computer?", reply_markup=buttons())

async def shutdown_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "confirm":
        await query.edit_message_text("The computer will shutdown momentarily...")
        subprocess.run(
            "shutdown /s /f"
        )
    elif query.data == "cancel":
        await query.edit_message_text("Aborted operation.")