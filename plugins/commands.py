# (c) PMV

from pyrogram import Client, idle
from config import Config
from utils import *
from pyrogram import filters
import pyrogram
from pyrogram.types import Message
import time
import os
import shlex
import datetime
import pytz
import asyncio
import re
import shutil
import psutil
import logging

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
PMVBot = Client(name="PMVPyroBot", bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)
# Bot stats
BOT_UPSTATE = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%y %I:%M:%S %p")
BOT_START_TIME = time.time()
# i think we cant change the value in class
AUTH_USERS = Config.AUTH_USERS


async def auth_check(_, __, m):
    global AUTH_USERS
    return m.chat.id in AUTH_USERS

static_auth_filter = filters.create(auth_check)

@PMVBot.on_message(filters.command("auth") & filters.user(Config.OWNER_ID))
async def tg_auth_Handler(bot: PMVBot, message: Message):
    global AUTH_USERS
    if message.reply_to_message:
         AUTH_USERS.append(message.reply_to_message.from_user.id)
         await message.reply_text(f"Now {message.reply_to_message.from_user.name} can use me")
    else:
        try:
            input_str = message.text.split(" ", 1)[1]
            AUTH_USERS.append(input_str)
            await message.reply_text(f"Id {input_str} now can use me")
        except:
            await message.reply_text("send along with I'd or reply to user msg")

@PMVBot.on_message(filters.command("unauth") & filters.user(Config.OWNER_ID))
async def tg_unauth_Handler(bot: PMVBot, message: Message):
    global AUTH_USERS
    if message.reply_to_message:
         AUTH_USERS.remove(message.reply_to_message.from_user.id)
         await message.reply_text(f"Now {message.reply_to_message.from_user.name} can not use me")
    else:
        try:
            input_str = message.text.split(" ", 1)[1]
            AUTH_USERS.remove(input_str)
            await message.reply_text(f"Id {input_str} now can not use me")
        except:
            await message.reply_text("send along with I'd or reply to user msg")

@PMVBot.on_message(filters.command(["logs", "log"]) & filters.user(Config.OWNER_ID))
async def tg_unauth_Handler(bot: PMVBot, message: Message):
    if os.path.exists("log.txt"):
        await message.reply_document("log.txt")
        return

@PMVBot.on_message(filters.command(["status", "status"]) & static_auth_filter)
async def status_msg(bot, update):
  currentTime = time.strftime("%H:%M:%S", time.gmtime(time.time() - BOT_START_TIME)) 
  total, used, free = shutil.disk_usage(".")
  total, used, free = humanbytes(total), humanbytes(used), humanbytes(free)
  cpu_usage = psutil.cpu_percent()
  ram_usage = f"{humanbytes(psutil.virtual_memory().used)}/{humanbytes(psutil.virtual_memory().total)}"
  msg = f"**Bot Current Status**\n\n**Bot Uptime:** {currentTime} \n\n**Total disk space:** {total} \n**Used:** {used} \n**Free:** {free} \n**CPU Usage:** {cpu_usage}% \n**RAM Usage:** {ram_usage}\n**Restarted on** `{BOT_UPSTATE}`"
  await update.reply_text(msg, quote=True)

@PMVBot.on_message(filters.regex('^/tgup') & filters.text)
async def tgupload(bot, update):
    msg = update.text.split(' ', 1)
    if len(msg) == 1:
        await update.reply_text(text='no filename')
        return
    filename = msg[1]
    if os.path.exists(filename):
        pass
    else:
        await update.reply_text(text="no such file")
        return
    proc = await update.reply_text(text="uploading")
    await bot.send_document(
        chat_id=update.chat.id,
        document=filename,
        #thumb="thumb.jpg",
        caption=f"<b>{filename}</b>")
    await proc.edit_text(text="uploaded 😊")

@PMVBot.on_message(filters.regex('^/sh1') & filters.text)
async def shell(bot, update):
    cmd = update.text.split(' ', 1)
    if len(cmd) == 1:
        await update.reply_text(text='no cmd 🙇‍♂️')
        return
    cmd = cmd[1]
    process = run(cmd, capture_output=True, shell=True)
    reply = ''
    stderr = process.stderr.decode('utf-8')
    stdout = process.stdout.decode('utf-8')
    if len(stdout) != 0:
        reply += f"*Stdout*\n<code>{stdout}</code>\n"
        logger.info(f"Shell - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"*Stderr*\n<code>{stderr}</code>\n"
        logger.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('shell_output.txt', 'w') as file:
            file.write(reply)
        with open('shell_output.txt', 'rb') as doc:
            await update.reply_document(
                "shell_output.txt",
                True,
                caption="shell output"
            )
    elif len(reply) != 0:
        await update.reply_text(text=reply)
    else:
        await update.reply_text(text='No reply')

PMVBot.start()
print("----@PMV15----")
print("------Bot Started------")
idle()
print("------Bot Stopped------")
PMVBot.stop()</code>
