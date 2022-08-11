from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, \
    DateTime, ForeignKey

import datetime
from sqlalchemy.orm import mapper
from sqlalchemy.engine.url import URL


# создание БД,показ логов включен
engine = create_engine('sqlite:///tg_db2.db', echo=True)
metadata = MetaData()
# создание таблиц
users = Table('users', metadata,
              Column('id', Integer(), primary_key=True),
              Column('tg_nik', String(50), nullable=False,unique=True),
              Column('first_name', String(50)),
              Column('last_name', String(50)),
              Column('car_brend', String(50)),
              Column('car_model', String(50)),
              Column('car_number', String(50)),
              Column('phone_number', String(15)))

requests = Table('requests', metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('driver', Integer(), ForeignKey('users.id'),nullable=False),
                 Column('terms_delivery', String(50)),
                 Column('datetime', String(), nullable=False),
                 Column('place_departure', String(50), nullable=False),
                 Column('place_comming', String(50), nullable=False),
                 Column('number_of_seats', Integer(), nullable=False))

# создание всех таблиц
metadata.create_all(engine)
# пример добавление данных

values = ['@ckkda[r','Дарья','Шатилова','Toyota','Camry','a 456 rt','89503378718']
values_1 =[1,'за 100','ул. Звездова 101 а', '1776-01-01 00:00:00','пр-кт Комарова 22',2]

def add_data_in_user(values):
    '''
    Функция добавления записи в таблицу users
    :param values: список значений
    :return:
    '''
    ins = users.insert()
    field_list_users = ['tg_nik', 'first_name', 'last_name', 'car_brend', 'car_model', 'car_number', 'phone_number']
    obj_create = dict(zip(field_list_users,values))
    user_add = ins.values(obj_create)
    conn = engine.connect()
    conn.execute(user_add)

def add_data_in_requests(values):
    '''
    Функция добавления записи в таблицу requests
    :param values: список значений
    :return:
    '''
    ins = requests.insert()
    field_list_requests = ['driver','terms_delivery','datetime','place_departure','place_comming','number_of_seats']
    obj_create = dict(zip(field_list_requests,values))
    requests_add = ins.values(obj_create)
    conn = engine.connect()
    conn.execute(requests_add)

# add_data_in_user(values)
add_data_in_requests(values_1)