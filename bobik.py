import telebot
from currency import Currency
from apscheduler.schedulers.background import BackgroundScheduler
import xml.etree.ElementTree as ET
import requests

bot = telebot.TeleBot(TOKEN)
scheduler = BackgroundScheduler()
url = "https://www.cbr.ru/scripts/XML_daily.asp"
users = set()

exchange_rate = {}


def update_rates():
    response = requests.get(url)
    root = ET.fromstring(response.text)
    exchange_rate.clear()

    for valute in root.findall("Valute"):
        code = valute.find("CharCode").text
        nominal = int(valute.find("Nominal").text)
        value = float(valute.find("Value").text.replace(",", "."))
        rate = value / nominal

        exchange_rate[code] = Currency(
            code,
            valute.find("Name").text,
            rate            
        )
    print(exchange_rate)
update_rates()

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    user_input = message.text.strip().upper()
    users.add(message.chat.id) 

    if user_input == "/HELP":
        text = "Валюты: \n" + " ".join(exchange_rate.keys())
        bot.send_message(message.from_user.id, text)
        return

    if exchange_rate[user_input]:
        bot.send_message(message.from_user.id, exchange_rate[user_input].show_currency())


#рассылка в 12 часов
def send_to_users():
    usd = exchange_rate["USD"]
    eur = exchange_rate["EUR"]
    text = f"{usd.show_currency()}\n{eur.show_currency()}"
    print(text)
    print(users)
    for user in users:
        bot.send_message(user, text)


scheduler.add_job(update_rates, 'cron', hour=12, minute=0)
scheduler.add_job(send_to_users, 'cron', hour=13, minute=24)
scheduler.start()
        
bot.polling(none_stop=True, interval=0)