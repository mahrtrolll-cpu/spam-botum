import asyncio
from collections import defaultdict, deque
from time import time

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8737262228:AAFU41QFkkE4CIJAhI1CvhuIchpSFv7TJBA"

bot = Bot(TOKEN)
dp = Dispatcher()

# Spam sistemi
user_messages = defaultdict(lambda: deque())
SPAM_LIMIT = 15
SPAM_TIME = 10

# Özel /start
@dp.message(Command("start"))
async def start(message: types.Message):
    if message.chat.type == "private":
        await message.answer(
            "Sadece özel çalışırım.\n@c31ksatanal"
        )

# Düzenlenen mesajları sil
@dp.edited_message()
async def edited(message: types.Message):
    try:
        await message.delete()
    except:
        pass

# Fotoğraf video sticker silme
async def delete_later(message):
    await asyncio.sleep(31)

    try:
        await message.delete()
    except:
        pass

@dp.message()
async def all_messages(message: types.Message):

    # Özel mesajlarda spam kontrol yapma
    if message.chat.type == "private":
        return

    user_id = message.from_user.id
    now = time()

    # Spam kontrol
    user_messages[user_id].append(now)

    while user_messages[user_id]:
        if now - user_messages[user_id][0] > SPAM_TIME:
            user_messages[user_id].popleft()
        else:
            break

    if len(user_messages[user_id]) >= SPAM_LIMIT:
        warn = await message.answer(
            "@admin Spam var!"
        )

        await asyncio.sleep(5)

        try:
            await warn.delete()
        except:
            pass

        user_messages[user_id].clear()

    # Medya silme
    if (
        message.photo
        or message.video
        or message.sticker
    ):
        asyncio.create_task(delete_later(message))

async def main():
    print("Bot aktif!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())