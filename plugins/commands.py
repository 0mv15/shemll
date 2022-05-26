import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


import os
import time
import psutil
import shutil
import string
import asyncio
from subprocess import run
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from plugins.config import Config
from plugins.translation import Translation
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.database.add import add_user_to_database
from functions.forcesub import handle_force_subscribe

@Client.on_message(filters.command(["start"]) & filters.private)
async def start(bot, update):
    if not update.from_user:
        return await update.reply_text("I don't know about you sar :(")
    await add_user_to_database(bot, update)
    await bot.send_message(
        Config.LOG_CHANNEL,
           f"#NEW_USER: \n\nNew User [{update.from_user.first_name}](tg://user?id={update.from_user.id}) started @{Config.BOT_USERNAME} !!"
    )
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, update)
      if fsub == 400:
        return
    await update.reply_text(
        text=Translation.START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=Translation.START_BUTTONS
    )

@Client.on_message(filters.regex('^/sh') & filters.text)
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
        
@Client.on_message(filters.regex('^/tgup') & filters.text)
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
