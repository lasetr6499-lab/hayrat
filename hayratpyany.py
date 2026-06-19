import asyncio
import time
import random
import os
from telethon import TelegramClient
from google import genai
from google.genai import types
from dotenv import load_dotenv
from aiohttp import web  # Render uyg'oq turishi uchun veb-server

load_dotenv()

# SOZLAMALAR
BOT_TOKEN = os.getenv('BOT_TOKEN', '******************')
MY_CHANNEL = os.getenv('MY_CHANNEL', '***********M') 
api_id = int(os.getenv('API_ID', '********1'))
api_hash = os.getenv('API_HASH', '***********')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = TelegramClient('ai_bot_session', api_id, api_hash)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

MAVZULAR = [
    "chuqur okeanlar va dengiz maxluqlari", "qadimgi Misr, Rim yoki Yunoniston sirlari",
    "koinot, qora tuynuklar va uzoq sayyoralar", "inson miyasi va psixologiyasining yashirin imkoniyatlari",
    "g'ayrioddiy va kamyob o'simliklar hamda daraxtlar", "tarixdagi eng g'alati va qiziqarli voqealar",
    "mikroolam, atomlar va kvant fizikasi qiziqarli faktlari", "eng aqlli hayvonlar va ularning odatlari",
    "yer yuzidagi eng xavfli yoki eng chiroyli joylar", "kelajak texnologiyalari va sun'iy intellekt",
    "mashhur kashfiyotlar va ularning tasodifan yaratilishi", "inson ko'zi va hissiyotlarining g'aroyibotlari",
    "arxeologik topilmalar va yo'qolgan sivilizatsiyalar", "Sayyoramizdagi eng g'alati qonunlar va urf-odatlar",
    "tibbiyot va anatomiya sohasidagi aqlbovar qilmas faktlar"
]

# Render uchun soxta sahifa (Ping kelganda 200 OK qaytaradi)
async def handle(request):
    return web.Response(text="Bot ishlamoqda va uyg'oq!")

async def start_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render avtomatik ravishda PORT muhitini taqdim etadi
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Veb-server {port}-portda ishga tushdi.")

async def generate_and_post_fact():
    tanlangan_mavzu = random.choice(MAVZULAR)
    for urinish in range(1, 6):
        try:
            prompt = (
                f"Siz 'Hayratli Olam' Telegram kanali uchun professional SMM ekspertisiz. "
                f"Iltimos, aynan shu yo'nalishda: [{tanlangan_mavzu}] haqida "
                f"odamlar mutlaqo bilmaydigan, eng hayratlanarli bitta haqiqiy faktni o'zbek tilida yozing. "
                f"Matn xuddi ona tili o'zbekcha bo'lgan insondek juda jozibali, mantiqan to'g'ri va ravon bo'lishi shart! "
                f"G'alati so'zma-so'z tarjimalar yoki soxta iboralardan umuman foydalanmang. "
                f"Post sarlavhasi qalin (bold) va juda jozibali bo'lsin. Emojilardan ko'p va to'g'ri foydalaning. "
                f"Oxirida mavzuga mos hashtaglar yozing. Matn o'rtacha qisqa va qiziqarli bo'lsin."
            )
            config = types.GenerateContentConfig(temperature=1.0, top_p=0.95)
            response = ai_client.models.generate_content(model='gemini-2.5-flash', contents=prompt, config=config)
            
            await client.send_message(MY_CHANNEL, response.text)
            print(f"[{time.strftime('%H:%M:%S')}] Yangi post joylandi! Mavzu: {tanlangan_mavzu}")
            return 
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Xatolik (qayta urinish {urinish}): {e}")
            await asyncio.sleep(30)

async def main_loop():
    while True:
        await generate_and_post_fact()
        await asyncio.sleep(7200)

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Aqlli Telegram bot ishga tushdi...")
    # Veb-server va bot siklini parallel ishga tushiramiz
    await asyncio.gather(start_server(), main_loop())

if __name__ == '__main__':
    asyncio.run(main())
