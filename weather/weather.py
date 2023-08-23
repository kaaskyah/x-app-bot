import telebot
import requests
import json

bot = telebot.TeleBot('6473370618:AAG2VOUwsOSePUMC4ggTzi48t3SmT2CCJXw')
API = '1320f250f331be3ebbd40185f2507bd3'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, рад тебя видеть! Напиши название города')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = int(data["main"]["temp"])
        bot.reply_to(message, f'Сейчас погода: {temp}°C')

        image = 'sunny.png' if temp > 5.0 else 'cloudy.png'
        file = open('weather/' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан неверно')


bot.polling(none_stop=True)
