import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_calendar import simple_cal_callback, SimpleCalendar, \
    dialog_cal_callback, DialogCalendar
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import datetime
from tg_bd import add_data_in_user, users, engine, add_data_in_requests
from sqlalchemy import select

storage = MemoryStorage()

# бот
bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Ошибка, нет токена")
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
# создание клавиатуры для выбора даты
date_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
month = datetime.datetime.now().month
day = datetime.datetime.now().day
print(day)
count = 0
row = []
for i in range(day, day + 5):
    if count == 3:
        date_keyboard.row(*row)
        row.clear()
        count = 0
    str_month = str(month)
    button = f"{i}.{month if len(str(month))==2 else '0'+str_month}"
    row.append(button)
    count += 1
date_keyboard.row(*row)
button_cancel = types.KeyboardButton(text="Отмена")
date_keyboard.add(button_cancel)
##############################################
# создание клавиатуры для выбора даты
time_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
time_keyboard.row(*["22:00", "22:10", "22:20", "22:30", "22:40"])
time_keyboard.row(*["23:00", "23:10", "23:20", "23:30", "23:40"])
time_keyboard.row(*["01:00", "01:10", "01:20", "01:30", "01:40"])
time_keyboard.row(*["02:00", "02:10", "02:20", "02:30", "02:40"])
time_keyboard.add(button_cancel)
##############################################
# создание клавиатуры для введения места отправления и места прибытия
default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add(button_cancel)
##############################################
# создание клавиатуры для введения места отправления и места прибытия
number_of_seats_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
number_of_seats_keyboard.row(*['1','2'])
number_of_seats_keyboard.row(*['3','4'])
number_of_seats_keyboard.add(button_cancel)
##############################################
# Клавиатура для главного меню
keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Создать заявку", "Мои заявки"]
buttons_1 = ["Оценить пользователя", "Отмена"]
button_create_profile = types.KeyboardButton(text="Создать/редактировать профиль")
keyboard_menu.row(*buttons)
keyboard_menu.add(button_create_profile)
keyboard_menu.row(*buttons_1)

############################################
# Создание формы для создания заявки
class Request(StatesGroup):
    date = State()
    time = State()
    place_departure = State()
    place_comming = State()
    number_of_seats = State()
res = []

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    name = message.from_user.first_name
    tg_nik = message.from_user.id
    date_user = [tg_nik, name, "", "", "", "", ""]
    add_data_in_user(date_user)
    select_user = select([users.c.id]).where(
        users.c.tg_nik == message.from_user.id)
    res.append(select_user)
    await message.answer(
        f"Здравствуйте, {name}!\nВaс приветствует бот-развоз.\nВы в главном меню:",
        reply_markup=keyboard_menu)


# Добавляем возможность отмены, если пользователь передумал заполнять
@dp.message_handler(state='*', commands='Отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Вы в главном меню', reply_markup=keyboard_menu)


@dp.message_handler(Text(equals=['Создать заявку'], ignore_case=True))
async def choice_date(message: types.Message):
    await Request.date.set()
    await message.answer("Выерите дату: ", reply_markup=date_keyboard)


@dp.message_handler(state=Request.date)
async def process_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await Request.next()
    await message.answer("Выберите время:", reply_markup=time_keyboard)


@dp.message_handler(state=Request.time)
async def process_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
        res.append(f"{data['date']}{data['time']}")
    await Request.next()
    await message.answer("Введите место отправления",reply_markup=default_keyboard)


@dp.message_handler(state=Request.place_departure)
async def process_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['place_departure'] = message.text
        res.append(data['place_departure'])
    await Request.next()
    await message.answer("Введите место прибытия",reply_markup=default_keyboard)


@dp.message_handler(state=Request.place_comming)
async def process_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['place_comming'] = message.text
        res.append(data['place_comming'])
    await Request.next()
    await message.answer("Выберите количество мест:",reply_markup=number_of_seats_keyboard)


@dp.message_handler(state=Request.number_of_seats)
async def process_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_of_seats'] = message.text
        res.append(data['number_of_seats'])
        add_data_in_requests(res)
    await state.finish()
    await message.answer('Заявка создана', reply_markup=keyboard_menu)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)  # storage = MemoryStorage()
# # бот
# bot_token = getenv("BOT_TOKEN")
# if not bot_token:
#     exit("Ошибка, нет токена")
# bot = Bot(token=bot_token)
# dp = Dispatcher(bot)
# logging.basicConfig(level=logging.INFO)
#
#
#
#
#
#
#
# @dp.message_handler(commands="start")
# async def cmd_start(message:types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons=["Создать заявку","Мои заявки"]
#     buttons_1=["Оценить пользователя","Отмена"]
#     button_create_profile = types.KeyboardButton(text="Создать/редактировать профиль")
#     keyboard.row(*buttons)
#     keyboard.add(button_create_profile)
#     keyboard.row(*buttons_1)
#     name = message.from_user.first_name
#     await message.answer(f"Здравствуйте {name}!Вaс приветствует бот-развоз.Вы в главном меню",reply_markup=keyboard)
#
#
# @dp.message_handler(Text(equals=['Создать заявку'], ignore_case=True))
# async def choice_date(message:types.Message):
#     await message.answer("Выерите дату: ", reply_markup=await SimpleCalendar().start_calendar())
#
#
# @dp.callback_query_handler(simple_cal_callback.filter())
# async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ["Изменить дату","Отмена","Выбрать время"]
#     keyboard.add(*buttons)
#     selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
#     print(date)
#     if selected:
#         await callback_query.message.answer(
#             f'Вы выбрали дату {date.strftime("%d-%m-%Y")}',
#             reply_markup=keyboard
#         )
# async def process_simple_time(callback_query: CallbackQuery, callback_data: dict):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ["Изменить дату","Отмена","Выбрать время"]
#     keyboard.add(*buttons)
#     selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
#     print(date)
#     if selected:
#         await callback_query.message.answer(
#             f'Вы выбрали дату {date.strftime("%d-%m-%Y")}',
#             reply_markup=keyboard
#         )
# @dp.message_handler(content_types=['text'])
# async def choice_date(message:types.Message):
#     if message.text == "Изменить дату":
#         await message.answer("Выерите дату: ", reply_markup=await SimpleCalendar().start_calendar())
#
#
#
#
# if __name__ == "__main__":
#     executor.start_polling(dp,skip_updates=True)
