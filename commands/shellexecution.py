import subprocess
import logging
from telegram import Update
from telegram.ext import ContextTypes
from commands.decorator import authorization

logger = logging.getLogger(__name__)

SHELLSESSION = None

@authorization
async def shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SHELLSESSION

    if context.args[0] == "start":
        if SHELLSESSION is not None:
            await update.message.reply_text("A CMD shell already exists. Please send your command via /shell 'command' ")
        else:
            SHELLSESSION = subprocess.Popen(
                'cmd.exe /Q /D /k "whoami"',
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            await update.message.reply_text("A new CMD shell has been started! Please send your command via /shell 'command' ")
            logger.warning(f"{update.effective_user.full_name} Just started a new CMD shell session.")
    elif context.args[0] == "stop":
        if SHELLSESSION is None:
            await update.message.reply_text("CMD shell not detected.")
        else:
            SHELLSESSION.kill()
            SHELLSESSION = None
            await update.message.reply_text("CMD shell session process has been terminated.")
            logger.warning(f"{update.effective_user.full_name} Killed a CMD shell session")
    else:
        if SHELLSESSION is None:
            await update.message.reply_text("CMD shell doesn't exist, Please run /shell start")
        else:
            await update.message.reply_text("Running command...")
            command = " ".join(context.args)
            SHELLSESSION.stdin.write(command + "\n")
            logger.warning(f"{update.effective_user.full_name} Ran this command: {command}")
            SHELLSESSION.stdin.write("echo __ENDOFCOMMAND__\n")
            SHELLSESSION.stdin.flush()

            output = []
            while True:
                line = SHELLSESSION.stdout.readline()

                if "__ENDOFCOMMAND__" in line:
                    break

                output.append(line)

            await update.message.reply_text("\n".join(output))