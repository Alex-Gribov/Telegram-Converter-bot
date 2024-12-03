#bot.py
import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = """
    Привет! Я бот для конвертации валют.  Поддерживаются следующие валюты: доллар, евро, рубль.

    Введите команду в формате: <валюта_из> <валюта_в> <количество>
    Например: доллар рубль 10  (10 долларов в рублях)
    /values - список доступных валют (пока не реализовано)
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['values'])
def values(message):
    bot.reply_to(message, "Список доступных валют пока не реализован. Используйте: доллар, евро, рубль")

@bot.message_handler(content_types=['text'])
def get_currency_price(message):
    try:
        base, quote, amount_str = message.text.split()

        if not amount_str.replace('.', '', 1).isdigit():
            raise APIException('Некорректное количество валюты. Используйте число.')

        amount = float(amount_str)
        if amount <= 0:
            raise APIException('Количество валюты должно быть больше нуля.')

        total = CurrencyConverter.get_price(base, quote, amount)
        bot.reply_to(message, f'{amount} {base} стоит {total:.2f} {quote}.')

    except ValueError:
        bot.reply_to(message, 'Ошибка: Неверный формат запроса. Используйте формат "<валюта_из> <валюта_в> <количество>". Пример: доллар евро 10')
    except APIException as e:
        bot.reply_to(message, f'Ошибка: {str(e)}')
    except Exception as e:
        bot.reply_to(message, f"Произошла неизвестная ошибка: {type(e).__name__}")

bot.polling(none_stop=True)
