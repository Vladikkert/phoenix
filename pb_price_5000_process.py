
import websocket
import json
import time
import pickle

import logging
from pytz import timezone 
from datetime import datetime

import threading


#########################################################
logging.basicConfig(level=logging.INFO, filename='pb_price_5000_logging.log', format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]', datefmt='%d/%m/%Y %I:%M:%S',
                    filemode='w')

warlock = logging.getLogger(__name__)
handler = logging.FileHandler('warlock.log', encoding='utf-8')
formatter = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]')


tz = timezone('Europe/Moscow') # UTC + 3
formatter.converter = lambda *args: tz.fromutc(datetime.utcnow()).timetuple()

handler.setFormatter(formatter)


warlock.addHandler(handler)
############################################################



def update_last_price():
    # Открываем файл и загружаем словарь
    file1 = open(f"za_last_price.pkl", "rb")
    last_price_1 = pickle.load(file1)
    file1.close() # Закрыть файл

    file2 = open(f"za_last_price_5.pkl", "rb")
    last_price_5 = pickle.load(file2)
    file2.close()

    file3 = open(f"za_last_price_sma.pkl", "rb")
    last_price_sma = pickle.load(file3)
    file3.close()

    file3 = open(f"za_volume.pkl", "rb")
    volume = pickle.load(file3)
    file3.close()

    

    for key in last_price_1.keys():

        # Обновляем значения для объемов
        if key in volume.keys():
            volume[key].append(last_price_1[key][1])
            volume[key] = volume[key][-6000:]
        else:
            volume[key] = []
            

        # Обновляем значения в словаре для сумм и СМА
        if key in last_price_5.keys():
            #print(1)
            if isinstance(last_price_5[key], list):
                #print(1)
                #Записываем последнюю цену
                last_price_5[key].append(last_price_1[key][0])
                last_price_5[key] = last_price_5[key][-6000:]

                #Записываем SMA 
                price_for_SMA = last_price_5[key]

                #print(len(price_for_SMA))
                if len(price_for_SMA) == 6000:

                    SMA = sum(price_for_SMA)/len(price_for_SMA)

                    if key in last_price_sma.keys():
                        #print(last_price_rsi[key]) 
                        if isinstance(last_price_sma[key], list):
                            #print(1)
                            last_price_sma[key].append(SMA)
                            last_price_sma[key] = last_price_sma[key][-6000:]
                else:
                    last_price_sma[key] = []



                #if key == 'BTCUSDT':
                    #print(last_price_1[key])
                #print(len(btc))

                # # Модуль подсчета RSI ####################
                #btc = last_price_5[key][-420:]
                # if len(btc) > 15:
                #     s = btc[0]

                #     l = 0
                #     sh = 0

                #     for i in btc:
                #         d = i - s
                #         if d > 0:
                #             l += d  
                #         elif d < 0:
                #             sh += d

                #         s = i 

                #     AG = l/14
                #     AL = abs(sh/14)

                #     if AL != 0:
                #         RS = AG / AL
                #     else:
                #         RS = 1

                #     RSI = 100 - (100/(1 + RS))

                #     #last_price_rsi[key] = RSI

                #     if key in last_price_rsi.keys():
                #         #print(last_price_rsi[key])
                #         if isinstance(last_price_rsi[key], list):
                #             #print(1)
                #             last_price_rsi[key].append(RSI)
                #             last_price_rsi[key] = last_price_rsi[key][-20000:]
                #         else:
                #             last_price_rsi[key] = []

                #     #Разблочить
                #     # if RSI > 60:
                #     #     warlock.info(f'{key}, RSI = {str(RSI)}')
                #     # elif RSI < 40:
                #     #     warlock.info(f'{key}, RSI = {str(RSI)}')

                ############################################
                
        else:
            last_price_5[key] = []
            last_price_sma[key] = []

    #     last_price_5[key].append(float(last_price_1[key])) # Добавляем последнее значение в начало списка
    #     last_price_5[key] = last_price_5[key][-600:] # Ограничиваем список только пятью последними значениями

    #print(len(last_price_5['BTCUSDT']))
    # print(len(last_price_rsi['BTCUSDT']))
    #warlock.info(len(last_price_5['BTCUSDT']))
    file2 = open(f"za_last_price_5.pkl", "rb+")
    pickle.dump(last_price_5, file2)
    file2.close()

    file3 = open(f"za_last_price_sma.pkl", "rb+")
    pickle.dump(last_price_sma, file3)
    file3.close()

    file3 = open(f"za_volume.pkl", "rb+")
    pickle.dump(volume, file3)
    file3.close()


            
    # Сохраняем обновленный словарь по 5 тысячам монет в новый фай



warlock.info('*****Запуск, сохранения 5000 цен*****')

while True:
    try:
        update_last_price()
    except Exception as e:
        warlock.error('*****ошибка обновления цен 5000*****', e)
        time.sleep(2)
        continue

    #l = load('za_last_price_5')
    #print(l['BTCUSDT'])
    time.sleep(2)
