import telebot
from telebot import types


def check_user(username, userlist):
    check = False
    for user in userlist:
        if username == user[0]:
            check = True
            break
    return check


def send_mess(nickname, message, users, users_list, bot):
    for i in users_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        butt1 = types.KeyboardButton("Да")
        butt2 = types.KeyboardButton("Нет")
        markup.add(butt1, butt2, row_width=2)
        if message.text == i[0]:

            bot.send_message(i[1],
                             'Пользователь с ником '+'@'+nickname+' отправил вам сообщение: \n'+users[message.from_user.username]['output'],
                             parse_mode='html')
            bot.send_message(i[1],
                             'Хотите ли вы расшифровать данное сообшение?',
                             parse_mode='html',
                             reply_markup=markup)
            users[i[0]]['state'] = 'decode_message'
            users[i[0]]['input'] = users[message.from_user.username]['output']
            print(users)
            break
