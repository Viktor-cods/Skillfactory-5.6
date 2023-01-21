import telebot
from seting import keys,TOKEN
from extensions import APIException,ValutConverter
import traceback

bot=telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start','help'])
def pusk(message: telebot.types.Message):
    text='Чтобы начать работу введите боту данные в следующем виде:' \
     '' \
     '<имя валюты, цену которой вы хотите узнать> ' \
     '<имя валюты, в которой надо узнать цену первой валюты> ' \
     '<количество первой валюты>' \
     'Увидеть доступный список валют : /values'
    bot.send_message(message.chat.id, text)



@bot.message_handler(commands=['values'])
def dost_val(message: telebot.types.Message):
    text='Доступные валюты :'
    for key in keys:
      text='\n'.join((text,key))
    bot.reply_to(message,text)


@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
          values = message.text.split(' ')
          total_base = ValutConverter.get_price(*values)
          if len(values) != 3:
            raise  APIException('Неверное количество параметров!')

    except APIException as e:
            bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
            traceback.print_tb(e.__traceback__)
            bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
            bot.reply_to(message, total_base)



bot.polling()
