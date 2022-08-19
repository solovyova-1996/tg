import logging
import aiogram.utils.markdown as md
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
from tg_bd import add_data_in_user, users, requests, engine, \
    add_data_in_requests, select_data_from_users
from sqlalchemy import select
from main import handler_date, handler_time, combine_date_and_time, \
    refactor_str, convert_str_in_date, convert_str_in_time
import emoji
from aiogram.types import ParseMode

storage = MemoryStorage()

# бот
bot_token = getenv("BOT_TOKEN")
channel_id = getenv("CHANNEL_ID")

if not bot_token:
    exit("Ошибка, нет токена")
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
# создание клавиатуры для выбора даты
date_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
month = datetime.datetime.now().month
day = datetime.datetime.now().day
count = 0
row = []

for i in range(day, day + 5):
    if count == 3:
        date_keyboard.row(*row)
        row.clear()
        count = 0
    str_month = str(month)
    str_day = str(day)
    button = f"{i if len(str_day) == 2 else '0' + str_day}.{month if len(str_month) == 2 else '0' + str_month}"
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
# создание клавиатуры для введения места прибытия
default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add(button_cancel)
##############################################
# создание клавиатуры для введения места отправления
keyboard_place_departure = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_place_departure = types.KeyboardButton(text="ул.Звездова 101 A")
keyboard_place_departure.add(button_place_departure)
keyboard_place_departure.add(button_cancel)
##############################################
# создание клавиатуры для введения условий довоза
keyboard_terms_delivery = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_terms_delivery = types.KeyboardButton(text="Дальше")
button_shoko = types.KeyboardButton(
    text="За шоколадку " + emoji.emojize(":chocolate_bar:"))
keyboard_terms_delivery.add(button_shoko)
keyboard_terms_delivery.add(button_terms_delivery)
keyboard_terms_delivery.add(button_cancel)
##############################################
# создание клавиатуры для введения места прибытия
number_of_seats_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
number_of_seats_keyboard.row(*['1', '2'])
number_of_seats_keyboard.row(*['3', '4'])
number_of_seats_keyboard.add(button_cancel)
##############################################
# Клавиатура для главного меню
keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Создать заявку", "Мои заявки"]
buttons_1 = ["Оценить пользователя", "Отмена"]
button_create_profile = types.KeyboardButton(
    text="Создать/редактировать профиль")
keyboard_menu.row(*buttons)
keyboard_menu.add(button_create_profile)
keyboard_menu.row(*buttons_1)

##############################################
# Клавиатура для подтверждения заявки
keyboard_ok = types.ReplyKeyboardMarkup(resize_keyboard=True)

button_requests_ok = types.KeyboardButton(text="Подтвердить заявку")
button_menu = types.KeyboardButton(text="В главное меню")
button_requests_error = types.KeyboardButton(text="Отменить заявку")
keyboard_ok.add(button_requests_ok)
keyboard_ok.add(button_requests_error)
keyboard_ok.add(button_menu)


############################################



@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):

    name = message.from_user.first_name
    last_name = message.from_user.last_name
    tg_id = message.from_user.id
    tg_nik = message.from_user.username
    date_user = [tg_nik, tg_id, name,last_name, 'Toyota', 'Camry', 'a 456 rt','89503378718']
    add_data_in_user(date_user)
    # select_user = select([users.c.id]).where(
    #     users.c.tg_id == message.from_user.id)
    # conn = engine.connect()
    # result = conn.execute(select_user)
    # result = list(result)
    # # res.append(result[0][0])
    await message.answer(
        f"Здравствуйте, {name}!\nВaс приветствует бот-развоз " + emoji.emojize(
            ':oncoming_automobile:') + "\nВы в главном меню:",
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


@dp.message_handler(Text(equals='В главное меню', ignore_case=True))
async def menu_handler(message: types.Message):
    await message.answer('Вы в главном меню:', reply_markup=keyboard_menu)


@dp.message_handler(Text(equals=['Мои заявки'], ignore_case=True))
async def main_requests(message: types.Message):
    # декомпозтровать в файл бд
    select_user = select([users.c.id]).where(
        users.c.tg_id == message.from_user.id)
    conn = engine.connect()
    result_user = conn.execute(select_user)
    result_user = list(result_user)
    result_user = result_user[0][0]
    print(result_user)
    select_request = select([requests]).where(requests.c.driver == result_user)
    conn = engine.connect()
    result_requests = conn.execute(select_request)
    ################################################
    keyboard_requests = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in list(result_requests)[-5:]:
        str_date = convert_str_in_date(i[3])
        str_time = convert_str_in_time(i[4])
        button = types.KeyboardButton(
            text=f"{refactor_str(str_date.day)}.{refactor_str(str_date.month)} | {i[5]} -> {i[6]}")
        keyboard_requests.add(button)
    button_menu = types.KeyboardButton(text="В главное меню")
    keyboard_requests.add(button_menu)
    if len(keyboard_requests["keyboard"]) > 0:
        await message.answer("Ваши заявки " + emoji.emojize(':open_book:'),
                             reply_markup=keyboard_requests)
    else:
        await message.answer(
            f"{message.from_user.first_name}, у вас нет ни одной заявки \nВы в главном меню: ",
            reply_markup=keyboard_menu)

############################ Создание заявки #########################
# Создание формы для создания заявки
class Request(StatesGroup):
    date = State()
    time = State()
    terms_delivery = State()
    place_departure = State()
    place_comming = State()
    number_of_seats = State()
    driver = State()


@dp.message_handler(Text(equals=['Создать заявку'], ignore_case=True))
async def choice_date(message: types.Message):
    await Request.date.set()
    await message.answer("Выерите дату " + emoji.emojize(':calendar:'),
                         reply_markup=date_keyboard)

@dp.message_handler(state=Request.date)
async def process_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = str(handler_date(message.text))
    await Request.next()
    await message.answer("Выберите время" + emoji.emojize(':alarm_clock:'),
                         reply_markup=time_keyboard)


@dp.message_handler(state=Request.time)
async def process_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = str(handler_time(message.text))
    await Request.next()
    await message.answer(
        "Введите условие довоза\n Например: 'за шоколадку' \n Или нажмите  'дальше'",
        reply_markup=keyboard_terms_delivery)


@dp.message_handler(state=Request.terms_delivery)
async def process_terms_delivery(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['terms_delivery'] = message.text
    await Request.next()
    await message.answer(
        "Введите или выберите место отправления\nНапример:'Маркса 22'",
        reply_markup=keyboard_place_departure)


@dp.message_handler(state=Request.place_departure)
async def process_place_departure(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['place_departure'] = message.text
    await Request.next()
    await message.answer("Введите место прибытия\nНапример:'Маркса 22'",
                         reply_markup=default_keyboard)


@dp.message_handler(state=Request.place_comming)
async def process_place_comming(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['place_comming'] = message.text
    await Request.next()
    await message.answer("Выберите количество мест:",
                         reply_markup=number_of_seats_keyboard)


@dp.message_handler(state=Request.number_of_seats)
async def process_number_of_seats(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_of_seats'] = int(message.text)
    await Request.next()
    await message.answer(
        'Подтвердите создание заявки  ' + emoji.emojize(':check_mark_button:'),
        reply_markup=keyboard_ok)
    await bot.send_message(message.chat.id, md.text(md.text(
        f'{md.bold("Когда и восколько: ")}{refactor_str(convert_str_in_date(data["date"]).day)}.{refactor_str(convert_str_in_date(data["date"]).month)}.{convert_str_in_date(data["date"]).year} в {refactor_str(convert_str_in_time(data["time"]).hour)}:{refactor_str(convert_str_in_time(data["time"]).minute)}'),
        md.text(
            f"{md.bold('Условия довоза: ')}{data['terms_delivery'] if data['terms_delivery'] != 'Дальше' else 'Не указано'}"),
        md.text(f'{md.bold("Место отправления: ")}{data["place_departure"]}'),
        md.text(f'{md.bold("Место прибытия: ")}{data["place_comming"]}'),
        md.text(f'{md.bold("Количество мест: ")}{data["number_of_seats"]}'),
        sep='\n', ), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(Text(equals=['Подтвердить заявку'], ignore_case=True))
@dp.message_handler(state=Request.driver)
async def process_driver(message: types.Message, state: FSMContext):
    if message.text == "Подтвердить заявку":
        async with state.proxy() as data:
            select_user = select([users.c.id]).where(
                users.c.tg_id == message.from_user.id)
            conn = engine.connect()
            result_user = conn.execute(select_user)
            result_user = list(result_user)
            result_user = result_user[0][0]
            data['driver'] = result_user
        data = await state.get_data()
        add_data_in_requests(data)
        print(data)
        user_data = select_data_from_users(result_user)
        await state.finish()
        await bot.send_message(message.chat.id,
                               md.text(md.text(f'{md.code("Заявка создана")}'),
                                       md.text(
                                           f'{md.bold("Водитель: ")}{user_data[0]} {user_data[1]} '),
                                       md.text(
                                           f'{md.bold("Номер телефона: ")}{user_data[5] if len(user_data[5]) > 0 else "не указан"}'),
                                       md.text(
                                           f'{md.bold("Машина: ")}{user_data[2]} {user_data[3]} ({user_data[4]})'),
                                       md.text(
                                           f'{md.bold("Когда и восколько: ")}{refactor_str(convert_str_in_date(data["date"]).day)}.{refactor_str(convert_str_in_date(data["date"]).month)}.{convert_str_in_date(data["date"]).year} в {refactor_str(convert_str_in_time(data["time"]).hour)}:{refactor_str(convert_str_in_time(data["time"]).minute)}'),
                                       md.text(
                                           f"{md.bold('Условия довоза: ')}{data['terms_delivery'] if data['terms_delivery'] != 'Дальше' else 'Не указано'}"),
                                       md.text(
                                           f'{md.bold("Место отправления: ")}{data["place_departure"]}'),
                                       md.text(
                                           f'{md.bold("Место прибытия: ")}{data["place_comming"]}'),
                                       md.text(
                                           f'{md.bold("Количество мест: ")}{data["number_of_seats"]}'),
                                       sep='\n', ), reply_markup=keyboard_menu,
                               parse_mode=ParseMode.MARKDOWN)
        await bot.send_message(channel_id, md.text(
            md.text(f'{md.bold("Водитель: ")}{user_data[0]} {user_data[1]} '),
            md.text(
                f'{md.bold("Номер телефона: ")}{user_data[5] if len(user_data[5]) > 0 else "не указан"}'),
            md.text(
                f'{md.bold("Машина: ")}{user_data[2]} {user_data[3]} ({user_data[4]})'),
            md.text(
                f'{md.bold("Когда и восколько: ")}{refactor_str(convert_str_in_date(data["date"]).day)}.{refactor_str(convert_str_in_date(data["date"]).month)}.{convert_str_in_date(data["date"]).year} в {refactor_str(convert_str_in_time(data["time"]).hour)}:{refactor_str(convert_str_in_time(data["time"]).minute)}'),
            md.text(
                f"{md.bold('Условия довоза: ')}{data['terms_delivery'] if data['terms_delivery'] != 'Дальше' else 'Не указано'}"),
            md.text(
                f'{md.bold("Место отправления: ")}{data["place_departure"]}'),
            md.text(f'{md.bold("Место прибытия: ")}{data["place_comming"]}'),
            md.text(f'{md.bold("Количество мест: ")}{data["number_of_seats"]}'),
            sep='\n', ), parse_mode=ParseMode.MARKDOWN)
    else:
        await state.finish()
        await message.answer('Вы в главном меню:', reply_markup=keyboard_menu)

############################ Создание профиля #########################
# Создание формы для создания профиля
# ['tg_nik','tg_id', 'first_name', 'last_name', 'car_brend','car_model', 'car_number', 'phone_number']
# class Users(StatesGroup):
#     date = State()
#     time = State()
#     terms_delivery = State()
#     place_departure = State()
#     place_comming = State()
#     number_of_seats = State()
#     driver = State()
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
