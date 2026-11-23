import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import logging
from typing import Optional
from fastapi import FastAPI, Request, Response
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, GEMINI_MODEL
from handlers import main_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vercel_bot")

app = FastAPI(title="Telegram Voice Transcriber (Gemini 3.5 Flash Lite)")

_bot: Optional[Bot] = None

def get_bot() -> Bot:
    global _bot
    if _bot is None:
        if not BOT_TOKEN:
            raise ValueError("BOT_TOKEN o'rnatilmagan! Vercel Environment Variables ga BOT_TOKEN ni kiriting.")
        _bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
        )
    return _bot

dp = Dispatcher()
dp.include_router(main_router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Telegram Uzbek Voice Transcriber Bot",
        "engine": "Gemini 3.5 Flash Lite",
        "model": GEMINI_MODEL,
        "instructions": "Vercel Webhook: /api/webhook. O'rnatish uchun: /api/set_webhook"
    }

@app.post("/api/webhook")
@app.post("/webhook")
@app.post("/")
async def telegram_webhook(request: Request):
    try:
        current_bot = get_bot()
        data = await request.json()
        update = types.Update(**data)
        await dp.feed_update(bot=current_bot, update=update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Webhook processing error: {e}", exc_info=True)
        return Response(content=str(e), status_code=500)

@app.get("/api/set_webhook")
@app.get("/set_webhook")
async def set_webhook_endpoint(request: Request):
    try:
        current_bot = get_bot()
    except Exception as e:
        return {"error": str(e)}

    host = request.headers.get("x-forwarded-host") or request.headers.get("host")
    proto = request.headers.get("x-forwarded-proto", "https")
    webhook_url = f"{proto}://{host}/api/webhook"

    success = await current_bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"]
    )
    info = await current_bot.get_webhook_info()

    return {
        "success": success,
        "webhook_url": webhook_url,
        "pending_updates": info.pending_update_count,
        "message": "Webhook muvaffaqiyatli o'rnatildi! Endi bot Telegramda ishlaydi."
    }

@app.get("/api/delete_webhook")
@app.get("/delete_webhook")
async def delete_webhook_endpoint():
    try:
        current_bot = get_bot()
        success = await current_bot.delete_webhook(drop_pending_updates=True)
        return {
            "success": success,
            "message": "Webhook o'chirildi. Endi botni lokal kompyuterda ishlatish mumkin."
        }
    except Exception as e:
        return {"error": str(e)}
