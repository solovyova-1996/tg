from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, \
    DateTime, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.engine.url import URL


# DATABASE = {'draivername': 'postgres', 'host': 'localhost', 'port': '5432',
#             'username': 'username', 'password': 'password',
#             'database': 'tg_bot'}
engine = create_engine('sqlite:///tg_db.db', echo=True)
# engine = create_engine(URL(DATABASE), echo=True)
metadata = MetaData()
users = Table('users', metadata,
              Column('id', Integer(), primary_key=True),
              Column('tg_nik', String(50), nullable=False,unique=True),
              Column('first_name', String(50)),
              Column('last_name', String(50)),
              Column('car_brend', String(50)),
              Column('car_model', String(50)),
              Column('car_number', String(50)),
              Column('phone_number', String(15)))
# class Users(object):
#     pass
# mapper(Users,users)
requests = Table('requests', metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('driver', Integer(), ForeignKey('users.id'),
                        nullable=False),
                 Column('terms_delivery', String(50)),
                 Column('datetime', DateTime(), nullable=False),
                 Column('place_departure', String(50), nullable=False),
                 Column('place_comming', String(50), nullable=False),
                 Column('number_of_seats', Integer(), nullable=False))
# class Requests():
#     pass
# mapper(Requests,requests)
# создание всех таблиц
metadata.create_all(engine)
# добавление данных
# values = ['@dar','Дарья','Шатилова','Toyota','Camry','a 456 rt','89503378718']
ins = users.insert()
user_1= ins.values(tg_nik='@dar',first_name='Дарья',last_name='Шатилова',car_brend='Toyota',car_model='Camry',car_number='a 456 rt',phone_number='89503378718' )
conn =engine.connect()
conn.execute(user_1)


# import sqlite3
# db='tg2.db'
# conn = sqlite3.connect(db,
#                        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
# cur = conn.cursor()
# cur.execute("""CREATE TABLE IF NOT EXISTS users (
# 	user_id integer PRIMARY KEY AUTOINCREMENT,
# 	tg_nik varchar not null,
# 	first_name varchar,
# 	last_name varchar,
# 	car_brend varchar,
# 	car_model varchar,
# 	car_number varchar,
# 	phone_number varchar
# );
# """)
#
# cur.execute("""
#  CREATE TABLE IF NOT EXISTS requests (
# 	id integer PRIMARY KEY AUTOINCREMENT,
# 	driver integer not null,
# 	terms_delivery varchar,
# 	datetime datetime not null,
# 	place_departure varchar not null,
# 	place_comming varchar not null,
# 	number_of_seats integer not null
# );
# """)
# conn.commit()
#
# field_list_users =['tg_nik','first_name','last_name','car_brend','car_model','car_number','phone_number']
# field_list_requests =['driver','terms_delivery','datetime','place_departure','place_comming','number_of_seats']
# values = ['@dar','Дарья','Шатилова','Toyota','Camry','a 456 rt','89503378718']
# values_1 =[1,'за 100','ул. Звездова 101 а', '2004-05-23T14:25:10','пр-кт Комарова 22',2]
#
# def str_question(len_str):
#     '''
#     Функция формирует строку типа '?,?,?',необходимую для sql запроса
#     :param len_str: кол-во ? в строке
#     :return: строка типа '?,?,?'
#     '''
#     str_1 = ''
#     for i in range(len_str):
#         if i != len_str - 1:
#             str_1 += '?, '
#         else:
#             str_1 += '?'
#     return len_str
#
#
# def add_data(name_table, field_list, value_list, db):
#     '''
#     Функция добавления даты в БД
#     :param name_table: имя таблицы
#     :param field_list: список полей таблицы
#     :param value_list: список значений для записи в таблицу
#     :param db:
#     :return:
#     '''
#     str_for_sql = str_question(len(field_list))
#     conn = sqlite3.connect(db,
#                            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
#     cur = conn.cursor()
#     cur.execute(
#         f"INSERT INTO {name_table} {tuple(field_list)} VALUES ({str_for_sql});",
#         value_list)
#     conn.commit()
#
#
# def select_data(name_table,field,value):
#     '''
#     Функция выбора данных из базы данных с условием 'WHERE field = field'
#     :param name_table: имя таблицы
#     :param field: название поля
#     :param value: значение поля
#     :return: список значений(строка таблицы)
#     '''
#     conn = sqlite3.connect(db,
#                            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
#     cur = conn.cursor()
#     res =  cur.execute(
#         f"SELECT * FROM {name_table} WHERE {field} = {value};")
#     return res
#
#
# # add_data('users',field_list_users,values)
# # add_data('requests',field_list_requests,values_1)
# res = select_data('users','user_id',1)
# print(list(res))
