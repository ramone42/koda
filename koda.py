from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import whisper
import requests

API_KEY = "sk-f5a58234a9a74ee8875fb56936ec522c"
DEEPSEEK_URL = "https://api.deepseek.com/query"  # DeepSeek API URL
TELEGRAM_TOKEN = "5294576020:AAGFeriHYcoJgqiVCjpYb0bm0nKjfMvxvlc"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Whisper modelini yuklash
model = whisper.load_model("base")

def get_answer_from_deepseek(query):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    
    payload = {
        "query": query,
        "language": "uz"  # O'zbek tilida javob olish
    }
    
    response = requests.post(DEEPSEEK_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "Xatolik yuz berdi."

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path, language="uz")
    return result["text"]

@dp.message_handler(content_types=types.ContentType.AUDIO)
async def handle_audio(message: types.Message):
    file = await message.audio.download()
    
    # Audio fayldan matn olish
    query = transcribe_audio(file.name)
    print(f"Foydalanuvchidan so'ralgan: {query}")
    
    # DeepSeek API orqali javob olish
    answer = get_answer_from_deepseek(query)
    print(f"Javob: {answer}")
    
    # Foydalanuvchiga javob yuborish
    await message.reply(answer)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)