# from tg_bd import add_data_in_user,users,engine
# from sqlalchemy import select
# values = ['@daria', 'Дарья', 'Шатилова', 'Toyota', 'Camry', 'a 456 rt',
#           '89503378718']
# add_data_in_user(values)
# select_user = select([users.c.car_model]).where(users.c.id == 1)
# conn = engine.connect()
# result = conn.execute(select_user)
# for res in result:
#     print(res[0])
from datetime import datetime
a = '1776-01-01 00:00:00'
d = datetime.strptime(a,"%Y-%m-%d %H:%M:%S")
print(d.)