from functools import wraps
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes

load_dotenv()
whitelist_env = os.getenv("OWNER_ID", "")
whitelist = [
    int(user_id)
    for user_id in whitelist_env.split(",")
    if user_id
]

def authorization(func):
    @wraps(func)
    async def authorization_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in whitelist:
            await update.message.reply_text("you thought you could just access my shit huh?")
            return None
        else:
            return await func(update, context)
    return authorization_handler