import asyncio
import time
import random
import os
from telethon import TelegramClient
from google import genai
from google.genai import types
from dotenv import load_dotenv

# .env faylidan kalitlarni yuklash (Lokal test uchun)
load_dotenv()

# SOZLAMALAR (Kalitlar endi tizim muhitidan olinadi)
BOT_TOKEN = os.getenv('BOT_TOKEN', '8861403359:AAG_MS2Jw40UAjbkfsd4lDIbyeW29KXy37k')
MY_CHANNEL = os.getenv('MY_CHANNEL', '@HAYRATLIOLAM') 
api_id = int(os.getenv('API_ID', '36724951'))
api_hash = os.getenv('API_HASH', '8115a28bf2d642a0062bb854e5cbebaf')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# KLIENTLARNI ISHGA TUSHIRISH (Proksi olib tashlandi)
client = TelegramClient('ai_bot_session', api_id, api_hash)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

MAVZULAR = [
    "chuqur okeanlar va dengiz maxluqlari",
    "qadimgi Misr, Rim yoki Yunoniston sirlari",
    "koinot, qora tuynuklar va uzoq sayyoralar",
    "inson miyasi va psixologiyasining yashirin imkoniyatlari",
    "g'ayrioddiy va kamyob o'simliklar hamda daraxtlar",
    "tarixdagi eng g'alati va qiziqarli voqealar",
    "mikroolam, atomlar va kvant fizikasi qiziqarli faktlari",
    "eng aqlli hayvonlar va ularning odatlari",
    "yer yuzidagi eng xavfli yoki eng chiroyli joylar",
    "kelajak texnologiyalari va sun'iy intellekt",
    "mashhur kashfiyotlar va ularning tasodifan yaratilishi",
    "inson ko'zi va hissiyotlarining g'aroyibotlari",
    "arxeologik topilmalar va yo'qolgan sivilizatsiyalar",
    "Sayyoramizdagi eng g'alati qonunlar va urf-odatlar",
    "tibbiyot va anatomiya sohasidagi aqlbovar qilmas faktlar"
]

async def generate_and_post_fact():
    tanlangan_mavzu = random.choice(MAVZULAR)
    
    for urinish in range(1, 6):
        try:
            prompt = (
                f"Siz 'Hayratli Olam' Telegram kanali uchun professional SMM ekspertisiz. "
                f"Iltimah, aynan shu yo'nalishda: [{tanlangan_mavzu}] haqida "
                f"odamlar mutlaqo bilmaydigan, eng hayratlanarli bitta haqiqiy faktni o'zbek tilida yozing. "
                f"Matn xuddi ona tili o'zbekcha bo'lgan insondek juda jozibali, mantiqan to'g'ri va ravon bo'lishi shart! "
                f"G'alati so'zma-so'z tarjimalar yoki soxta iboralardan umuman foydalanmang. "
                f"Post sarlavhasi qalin (bold) va juda jozibali bo'lsin. Emojilardan ko'p va to'g'ri foydalaning. "
                f"Oxirida mavzuga mos hashtaglar yozing. Matn o'rtacha qisqa va qiziqarli bo'lsin. "
                f"Hech qanday ortiqcha markdown (```) ishlatmang."
            )
            
            config = types.GenerateContentConfig(
                temperature=1.0,
                top_p=0.95
            )
            
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=config
            )
            fact_text = response.text
            
            await client.send_message(MY_CHANNEL, fact_text)
            print(f"[{time.strftime('%H:%M:%S')}] Yangi post joylandi! Mavzu: {tanlangan_mavzu}")
            return 
            
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Xatolik (qayta urinish {urinish}): {e}")
            await asyncio.sleep(30)

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Aqlli Telegram bot ishga tushdi...")
    
    while True:
        await generate_and_post_fact()
        await asyncio.sleep(7200)

if __name__ == '__main__':
    asyncio.run(main())
