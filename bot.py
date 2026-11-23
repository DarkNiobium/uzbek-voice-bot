import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, GEMINI_MODEL
from handlers import main_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("uzbek_voice_bot")

async def main():
    if not BOT_TOKEN:
        logger.error("XATOLIK: BOT_TOKEN aniqlanmadi! .env fayliga Telegram bot tokenini kiriting.")
        return

    logger.info(f"Bot ishga tushirilmoqda... Model: {GEMINI_MODEL}")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher()
    dp.include_router(main_router)

    # Oldingi o'qilmagan xabarlarni tozalash (drop pending updates)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot tayyor! Ovozli xabarlar kutilyapti...")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
