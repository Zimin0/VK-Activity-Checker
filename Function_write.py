import vk_api
import time 
from time import time, localtime, sleep

ss = vk_api.VkApi(token = 'your token')
vk = ss.get_api()


USERS = {
    'USER1': 555555555,
    'USER2': 555555555
}



def making_file_name(user_name,now):
    D = ('0' + str(now.tm_mday))[-2:]
    M = ('0' + str(now.tm_mon))[-2:]
    Y = ('0' + str(now.tm_year))[-2:]
    U = user_name
    file_name = '_'.join([D,M,Y,U]) + '.txt'
    print(file_name)
    return file_name


def WRITE_DATA_ACTIVITY(N_USER): 
    """Запись активности пользователя в файл."""

    SLEEP_TIME = 2
    now = localtime(time()) # (tm_year=2022, tm_mon=6, tm_mday=11, tm_hour=1, tm_min=3, tm_sec=4, tm_wday=5, tm_yday=162, tm_isdst=0)
    TIME_00_00_U = int(time()-(now.tm_sec + now.tm_min*60 + now.tm_hour*60*60)) # Время 00:00 в unix
    next_day_00_00 = TIME_00_00_U + 86_400 # Время 00:00 след. дня в unix
    val = True # переменная цикла
    online_now = False # был ли человек онлайн к моменту прошлого запроса

    file_name = making_file_name(N_USER,now) # делает имя в формате 27_06_22_USER1.txt
    try:
        f = open(file_name,'w+')
        start_offline = TIME_00_00_U
        while val:
            get_activity_now = ss.method('messages.getLastActivity', {'user_id':USERS[N_USER]}) # {'online': 0, 'time': 1654893554} # отправляем запрос к апи
            if get_activity_now['online'] == 1:
                print('online')
                if online_now == False: # если человек до этого не был в онлайне # == False для наглядности 
                    print('1')
                    start_online = int(get_activity_now['time'])  # когда программа сделала запрос и обнаружила, что человек онлайн # погрешность в SLEEP_TIME
                    word = (start_online - start_offline) * '0' + '1'
                    online_now = True
                    f.write(word)
            if get_activity_now['online'] == 0:
                print('offline')
                if online_now == True: # если человек до этого был в онлайне 
                    print('2')
                    start_offline = int(get_activity_now['time']) # Время последнего захода в сеть
                    word = (start_offline - start_online) * '1' + '0'
                    online_now = False
                    f.write(word)
            if int(time()) >= next_day_00_00: 
                # Когда будет запись в несколько файлов
                # if online_now == True:
                #     word = (next_day_00_00 - start_online) * '1' 
                # else:
                #     word = (next_day_00_00 -  start_offline) * '0'
                f = open(file_name,'w') # очищается файл 
                f.close()
            sleep(SLEEP_TIME)
    except:
        if online_now == True: # если вызвало ошибку - то активность будет все равно дозаписана в файл 
            word = (next_day_00_00 - start_online) * '1' 
        else:
            word = (next_day_00_00 -  start_offline) * '0'
        f.write(word)
        f.close()
    finally:
        return file_name, TIME_00_00_U, int(time())



############# КОНЕЦ ЗАПИСИ В ФАЙЛ #############
WRITE_DATA_ACTIVITY('USER1')          