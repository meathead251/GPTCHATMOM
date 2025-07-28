import os
import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

# Вставь свои ключи:
TELEGRAM_BOT_TOKEN = "8265401743:AAGdHQx7C9O_zVnFvBuMGmhhLAHt-stlnRE"
OPENROUTER_API_KEY = "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"  # получим ниже

# Инициализация
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()

# Основная функция общения с GPT
async def ask_gpt(prompt: str, image_url: str = None):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "MomBot"
    }
    messages = [{"role": "user", "content": prompt}]
    if image_url:
        # Добавим картинку для анализа
        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}]
        })
    payload = {
        "model": "openai/gpt-4o-mini",  # Можно поменять на "gpt-4o" (дороже)
        "messages": messages
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            data = await resp.json()
            try:
                return data["choices"][0]["message"]["content"]
            except:
                return "Ошибка: не удалось получить ответ."

# Ответ на текстовые сообщения
@dp.message()
async def chat_with_gpt(message: types.Message):
    if message.photo:
        # Если фото, загружаем файл и передаем GPT
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file.file_path}"
        reply = await ask_gpt("Опиши, что на картинке.", image_url=file_url)
    else:
        reply = await ask_gpt(message.text)
    await message.answer(reply)

# Старт бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
