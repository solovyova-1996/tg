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
from datetime import datetime,date,time
def handler_date(str_date):
    lst_date = str_date.split('.')
    day = int(lst_date[0])
    month = int(lst_date[1])
    year = datetime.now().year
    return date(year,month,day)
def handler_time(str_time):
    lst_time = str_time.split(':')
    hour = int(lst_time[0])
    minute = int(lst_time[1])
    second = 0
    return time(hour,minute,second)
def combine_date_and_time(date_res,time_res):
    return datetime.combine(date_res,time_res)
def refactor_str(str_input):
    str_input = str(str_input)
    return f"{str_input if len(str_input) == 2 else '0'+str_input}"
def convert_str_in_date(str_date):
    return datetime.strptime(str_date,"%Y-%m-%d")
def convert_str_in_time(str_time):
    return datetime.strptime(str_time,"%H:%M:%S")
if __name__ == '__main__':
    # str_date = "17.08"
    # str_time = "22:20"
    # res_date = handler_date(str_date)
    # res_time = handler_time(str_time)
    #
    # print(combine_date_and_time(res_date,res_time))
    # print(type(combine_date_and_time(res_date,res_time)))
    str_date = '2022-08-19'
    a = convert_str_in_date(str_date)
    print(a.day)
    print(refactor_str(convert_str_in_date(str_date).day))
    str_time = '22:30:00'
    print(refactor_str(convert_str_in_time(str_time).hour))
    print(refactor_str(convert_str_in_time(str_time).minute))