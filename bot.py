import logging
from aiogram import Bot,Dispatcher,executor,types
from os import getenv
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery,ReplyKeyboardMarkup
from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar
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


# @dp.message_handler(commands="start")
# async def cmd_start(message:types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons=["Водитель","Пассажир"]
#     button_cancel = types.KeyboardButton(text="Отмена")
#     keyboard.add(*buttons)
#     keyboard.add(button_cancel)
#     await message.answer("Выберите роль",reply_markup=keyboard)

@dp.message_handler(commands="start")
async def cmd_start(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons=["Создать заявку","Мои заявки"]
    buttons_1=["Оценить пользователя","Отмена"]
    button_create_profile = types.KeyboardButton(text="Создать/редактировать профиль")
    keyboard.row(*buttons)
    keyboard.add(button_create_profile)
    keyboard.row(*buttons_1)
    name = message.from_user.first_name
    await message.answer(f"Здравствуйте {name}!Вaс приветствует бот-развоз.Вы в главном меню",reply_markup=keyboard)



@dp.message_handler(Text(equals=['Создать заявку'], ignore_case=True))
async def choice_date(message:types.Message):
    await message.answer("Выерите дату: ", reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Назад","Отмена","Выбрать время"]
    keyboard.add(*buttons)
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали дату {date.strftime("%d-%m-%Y")}',
            reply_markup=keyboard
        )

# @dp.message_handler(Text(equals=['Назад'], ignore_case=True))
# async def back(message:types.Message):


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