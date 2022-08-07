import logging
from aiogram import Bot,Dispatcher,executor,types
from os import getenv
# бот
bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Ошибка, нет токена")
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
@dp.message_handler(commands='test')
async def cmd_test(message:types.Message):
    await message.reply("Test")
@dp.message_handler(commands="answer")
async def cmd_answer(message: types.Message):
    await message.answer('Это простой ответ')
@dp.message_handler(commands="start")
async def cmd_start(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons=["Водитель","Пассажир"]
    button_cancel = types.KeyboardButton(text="Отмена")
    keyboard.add(*buttons)
    keyboard.add(button_cancel)
    await message.answer("Выберите роль",reply_markup=keyboard)
@dp.message_handler(lambda message: message.text == "Водитель")
async def driver(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Из дома", "Из ЕРКЦ"]
    button_cancel = types.KeyboardButton(text="Отмена")
    keyboard.add(*buttons)
    keyboard.add(button_cancel)
    await message.reply("Откуда поедете?",reply_markup=keyboard)
if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)