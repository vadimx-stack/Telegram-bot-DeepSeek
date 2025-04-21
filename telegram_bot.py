import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
import aiohttp
from typing import Dict, Any


TOKEN = ''


logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()
session = None


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я бот с подключенной нейросетью, отправь свой запрос', parse_mode = 'HTML')


@dp.message()
async def filter_messages(message: Message):
    await bot.send_chat_action(message.chat.id, "typing")
    
    response_text = await get_ai_response(message.text)
    
    await message.answer(response_text, parse_mode="Markdown")


async def get_ai_response(user_query: str) -> str:
    global session
    
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer ",
    }

    data = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Keep your responses concise."
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 1
    }

    try:
        async with session.post(url, headers=headers, json=data, timeout=30) as response:
            response_data = await response.json()
            text = response_data['choices'][0]['message']['content']
            try:
                bot_text = text.split('</think>\n\n')[1]
            except:
                bot_text = text
            return bot_text
    except Exception as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        return "Извините, произошла ошибка при обработке запроса."


async def main():
    global session
    session = aiohttp.ClientSession()
    
    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(main()) 