import io
import logging
from aiogram import Router, F, Bot
from aiogram.enums import ChatAction, ChatType
from aiogram.types import Message
from aiogram.filters import Command
from gemini_transcriber import GeminiTranscriber
from config import GEMINI_API_KEY, GEMINI_MODEL
from utils.text_splitter import split_text
from .common import get_user_script

logger = logging.getLogger(__name__)
router = Router()

transcriber = GeminiTranscriber(api_key=GEMINI_API_KEY, model_name=GEMINI_MODEL)

async def process_and_reply_transcription(target_message: Message, bot: Bot, trigger_message: Message = None):
    """
    Ovozli yoki audio xabarni yuklab olib, Gemini 3.5 Flash Lite
    orqali matnga aylantiradi va javob qaytaradi.
    """
    if trigger_message is None:
        trigger_message = target_message

    if not GEMINI_API_KEY:
        await trigger_message.reply(
            "⚠️ **Xatolik:** Gemini API kaliti o'rnatilmagan!\n"
            "Administrator `.env` faylida `GEMINI_API_KEY` ni ko'rsatishi zarur.",
            parse_mode="Markdown"
        )
        return

    is_group = target_message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
    sender_name = target_message.from_user.first_name if target_message.from_user else "Foydalanuvchi"

    # Status: Guruhda yoki shaxsiyda "yozmoqda..." holati
    await bot.send_chat_action(chat_id=target_message.chat.id, action=ChatAction.TYPING)
    
    status_text = (
        f"⏳ *{sender_name} ning ovozli xabari matnga aylantirilmoqda...*"
        if is_group
        else "⏳ *Ovozli xabar tinglanmoqda va matnga aylantirilmoqda...*"
    )
    status_msg = await trigger_message.reply(status_text, parse_mode="Markdown")

    file_id = None
    mime_type = "audio/ogg"

    if target_message.voice:
        file_id = target_message.voice.file_id
        mime_type = target_message.voice.mime_type or "audio/ogg"
    elif target_message.audio:
        file_id = target_message.audio.file_id
        mime_type = target_message.audio.mime_type or "audio/mpeg"
    elif target_message.video_note:
        file_id = target_message.video_note.file_id
        mime_type = "video/mp4"
    else:
        await status_msg.edit_text("❌ Bu xabarda audio yoki ovozli yozuv topilmadi.")
        return

    try:
        # Faylni xotiraga yuklab olish
        file_info = await bot.get_file(file_id)
        file_bytes_io = io.BytesIO()
        await bot.download_file(file_info.file_path, destination=file_bytes_io)
        audio_bytes = file_bytes_io.getvalue()

        # Tanlangan yozuv turi (Lotin / Kirill)
        user_script = get_user_script(target_message.from_user.id if target_message.from_user else 0)

        # Gemini 3.5 Flash Lite orqali transkripsiya
        transcription = await transcriber.transcribe_audio(
            audio_bytes=audio_bytes,
            mime_type=mime_type,
            script=user_script
        )

        if is_group:
            header = f"🗣️ **{sender_name}:**\n\n"
        else:
            header = "📝 **Transkripsiya:**\n\n"

        full_text = f"{header}{transcription}"
        chunks = split_text(full_text, max_chunk_size=4000)

        # Status xabarini yangilaymiz
        await status_msg.edit_text(chunks[0], parse_mode="Markdown")

        # Agar xabar 4000 belgidan uzun bo'lsa, qolgan qismlarini yuboramiz
        for extra_chunk in chunks[1:]:
            await target_message.reply(extra_chunk, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Transkripsiyada xatolik: {e}", exc_info=True)
        err_text = (
            "❌ **Transkripsiyada xatolik yuz berdi:**\n"
            f"`{str(e)[:250]}`"
        )
        try:
            await status_msg.edit_text(err_text, parse_mode="Markdown")
        except Exception:
            await trigger_message.reply(err_text, parse_mode="Markdown")

# 1. To'g'ridan-to'g'ri ovozli yoki audio xabar kelganda (shaxsiy chatda yoki guruhda)
@router.message(F.voice | F.audio | F.video_note)
async def handle_direct_audio(message: Message, bot: Bot):
    await process_and_reply_transcription(target_message=message, bot=bot)

# 2. Guruhda eski ovozli xabarga reply qilib /transcribe yoki /matn yozilganda
@router.message(Command("transcribe", "matn", "t"))
async def handle_reply_command(message: Message, bot: Bot):
    if not message.reply_to_message:
        await message.reply(
            "ℹ️ Ushbu buyruqni biron-bir **ovozli xabarga javob (reply)** qilib yuboring.",
            parse_mode="Markdown"
        )
        return

    replied = message.reply_to_message
    if replied.voice or replied.audio or replied.video_note:
        await process_and_reply_transcription(target_message=replied, bot=bot, trigger_message=message)
    else:
        await message.reply("⚠️ Siz javob bergan xabar ovozli xabar yoki audio emas!")
