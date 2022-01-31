import requests
import json
import telebot
from telebot import TeleBot
from config import TOKEN, Mydict

bot: TeleBot = telebot.TeleBot(TOKEN)



class ConvertionException(Exception):
    pass

#первые команды
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Выберите доступную валюту: /currency \n Валютные операции /conversion'
    bot.reply_to(message,text)


#если выбрали конкретный курс без конвертаций

@bot.message_handler(commands=['currency'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in Mydict.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message,text)

@bot.message_handler(commands=['eur'])
def convert(message: telebot.types.Message):
    text = 'Актуальный курс Евро, PLN:'
    r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/eur/')  # запрос актуального среднего курса евро нац банка Польши
    texts = json.loads(r.content)  # конвертируем в читаемый формат
    Rates = texts.get('rates')  # убираем лишнее
    EUR = str(Rates[0].get('mid'))  # выводим только курс  в строковом формате иначе будет ошибка
    Mydict = {
        "eur": "",
    }
    Mydict["/eur"] = EUR
    for value in Mydict.values():
        text = '\n'.join((text, value,))
    bot.reply_to(message, text)

@bot.message_handler(commands=['usd'])
def convert(message: telebot.types.Message):
    text = 'Актуальный курс Доллара, PLN:'
    r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/')  # запрос актуального среднего курса доллара нац банка Польши
    texts = json.loads(r.content)  # конвертируем в читаемый формат
    Rates = texts.get('rates')  # убираем лишнее
    USD = str(Rates[0].get('mid'))  # выводим только курс  в строковом формате иначе будет ошибка
    Mydict = {
        "usd": "",
    }
    Mydict["/usd"] = USD
    for value in Mydict.values():
        text = '\n'.join((text, value,))
    bot.reply_to(message, text)

@bot.message_handler(commands=['rub'])
def convert(message: telebot.types.Message):
    text = 'Актуальный курс Российского рубля, PLN:'
    r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/rub/')  # запрос актуального среднего курса рубля нац банка Польши
    texts = json.loads(r.content)  # конвертируем в читаемый формат
    Rates = texts.get('rates')  # убираем лишнее
    RUB = str(Rates[0].get('mid'))  # выводим только курс  в строковом формате иначе будет ошибка
    Mydict = {
        "rub": "",
    }
    Mydict["/rub"] = RUB
    for value in Mydict.values():
        text = '\n'.join((text, value,))
    bot.reply_to(message, text,)


#если выбрали  конвертацию валют


#  выводим на экран список операций и все актуальные  курсы
@bot.message_handler(commands=['conversion'])
def operations(message: telebot.types.Message):
    text = 'Актуальные курсы:\n  /pln_to_usd \n  /pln_to_rub \n  /pln_to_eur \n  /usd_to_pln \n  /rub_to_pln \n  /eur_to_pln'
    r1 = requests.get(
        'http://api.nbp.pl/api/exchangerates/rates/a/eur/')  # запрос актуального среднего курса евро нац банка Польши
    texts1 = json.loads(r1.content)  # конвертируем в читаемый формат
    Rates1 = texts1.get('rates')  # убираем лишнее
    EUR1 = str(Rates1[0].get('mid'))
    r2 = requests.get(
        'http://api.nbp.pl/api/exchangerates/rates/a/usd/')  # запрос актуального среднего курса доллара нац банка Польши
    texts2 = json.loads(r2.content)  # конвертируем в читаемый формат
    Rates2 = texts2.get('rates')  # убираем лишнее
    USD1 = str(Rates2[0].get('mid'))

    r3 = requests.get(
        'http://api.nbp.pl/api/exchangerates/rates/a/rub/')  # запрос актуального среднего курса рубля нац банка Польши
    texts3 = json.loads(r3.content)  # конвертируем в читаемый формат
    Rates3 = texts3.get('rates')  # убираем лишнее
    RUB1 = str(Rates3[0].get('mid'))  # выводим только курс  в строковом формате иначе будет ошибка
    Mydict = {
        "eur": "",
        "usd": "",
        "rub": "",
    }
    Mydict["eur"] = EUR1
    Mydict["usd"] = USD1
    Mydict["rub"] = RUB1
    for key in Mydict.keys():
        text = '\n'.join((text, key, '->', Mydict[key]))
    bot.reply_to(message, text)

#а теперь проходим конкретно по конвертациям

#конвертируем злотые в доллары
@bot.message_handler(commands=['pln_to_usd'])
def pln_to_usd(message):
    bot.send_message(message.chat.id, "Введите количесто pln,которые вы хотите конвертировать в usd")
    @bot.message_handler(content_types=['text',])
    def plnusd(message):
        r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/')  # запрос актуального среднего курса доллара нац банка Польши
        texts = json.loads(r.content)  # конвертируем в читаемый формат
        Rates = texts.get('rates')  # убираем лишнее
        USD = Rates[0].get('mid') # наш курс цифрой
        try:
            amount = int(message.text) # конвертируем входящие данные в число
        except:
            bot.send_message(message.chat.id, "Ввели не число")
            return
        total = round((amount/USD),2) # находим нужное количество
        result = f'{amount} pln это {total} usd' # выводим результат
        if type(amount) == str:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        bot.send_message(message.chat.id, result)
        bot.register_next_step_handler(message, operations)



#конвертируем злотые в рубли
@bot.message_handler(commands=['pln_to_rub'])
def pln_to_rub(message):
    bot.send_message(message.chat.id, "Введите количесто pln,которые вы хотите конвертировать в rub: ")
    @bot.message_handler(content_types=['text', ])
    def plnrub(message):
        r4 = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/rub/')  # запрос актуального среднего курса рубля нац банка Польши
        texts4 = json.loads(r4.content)  # конвертируем в читаемый формат
        Rates4 = texts4.get('rates')  # убираем лишнее
        RUB4 = Rates4[0].get('mid')
        try:
            amount4 = int(message.text)
        except:
            bot.send_message(message.chat.id, "Ввели не число")
            return
        total4 = round((amount4/RUB4),2)
        result4 = f'{amount4} pln это {total4} rub'
        if type(amount4) == str:
            raise ConvertionException(f'Не удалось обработать количество {amount4}')
        bot.send_message(message.chat.id, result4)
        bot.register_next_step_handler(message, operations)


#конвертируем злотые в eur
@bot.message_handler(commands=['pln_to_eur'])
def pln_to_eur(message):
    bot.send_message(message.chat.id, "Введите количесто pln,которые вы хотите конвертировать в eur:")
    @bot.message_handler(content_types=['text', ])
    def plneur(message):
        r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/eur/')  # запрос актуального среднего курса eur нац банка Польши
        texts = json.loads(r.content)  # конвертируем в читаемый формат
        Rates = texts.get('rates')  # убираем лишнее
        EUR = Rates[0].get('mid')
        try:
            amount = int(message.text)
        except:
            bot.send_message(message.chat.id, "Ввели не число")
            return
        total = round((amount/EUR),2)
        result = f'{amount} pln это {total} eur'
        bot.send_message(message.chat.id, result)
        bot.register_next_step_handler(message, operations)




#конвертируем доллары в злотые
@bot.message_handler(commands=['usd_to_pln'])
def usd_to_pln(message):
    bot.send_message(message.chat.id, "Введите количесто usd,которые вы хотите конвертировать в pln")
    @bot.message_handler(content_types=['text',])
    def usdpln(message):
        r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/')  # запрос актуального среднего курса доллара нац банка Польши
        texts = json.loads(r.content)  # конвертируем в читаемый формат
        Rates = texts.get('rates')  # убираем лишнее
        USD = Rates[0].get('mid') # наш курс цифрой
        try:
            amount = int(message.text) # конвертируем входящие данные в число
        except:
            bot.send_message(message.chat.id, "Ввели не число")
            return
        total = round((amount * USD),2) # находим нужное количество
        result = f'{amount} usd это {total} pln' # выводим результат
        bot.send_message(message.chat.id, result)
        bot.register_next_step_handler(message, operations)




#конвертируем рубль в злотый
@bot.message_handler(commands=['rub_to_pln'])
def rub_to_pln(message):
    bot.send_message(message.chat.id, "Введите количесто rub,которые вы хотите конвертировать в pln: ")
    @bot.message_handler(content_types=['text', ])
    def rubpln(message):
        r4 = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/rub/')  # запрос актуального среднего курса рубля нац банка Польши
        texts4 = json.loads(r4.content)  # конвертируем в читаемый формат
        Rates4 = texts4.get('rates')  # убираем лишнее
        RUB4 = Rates4[0].get('mid')
        try:
            amount4 = int(message.text)
        except:
            bot.send_message(message.chat.id, "Ввели не число")
            return
        total4 = round((amount4 * RUB4),2)
        result4 = f'{amount4} rub это {total4} pln'
        bot.send_message(message.chat.id, result4)
        bot.register_next_step_handler(message, operations)



#конвертируем eur в злотые
@bot.message_handler(commands=['eur_to_pln'])
def eur_to_pln(message):
    bot.send_message(message.chat.id, "Введите количесто eur,которые вы хотите конвертировать в pln:")
    @bot.message_handler(content_types=['text', ])
    def eurpln(message):
        r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/eur/')  # запрос актуального среднего курса eur нац банка Польши
        texts = json.loads(r.content)  # конвертируем в читаемый формат
        Rates = texts.get('rates')  # убираем лишнее
        EUR = Rates[0].get('mid')
        try:
            amount = int(message.text)
        except:
            bot.send_message(message.chat.id, "Ввели не число")
            return
        total = round((amount * EUR),2)
        result = f'{amount} eur это {total} pln'
        bot.send_message(message.chat.id, result)
        bot.register_next_step_handler(message, operations)



bot.polling(none_stop=True)