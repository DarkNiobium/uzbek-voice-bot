import os
import asyncio
import logging
from typing import Optional
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class GeminiTranscriber:
    """
    Google GenAI (Gemini 3.5 Flash Lite) orqali o'zbek tilidagi audio
    va ovozli xabarlarni matnga (transkripsiya) aylantirish klassi.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.5-flash-lite"):
        self.api_key = api_key
        self.model_name = model_name
        self._client: Optional[genai.Client] = None

    @property
    def client(self) -> genai.Client:
        if self._client is None:
            key = self.api_key or os.getenv("GEMINI_API_KEY", "").strip()
            if not key:
                raise ValueError("GEMINI_API_KEY ko'rsatilmagan! .env faylida GEMINI_API_KEY ni belgilang.")
            self._client = genai.Client(api_key=key)
        return self._client

    def _get_system_prompt(self, script: str = "latin") -> str:
        """
        O'zbek tili uchun moslashtirilgan transkripsiya ko'rsatmasi.
        """
        if script == "cyrillic":
            script_instruction = (
                "Matnni o'zbek kirill yozuvida (ўзбек кирилл алифбосида: ў, ғ, ш, ч, ҳ, х ва б.) yozing."
            )
        elif script == "auto":
            script_instruction = (
                "Gapiruvchi qaysi yozuvda tabiiy ko'rinsa yoki lotin alifbosida yozing."
            )
        else:  # latin default
            script_instruction = (
                "Matnni zamonaviy o'zbek lotin yozuvida (o'zbekcha lotin alifbosi: "
                "o‘, g‘, sh, ch, tutuq belgisi ') to'g'ri orfografiya bilan yozing."
            )

        return f"""Siz o'zbek tilidagi audio yozuvlarni yuqori aniqlikda matnga aylantiruvchi professional stenoqraf va transkribatorsiz.

VAZIFANGIZ:
Ushbu audio yozuvdagi barcha nutqni to'liq, so'zma-so'z o'zbek tilida matnga aylantiring (transkripsiya qiling).

QOIDALAR:
1. Alifbo: {script_instruction}
2. Nutqda ishlatilgan so'zlashuv iboralari, o'zbek lahjalari (shevalar) va o'zbek tiliga aralashgan ruscha/chet so'zlarni eshitilganidek to'g'ri aks ettiring.
3. Tinish belgilarini (nuqta, vergul, so'roq va undov belgilarini) hamda gap boshidagi katta harflarni joy-joyiga qo'ying.
4. Hech qanday qo'shimcha izoh, kirish so'zi, tarjima yoki xulosa yozmang (masalan: "Mana transkripsiya:", "Audioda aytildi:" kabi so'zlar bo'lmasin). Faqat audiodagi to'g'ridan-to'g'ri nutq matnini qaytaring.
5. Agar audioda nutq bo'lmasa, faqat shovqin bo'lsa yoki audio bo'sh bo'lsa, aniq shunday yozing: "[Nutq aniqlanmadi yoki audio tushunarsiz]".
"""

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        mime_type: str = "audio/ogg",
        script: str = "latin"
    ) -> str:
        """
        Audio baytlarini Gemini 3.5 Flash Lite ga yuborib matn oladi.
        """
        prompt = self._get_system_prompt(script=script)

        try:
            # google-genai async or to_thread call
            def _call_gemini():
                audio_part = types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type=mime_type,
                )
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[audio_part, prompt],
                    config=types.GenerateContentConfig(
                        temperature=0.1,  # past harorat aniq transkripsiya uchun
                    ),
                )
                return response.text

            # Run in thread pool to not block asyncio event loop
            transcription = await asyncio.to_thread(_call_gemini)
            if not transcription or not transcription.strip():
                return "[Nutq aniqlanmadi yoki audio bo'sh]"
            return transcription.strip()

        except Exception as e:
            logger.error(f"Gemini API xatoligi: {e}", exc_info=True)
            raise e
