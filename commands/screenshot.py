import os
import time
import mss
import logging
from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image
from commands.decorator import authorization

logger = logging.getLogger(__name__)

@authorization
async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching screenshot from system...")

    mss.mss().shot(output="screenshot.png")
    try:
        readableshit = time.ctime()
        with open("screenshot.png", "rb") as img:
            await update.message.reply_photo(img, caption=readableshit)
            img.close()
    except Exception as e:
        logger.error(e)
    finally:
        os.remove("screenshot.png")

async def watchjob(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.data["chatid"]

    mss.mss().shot(output="screenshot.png")
    try:
        current_time = time.ctime()
        new_img = Image.open("screenshot.png")
        new_img.save(
            "screenshot.jpg",
            format="JPEG",
            quality=80,
            optimize=True
        )
        new_img.close()
        with open("screenshot.jpg", "rb") as img:
            await context.bot.send_photo(chat_id=chat_id, photo=img, caption=current_time)
            img.close()
    except Exception as e:
        logger.error(e)
        await context.bot.send_message(chat_id=chat_id, text="An error occurred. check logs")

@authorization
async def watch(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Please enter the interval (in seconds) of which you want to receive your screenshots at.\ne.g /watch 10")
    elif len(context.args) == 1:
        job_name = context.job_queue.get_jobs_by_name("watcher")
        if not job_name:
            frequency = float(context.args[0])
            chatid = update.effective_user.id

            dataset = {
                "chatid": chatid
            }

            context.job_queue.run_repeating(
                watchjob,
                interval=frequency,
                first=0,
                data=dataset,
                name="watcher"
            )

            await update.message.reply_text(f"You will now receive a screenshot from your computer every {frequency} seconds.\nTo stop this watcher job run /stopwatch")
        else:
            await update.message.reply_text("A watcher job is already running! To stop the previous watcher run /stopwatch")
    else:
        await update.message.reply_text("Please enter the interval (in seconds) of which you want to receive your screenshots at.\ne.g /watch 10")

async def stopwatch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    watcher_job = context.job_queue.get_jobs_by_name("watcher")
    if not watcher_job:
        await update.message.reply_text("No watcher job is running, run /watch [seconds]")
    else:
        origmsg = await update.message.reply_text("Stopping system watcher...")
        for job in watcher_job:
            job.schedule_removal()
        os.remove("screenshot.png")
        os.remove("screenshot.jpg")
        await origmsg.edit_text("System watcher has now been stopped!")