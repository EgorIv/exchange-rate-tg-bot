import telebot
from currency import Currency
from apscheduler.schedulers.background import BackgroundScheduler


TOKEN = "8742389615"
bot = telebot.TeleBot(TOKEN)
scheduler = BackgroundScheduler()


exchange_rate = [{"CharCode": "USD", "Value": "76.454", "Name": "Dollar"}, {"CharCode": "EUR", "Value": "89.34543", "Name": "Euro"}]
@bot.message_handler(content_types=['text'])
def get_text_message(message):
    user_input = message.text.strip()
    for item in exchange_rate:
        if item.get("CharCode") == user_input or item.get("Name") == user_input:
            bot.send_message(message.from_user.id, Currency(item.get("CharCode"), item.get("Name"), item.get("Value")).show_currency())
            

bot.polling(none_stop=True, interval=0)