from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, \
    DateTime, ForeignKey, select, delete, update
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# создание БД,показ логов включен
engine = create_engine('sqlite:///t3333.db', echo=True)
metadata = MetaData()
# создание таблиц
users = Table('users', metadata, Column('id', Integer(), primary_key=True),
              Column('tg_nik', String(50), unique=True),
              Column('tg_id', String(50), nullable=False, unique=True),
              Column('first_name', String(50)), Column('last_name', String(50)),
              Column('car_brend', String(50)), Column('car_model', String(50)),
              Column('car_number', String(50)),
              Column('phone_number', String(15)))

requests = Table('requests', metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('driver', Integer(), ForeignKey('users.id'),nullable=False),
                 Column('terms_delivery', String(50)),
                 Column('date', String(),nullable=False),
                 Column('time', String(),nullable=False),
                 Column('place_departure', String(50),nullable=False),
                 Column('place_comming', String(50),nullable=False),
                 Column('number_of_seats', Integer(),nullable=False))

# создание всех таблиц
metadata.create_all(engine)


def add_data_in_user(values):
    '''
    Функция добавления записи в таблицу users
    :param values: список значений
    :return:
    '''
    ins = users.insert()
    field_list_users = ['tg_nik','tg_id', 'first_name', 'last_name', 'car_brend',
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
    :param values: словарь ключ-значение для заполнения строки в таблице
    :return:
    '''
    ins = requests.insert()
    requests_add = ins.values(values)
    conn = engine.connect()
    conn.execute(requests_add)




def select_data_from_users(user_id):
    user_date = select([users.c.first_name,users.c.last_name,users.c.car_brend,users.c.car_model,users.c.car_number,users.c.phone_number]).where(users.c.id == user_id)
    conn = engine.connect()
    result_user_date = conn.execute(user_date)
    result_user_date = list(result_user_date)
    return list(result_user_date[0])
# if __name__ == '__main__':
    # пример добавление данных
    #
    # values = ['@ckkda[r','1454049968', 'Дарья', 'Шатилова', 'Toyota', 'Camry', 'a 456 rt',
    #           '89503378718']
    # values_1 = [1, 'за 100', '1776-01-01', '00:00:00', 'ул. Звездова 101 а',
    #             'пр-кт Комарова 22', 2]
    # add_data_in_user(values)
    # add_data_in_requests(values_1)
    #
    # # Пример выбора данных(выбор модели машины пользователя с id==1) из бд, атрибут "c"-столбец
    # # select([users.c.car_model]) - перечисление столбцов,которые нужно выбрать
    # # where(users.c.id==1) - условия выбора
    # select_user = select([users.c.car_model]).where(users.c.id == 1)
    # conn = engine.connect()
    # result = conn.execute(select_user)
    # for res in result:
    #     print(res[0])
    #
    # # удаление данных из таблицы
    # delete_user = delete(users).where(users.c.id == 1)
    # conn = engine.connect()
    # result_delete = conn.execute(delete_user)
    #
    # # изменение данных в таблице
    # update_user = update(users).where(users.c.id == 1).values(car_model='lada')
    # conn = engine.connect()
    # result_update = conn.execute(update_user)
    #
    # # пример использования функции конвертации строки в тип datetime
    # convert_datetime = select([requests.c.datetime]).where(requests.c.id == 1)
    # conn = engine.connect()
    # result = conn.execute(convert_datetime)
    # for res in result:
    #     print(conversion_to_datetime(res[0]).day)
    # print(select_data_from_users(1))