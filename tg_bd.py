from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, \
    DateTime, ForeignKey, select, delete, update
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# создание БД,показ логов включен
engine = create_engine('sqlite:///tg_а2.db', echo=True)
metadata = MetaData()
# создание таблиц
users = Table('users', metadata, Column('id', Integer(), primary_key=True),
              Column('tg_nik', String(50), nullable=False, unique=True),
              Column('first_name', String(50)), Column('last_name', String(50)),
              Column('car_brend', String(50)), Column('car_model', String(50)),
              Column('car_number', String(50)),
              Column('phone_number', String(15)))

requests = Table('requests', metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('driver', Integer(), ForeignKey('users.id')), Column('terms_delivery', String(50)),
                 Column('datetime', String()),
                 Column('place_departure', String(50)),
                 Column('place_comming', String(50)),
                 Column('number_of_seats', Integer()))

# создание всех таблиц
metadata.create_all(engine)


def add_data_in_user(values):
    '''
    Функция добавления записи в таблицу users
    :param values: список значений
    :return:
    '''
    ins = users.insert()
    field_list_users = ['tg_nik', 'first_name', 'last_name', 'car_brend',
                        'car_model', 'car_number', 'phone_number']
    obj_create = dict(zip(field_list_users, values))
    user_add = ins.values(obj_create)
    conn = engine.connect()

    try:
        conn.execute(user_add)
    except IntegrityError:
        print(
            f"Ошибка,попытка добавления записи с неуникальным tg_nik,{values[0]}-уже существует")


def add_data_in_requests(values):
    '''
    Функция добавления записи в таблицу requests
    :param values: список значений
    :return:
    '''
    ins = requests.insert()
    field_list_requests = ['driver', 'terms_delivery', 'datetime',
                           'place_departure', 'place_comming',
                           'number_of_seats']
    obj_create = dict(zip(field_list_requests, values))
    requests_add = ins.values(obj_create)
    conn = engine.connect()
    conn.execute(requests_add)


def conversion_to_datetime(str_date):
    '''
    Конвертация строки в datetime (так как в sqlite нет типа datetime)
    :param str_date: строка с датой и временем
    :return: объкт класса datetime
    '''
    return datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    # пример добавление данных

    values = ['@ckkda[r', 'Дарья', 'Шатилова', 'Toyota', 'Camry', 'a 456 rt',
              '89503378718']
    values_1 = [1, 'за 100', '1776-01-01 00:00:00', 'ул. Звездова 101 а',
                'пр-кт Комарова 22', 2]
    add_data_in_user(values)
    add_data_in_requests(values_1)

    # Пример выбора данных(выбор модели машины пользователя с id==1) из бд, атрибут "c"-столбец
    # select([users.c.car_model]) - перечисление столбцов,которые нужно выбрать
    # where(users.c.id==1) - условия выбора
    select_user = select([users.c.car_model]).where(users.c.id == 1)
    conn = engine.connect()
    result = conn.execute(select_user)
    for res in result:
        print(res[0])

    # удаление данных из таблицы
    delete_user = delete(users).where(users.c.id == 1)
    conn = engine.connect()
    result_delete = conn.execute(delete_user)

    # изменение данных в таблице
    update_user = update(users).where(users.c.id == 1).values(car_model='lada')
    conn = engine.connect()
    result_update = conn.execute(update_user)

    # пример использования функции конвертации строки в тип datetime
    convert_datetime = select([requests.c.datetime]).where(requests.c.id == 1)
    conn = engine.connect()
    result = conn.execute(convert_datetime)
    for res in result:
        print(conversion_to_datetime(res[0]).day)
