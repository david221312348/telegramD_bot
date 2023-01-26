import telebot
from telebot import types
from funcs import send_mess, check_user
from token import token
alphabet1 =["А","Б","В","Г","Д","Е","Ё","Ж","З","И","Й","К","Л","М","Н","О",
        "П","Р","С","Т","У","Ф","Х","Ц","Ч","Ш","Щ","Ъ","Ы","Ь","Э","Ю","Я"]
alphabet2 = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о",
            "п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"]
users = {}
bot = telebot.TeleBot(token())
users_list = []


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    butt1 = types.KeyboardButton("/startencode")
    butt2 = types.KeyboardButton("/startdecode")
    markup.add(butt1, butt2, row_width=2)
    mess = f'Привет, Я бот который поможет тебе общаться с друзьями шифром Виженера!\n' \
           f'Мои команды:\n' \
           f'/startencode - Зашифровка\n' \
           f'/startdecode - Расшифровка'
    bot.send_message(message.chat.id,
                     mess,
                     parse_mode='html',
                     reply_markup=markup)
    users.update({message.from_user.username: {'state': 'default',
                                               'input': '',
                                               'output': '',
                                               'unlocked_output': '',
                                               'encode_key': '',
                                               'decode_key': '',
                                               }})
    with open(r'C:\Users\Home-PC\PycharmProjects\telegramD_bot\users.txt', mode='r') as file:
        lines = file.readlines()
        for i in lines:
            users_list.append(i.replace('\n', '').split(' : '))
    with open(r'C:\Users\Home-PC\PycharmProjects\telegramD_bot\users.txt', mode='a')as file:
        if not check_user(message.from_user.username, users_list):
            print(f'{message.from_user.username} : {message.chat.id}', file=file)
    print(users)


@bot.message_handler(commands=['startencode'])
def encode(message):
    try:
        markup = types.ReplyKeyboardRemove()
        users[message.from_user.username]['state'] = 'encode'
        print(users)
        bot.send_message(message.chat.id,
                         f'Введите слово для зашифровки.',
                         parse_mode='html',
                         reply_markup=markup
                         )
    except KeyError:
        bot.send_message(message.chat.id,
                         f'Для начала введите команду /start !',
                         parse_mode='html')


@bot.message_handler(commands=['startdecode'])
def decode(message):
     try:
        markup = types.ReplyKeyboardRemove()
        users[message.from_user.username]['state'] = 'decode'
        bot.send_message(message.chat.id,
                         f'Введите слово для расшифровки.',
                         parse_mode='html',
                         reply_markup=markup
                         )
     except KeyError:
         bot.send_message(message.chat.id,
                          f'Для начала введите команду /start! ',
                          parse_mode='html')


@bot.message_handler(content_types=['text'])
def text(message):
    try:
        if users[message.from_user.username]['state'] == 'encode_key':
            full_key = ''
            users[message.from_user.username]['encode_key'] = message.text
            print(users)
            while len(full_key) < len(users[message.from_user.username]['input']):
                full_key += users[message.from_user.username]['encode_key']
            while len(full_key) != len(users[message.from_user.username]['input']):
                full_key = full_key[0:-1]
            for i in range(len(users[message.from_user.username]['input'])):
                if users[message.from_user.username]['input'][i] in alphabet1 or users[message.from_user.username]['input'][i] in alphabet2:
                   users[message.from_user.username]['output'] += chr(((ord(users[message.from_user.username]['input'][i]) - 1072) + (ord(full_key[i]) - 1072)) % 32 + 1072)
                else:
                    users[message.from_user.username]['output'] += users[message.from_user.username]['input'][i]
            bot.send_message(message.chat.id,
                             'Зашифрованное сообщение: \n'+users[message.from_user.username]['output'],
                             parse_mode='html')
            users[message.from_user.username]['input'] = ''
            users[message.from_user.username]['encode_key'] = ''
            users[message.from_user.username]['state'] = 'default'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            butt1 = types.KeyboardButton("Да")
            butt2 = types.KeyboardButton("Нет")
            markup.add(butt1, butt2, row_width=2)
            bot.send_message(message.chat.id,
                             f'Хотите ли вы отправить это сообщение кому-нибудь?',
                             parse_mode='html',
                             reply_markup=markup
                             )
            users[message.from_user.username]['state'] = 'sending'
            print(users)
        elif users[message.from_user.username]['state'] == 'encode':
            users[message.from_user.username]['input'] = message.text
            print(users)
            bot.send_message(message.chat.id,
                             f'Введите ключ для зашифровки сообщения.',
                             parse_mode='html')
            users[message.from_user.username]['state'] = 'encode_key'
        elif users[message.from_user.username]['state'] == 'sending':
            if message.text.lower() == 'да':
                markup = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id,
                                f'Введите ник пользователя, которому хотите отправить сообщение.',
                                parse_mode='html',
                                reply_markup=markup
                                )
                users[message.from_user.username]['state'] = 'getting_username'
            elif message.text.lower() == 'нет':
                users[message.from_user.username]['state'] = 'default'
                users[message.from_user.username]['output'] = ''
            else:
                bot.send_message(message.chat.id,
                                 f'Введите Да или Нет!',
                                 parse_mode='html')
            print(users)
        elif users[message.from_user.username]['state'] == 'decode_message':
            if message.text.lower() == 'да':
                markup = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id,
                                 f'С помощью какого слова-ключа хотите расшифровать сообщение?',
                                 parse_mode='html',
                                 reply_markup=markup)
                users[message.from_user.username]['state'] = 'decode_key'
                users[message.from_user.username]['output'] = ''
            elif message.text.lower() == 'нет':
                users[message.from_user.username]['state'] = 'default'
            else:
                bot.send_message(message.chat.id,
                                 f'Введите Да или Нет!',
                                 parse_mode='html')
        elif users[message.from_user.username]['state'] == 'getting_username':
            if check_user(message.text, users_list):
                nickname = message.from_user.username
                send_mess(nickname, message, users, users_list, bot)
            else:
                bot.send_message(message.chat.id,
                                 f'Нельзя отправить сообщение данному пользоателю.',
                                 parse_mode='html')
                users[message.from_user.username]['state'] = 'default'
        elif users[message.from_user.username]['state'] == 'decode_key':
            full_key = ''
            users[message.from_user.username]['decode_key'] = message.text
            print(users)
            while len(full_key) < len(users[message.from_user.username]['input']):
                full_key += users[message.from_user.username]['decode_key']
            while len(full_key) != len(users[message.from_user.username]['input']):
                full_key = full_key[0:-1]
            for i in range(len(users[message.from_user.username]['input'])):
                if users[message.from_user.username]['input'][i] in alphabet1 or users[message.from_user.username]['input'][i] in alphabet2:
                    users[message.from_user.username]['unlocked_output'] += chr(((ord(users[message.from_user.username]['input'][i]) - 1072) - (ord(full_key[i]) - 1072)) % 32 + 1072)
                else:
                    users[message.from_user.username]['unlocked_output'] += users[message.from_user.username]['input'][i]
            bot.send_message(message.chat.id,
                             'Расшифрованное сообщение: \n'+users[message.from_user.username]['unlocked_output'],
                             parse_mode='html')
            users[message.from_user.username]['unlocked_output'] = ''
            users[message.from_user.username]['input'] = ''
            users[message.from_user.username]['decode_key'] = ''
            users[message.from_user.username]['state'] = 'default'
        elif users[message.from_user.username]['state'] == 'decode':
            users[message.from_user.username]['input'] = message.text
            print(users)
            bot.send_message(message.chat.id,
                             f'Введите ключ для расшифровки сообщения.',
                             parse_mode='html')
            users[message.from_user.username]['state'] = 'decode_key'
        elif users[message.from_user.username]['state'] == 'default':
            bot.send_message(message.chat.id,
                             message.text,
                             parse_mode='html')
        else:
            bot.send_message(message.chat.id,
                             f'Для начала введите команду /start !',
                             parse_mode='html')
    except KeyError:
            bot.send_message(message.chat.id,
                             f'Для начала введите команду /start !',
                             parse_mode='html')


bot.polling(none_stop=True)