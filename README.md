# 🎙️ Telegram Voice Transcriber Bot (O'zbek tili / Gemini 3.5 Flash Lite)

Ushbu Telegram bot o'zbek tilidagi barcha turdagi ovozli xabarlarni (**voice**), audio fayllarni (**audio**) va dumaloq video xabarlarni (**video note**) yuqori aniqlikda matnga (transkripsiya) aylantirib beradi.

Loyiha eng zamonaviy **Google Gemini 3.5 Flash Lite** modeliga asoslangan bo'lib, quyidagi 2 xil usulda ishlashga to'liq moslashtirilgan:
1. **Lokal kompyuterda (Long Polling)** — `run.bat` yoki `python bot.py` orqali.
2. **Vercel bulutli serverida (Serverless Webhook)** — bepul va 24/7 rejimida.

---

## ❓ Muhim savollar va Telegram imkoniyatlari

### 1. Inline rejimda birovning ovozli xabariga javoban chaqirish mumkinmi?
> **Texnik javob:** Telegram Bot API arxitekturasi tufayli **Inline rejimda (@bot) boshqa odamning ovozli xabarini o'qib bo'lmaydi.**
> 
> *Nima uchun?*
> Foydalanuvchi chatda `@botname` yozganda, Telegram botga faqatgina kiritilgan matnni (`query`) yuboradi. Telegram xavfsizlik qoidalariga ko'ra, inline rejimga chatdagi mavjud xabarlar yoki siz reply qilgan audio fayllar berilmaydi.

### 2. Guruhlarda ishlash (Eng qulay yechim!)
Bot guruhlarda a'zolar tashlagan har qanday ovozli xabarni avtomatik tutib olib, unga reply tarzida darhol matnli transkripsiyani qaytaradi!

**Guruhda ishlashi uchun muhim sozlama:**
1. Telegramda [@BotFather](https://t.me/BotFather) ga kiring.
2. `/mybots` -> Botingizni tanlang -> `Bot Settings` -> `Group Privacy`.
3. **Turn off** tugmasini bosing (*Privacy mode disabled* bo'lishi kerak).
   *(Bu botga guruhdagi barcha ovozli xabarlarni ko'rish va avtomatik matnga aylantirish imkonini beradi).*
4. Botni guruhingizga qo'shing.
5. Endi kimdir guruhga ovozli xabar yuborsa, bot darhol uni kim yuborganini ko'rsatib, matnini chiqarib beradi!
6. Shuningdek, avval yuborilgan ovozli xabarga reply qilib `/transcribe` yoki `/matn` deb yozsangiz ham bot uni matnga aylantiradi.

---

## 🚀 Vercel ga bepul 24/7 joylashtirish (Deploy)

Loyiha Vercel Serverless arxitekturasiga (`FastAPI` + `aiogram webhook`) to'liq moslashtirilgan.

### 1-qadam: GitHub ga yuklash
Loyihani o'zingizning GitHub akkauntingizga push qiling:
```bash
git init
git add .
git commit -m "Initial commit for Vercel"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main
```

### 2-qadam: Vercel ga ulash
1. [vercel.com](https://vercel.com) saytiga kiring.
2. **Add New Project** tugmasini bosing va GitHub repositoriyangizni import qiling.
3. **Environment Variables** bo'limida quyidagi o'zgaruvchilarni kiriting:
   - `BOT_TOKEN` = Sizning Telegram Bot tokeningiz ([@BotFather](https://t.me/BotFather))
   - `GEMINI_API_KEY` = Google Gemini API kalitingiz ([Google AI Studio](https://aistudio.google.com/))
   - `GEMINI_MODEL` = `gemini-3.5-flash-lite`
   - `DEFAULT_SCRIPT` = `latin` (yoki `cyrillic`)
4. **Deploy** tugmasini bosing. Vercel sizga domen beradi (masalan: `https://uzbek-voice-bot.vercel.app`).

### 3-qadam: Webhookni faollashtirish (Bir marta bosish bilan)
Deploy tugagach, brauzeringizda quyidagi manzilni oching:
```
https://SIZNING-DOMEN.vercel.app/api/set_webhook
```
Ekranda `{"success": true, "message": "Webhook muvaffaqiyatli o'rnatildi!"}` yozuvi chiqadi.

Yoki terminal orqali:
```bash
python set_webhook.py https://SIZNING-DOMEN.vercel.app
```
Bo'ldi! Bot Vercel da 24/7 rejimida mutlaqo bepul ishlaydi.

---

## 💻 Kompyuterda lokal ishga tushirish (Long Polling)

Agar Vercel sizga kerak bo'lmasa yoki avval kompyuteringizda sinab ko'rmoqchi bo'lsangiz:

1. `.env` fayliga `BOT_TOKEN` va `GEMINI_API_KEY` ni kiriting.
2. [run.bat](run.bat) faylini ikki marta bosing (Windows).
3. Yoki terminalda:
```powershell
cd C:\Users\User\uzbek_voice_bot
.\venv\Scripts\activate
python bot.py
```

*(Eslatma: agar bot avval Vercel webhookiga ulangan bo'lsa, lokal polling ishlashi uchun brauzerda `/api/delete_webhook` manzilini oching yoki bot.py uni avtomatik tozalaydi).*

---

## 📁 Loyiha Tuzilishi

```
uzbek_voice_bot/
│
├── api/
│   └── index.py            # Vercel serverless webhook handleri (FastAPI)
├── handlers/
│   ├── __init__.py         # Routerlar yig'indisi
│   ├── common.py           # /start, /help, /settings buyruqlari
│   └── voice.py            # Ovozli xabarlar, audio va guruhdagi xabarlar
├── utils/
│   ├── __init__.py
│   └── text_splitter.py    # 4000 belgidan oshgan matnlarni to'g'ri bo'lish
├── config.py               # Sozlamalar
├── gemini_transcriber.py   # Gemini 3.5 Flash Lite integratsiyasi
├── bot.py                  # Lokal kompyuterda ishga tushirish fayli
├── set_webhook.py          # Webhookni Vercel ga ulash skripti
├── vercel.json             # Vercel marshrutlash konfiguratsiyasi
├── requirements.txt        # Kerakli Python paketlari
├── run.bat                 # Windows tezkor start
└── .env                    # Maxfiy kalitlar
```
