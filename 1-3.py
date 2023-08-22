import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot('6473370618:AAG2VOUwsOSePUMC4ggTzi48t3SmT2CCJXw')

# Oткрыть сайт
@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://www.youtube.com/')

# Команда старт ДОБАВИТЬ
@bot.message_handler(commands=['main', 'hello'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!')

# Команда помощь
@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Что умеет этот бот: Ничего</b>', parse_mode='html')

# Кнопки сразу со старта бота
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Удалить фото')
    btn3 = types.KeyboardButton('Изменить текст')
    markup.row(btn2, btn3)
    file = open('./photo.jpg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    # bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
    # bot.send_audio(message.chat.id, 'Привет', reply_markup=markup)
    # bot.send_video(message.chat.id, 'Привет', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, "Website is open")
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, "Deleted")

# Ответ на фото, и кнопками снизу
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://www.youtube.com/')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)

    # или так
    # markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://www.youtube.com/'))
    # markup.add(types.InlineKeyboardButton('Удалить фото', callback_data='delete'))
    # markup.add(types.InlineKeyboardButton('Изменить текст', callback_data='edit'))

    bot.reply_to(message, 'Красивое фото!', reply_markup=markup)

# Функции удалить и редактировать
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

# Обычные сообщения и что на них должен ответить бот
@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!')
    elif message.text.lower() == 'id' or message.text.lower() == '/id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    else:
        bot.send_message(message.chat.id, 'Не понял')

# Чтобы бот не закрывался
bot.polling(none_stop=True)