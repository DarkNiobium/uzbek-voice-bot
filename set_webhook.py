import sys
import asyncio
from aiogram import Bot
from config import BOT_TOKEN

async def main():
    if not BOT_TOKEN:
        print("[XATO] BOT_TOKEN topilmadi! .env fayliga bot tokenini kiriting.")
        return

    bot = Bot(token=BOT_TOKEN)

    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip("/")
    else:
        base_url = input("Vercel domeningizni kiriting (masalan: https://my-bot.vercel.app): ").strip().rstrip("/")

    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"

    webhook_url = f"{base_url}/api/webhook"
    print(f"Webhook o'rnatilmoqda: {webhook_url} ...")

    try:
        success = await bot.set_webhook(
            url=webhook_url,
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )
        info = await bot.get_webhook_info()
        print(f"\n[NATIJA] Webhook muvaffaqiyatli o'rnatildi: {success}")
        print(f"Hozirgi Webhook URL: {info.url}")
        print(f"Kutilayotgan xabarlar soni: {info.pending_update_count}")
    except Exception as e:
        print(f"[XATOLIK] Webhookni o'rnatib bo'lmadi: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
