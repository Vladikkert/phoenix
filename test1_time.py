import websocket
import pickle
import json
import time
import telebot
from keys import dragons, TELEGRAM_TOKEN, TELEGRAM_CHANNEL

Wyverna = telebot.TeleBot(TELEGRAM_TOKEN, num_threads=1)

#Функция загрузки из файла
def load(file):
    with open(f'{file}.pkl', 'rb') as f:
        data = pickle.load(f)
    return data

#Функция записи в файл
def dump(file, data):
    with open(f'{file}.pkl', 'wb') as f:
        pickle.dump(data, f)

print(1)

# while True:
#     try:
#         a = load('za_last_price_rsi')
#         #l = []
#         max_key = max(a, key=lambda x: a[x])
#         max_value = a[max_key]
#         print(max_key, max_value)
#         # for i in a:
#         #     l.append(a[i])
        
#         # print(max(l))
#             #if a[i] > 51:


#             #print(i, a[i])

#         #print(a['BTCUSDT'])

#     except Exception as e:
#         print(e)
#         continue
        

#     time.sleep(5)


#Посмотреть данные по списку\
while True:
    a = load('za_volume')
    for i in a:
        if a[i][-1]/2 > sum(a[i][:-1])/5999 :
            #for i in range(10):
            Wyverna.send_message(TELEGRAM_CHANNEL, i)
            print(i, a[i][-1])
    time.sleep(5)


# #Посмотреть максимум и минимум выгруженного списка
# while True:
#     try:
#         a = load('za_last_price_rsi')
#         #print(a['SNTUSDT'])
#         l = []
#         max_key = max(a, key=lambda x: a[x])
#         max_value = a[max_key]

#         min_key = min(a, key=lambda x: a[x])
#         min_value = a[min_key]

#         print()
#         print(max_key, max_value)
#         print(min_key, min_value)
#         print()

#         # # for i in a:
#         # #     l.append(a[i])
        
#         # # print(max(l))
#         #     #if a[i] > 51:


#         #     #print(i, a[i])

#         # #print(a['BTCUSDT'])

#     except Exception as e:
#         print(e)
#         continue
        


