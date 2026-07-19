from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def button_shutdown() -> InlineKeyboardMarkup:
    buttonss = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data="confirm_shut"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_shut")
        ]
    ]
    return InlineKeyboardMarkup(buttonss)

def button_restart() -> InlineKeyboardMarkup:
    buttonss = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data="confirm_restart"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_restart")
        ]
    ]
    return InlineKeyboardMarkup(buttonss)

def button_lock() -> InlineKeyboardMarkup:
    buttonss = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data="confirm_lock"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_lock")
        ]
    ]
    return InlineKeyboardMarkup(buttonss)

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Are you sure you want to shutdown the computer?", reply_markup=button_shutdown())

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Are you sure you want to restart the computer?", reply_markup=button_restart())

async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Are you sure you want to lock the computer?", reply_markup=button_lock())