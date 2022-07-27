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
from plugins.translation import Translation
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.regex('^/shel') & filters.text)
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
