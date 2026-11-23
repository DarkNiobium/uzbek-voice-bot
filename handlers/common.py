from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from config import DEFAULT_SCRIPT

router = Router()

# Foydalanuvchilar tanlagan yozuv turini saqlash (oddiy in-memory xotira)
# user_id -> "latin" | "cyrillic" | "auto"
user_scripts = {}

def get_user_script(user_id: int) -> str:
    return user_scripts.get(user_id, DEFAULT_SCRIPT)

def get_settings_keyboard(current_script: str) -> InlineKeyboardMarkup:
    latin_mark = "✅ " if current_script == "latin" else ""
    cyrillic_mark = "✅ " if current_script == "cyrillic" else ""
    auto_mark = "✅ " if current_script == "auto" else ""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{latin_mark}🇺🇿 Lotin alifbosi (O‘zbekcha)",
                callback_data="set_script:latin"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"{cyrillic_mark}🇺🇿 Кирилл алифбоси (Ўзбекча)",
                callback_data="set_script:cyrillic"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"{auto_mark}⚡ Avtomatik / Asl holatda",
                callback_data="set_script:auto"
            )
        ]
    ])
    return keyboard

@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "🇺🇿 **Assalomu alaykum!**\n\n"
        "Men **Google Gemini 3.5 Flash Lite** asosida ishlovchi aqlli transkripsiya botiman.\n\n"
        "🎙 Menga istalgan **ovozli xabar (voice)**, **audio fayl** yoki **dumaloq video (video note)** yuboring, "
        "men uni tez va aniq matnga aylantirib beraman!\n\n"
        "⚙️ Yozuv turini (Lotin / Kirill) o'zgartirish uchun: /settings\n"
        "ℹ️ Yordam uchun: /help\n\n"
        "───\n"
        "🇷🇺 Отправьте мне голосовое сообщение или аудиофайл на узбекском языке, "
        "и я переведу его в текст с помощью нейросети **Gemini 3.5 Flash Lite**!"
    )
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📖 **Botdan foydalanish bo'yicha qo'llanma:**\n\n"
        "1. Menga shunchaki ovozli xabar (audio/voice) yuboring yoki boshqa chatdan forward qiling.\n"
        "2. Bot bir necha soniya ichida Gemini 3.5 Flash Lite orqali audio tarkibini to'liq matnga aylantirib qaytaradi.\n"
        "3. O'zbek tili lahjalari, so'zlashuv tili va aralashgan iboralar to'g'ri inobatga olinadi.\n\n"
        "📌 **Buyruqlar:**\n"
        "• /settings — Alifbo turini tanlash (Lotin yoki Kirill)\n"
        "• /help — Ushbu yordam oynasi"
    )
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("settings"))
async def cmd_settings(message: Message):
    current = get_user_script(message.from_user.id)
    text = (
        "⚙️ **Transkripsiya yozuv turini tanlang:**\n\n"
        f"Hozirgi tanlov: **{current.capitalize()}**\n\n"
        "Ovozli xabarlarni qaysi alifboda olishni xohlaysiz?"
    )
    await message.answer(text, reply_markup=get_settings_keyboard(current), parse_mode="Markdown")

@router.callback_query(F.data.startswith("set_script:"))
async def cb_set_script(callback: CallbackQuery):
    script_choice = callback.data.split(":")[1]
    user_scripts[callback.from_user.id] = script_choice

    script_names = {
        "latin": "Lotin alifbosi (O‘zbekcha)",
        "cyrillic": "Кирилл алифбоси (Ўзбекча)",
        "auto": "Avtomatik"
    }

    await callback.answer(f"Tanlandi: {script_names.get(script_choice, script_choice)}")
    await callback.message.edit_text(
        f"✅ Yozuv turi o'zgartirildi: **{script_names.get(script_choice, script_choice)}**\n\n"
        "Endi menga ovozli xabar yuborishingiz mumkin!",
        reply_markup=get_settings_keyboard(script_choice),
        parse_mode="Markdown"
    )
