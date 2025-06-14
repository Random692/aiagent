from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from .search_agent import search_and_answer
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = FastAPI()

# Setup Telegram bot
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

@telegram_app.message_handler(filters.TEXT & ~filters.COMMAND)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    reply = search_and_answer(query)
    await update.message.reply_text(reply)

# Start Telegram polling in a background task
@app.on_event("startup")
async def startup():
    import asyncio
    asyncio.create_task(telegram_app.run_polling())
