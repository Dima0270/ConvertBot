import telebot
from config import keys, TOKEN
from extensions import ConvertException, Convert


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}.\nBot Convert работает в следующем режиме - \nНужно ввести по порядку через пробел: \n'Имя валюты'  'Валюту в которую хотите перевести'  'Количество переводимой валюты' \nПример: рубль доллар 300 \nВы можете увидеть список доступных валют если введёте команду /values")

@bot.message_handler(commands=['values'])
def getvalues(message: telebot.types.Message):
    text = "Доступные валюты - "
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.send_message(message.chat.id, f"{text}")


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        request = message.text.split()

        if len(request) != 3:
            raise ConvertException("Неверное количество параметров ввода")

        currency_start, currency_end, value = request
        currency_start = currency_start.lower()
        currency_end = currency_end.lower()
        ratio = Convert.get_price(currency_start, currency_end, value)
    except ConvertException as e:
        bot.reply_to(message, f"Ошибка пользователя. \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду. \n{e}")
    else:
        res = f"Цена {value} {currency_start} в {currency_end} = {float(value) * ratio}"
        bot.send_message(message.chat.id, res)


bot.polling(none_stop=True)
