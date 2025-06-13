from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters
from .search_agent import search_and_answer
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, None, workers=0)
app = FastAPI()

def handle_message(update: Update, _):
    text = update.message.text
    reply = search_and_answer(text)
    update.message.reply_text(reply)

dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.post(f"/webhook/{BOT_TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    dp.process_update(update)
    return {"ok": True}
