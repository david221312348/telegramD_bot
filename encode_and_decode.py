def enc(message, key):
    alphabet1 = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О",
                 "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]
    alphabet2 = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
                 "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
    full_key = ''
    output = ''
    while len(full_key) < len(message):
        full_key += key
    while len(full_key) != len(message):
        full_key = full_key[0:-1]
    for i in range(len(message)):
        if message[i] in alphabet1 or message[i] in alphabet2:
            output += chr(((ord(message[i]) - 1072) + (ord(full_key[i]) - 1072)) % 32 + 1072)
        else:
            output += message[i]
    return output


def dec(message, key):
    alphabet1 = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О",
                 "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]
    alphabet2 = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
                 "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
    full_key = ''
    unlocked_output = ''
    while len(full_key) < len(message):
        full_key += key
    while len(full_key) != len(message):
        full_key = full_key[0:-1]
    for i in range(len(message)):
        if message[i] in alphabet1 or message[i] in alphabet2:
            unlocked_output += chr(((ord(message[i]) - 1072) - (ord(full_key[i]) - 1072)) % 32 + 1072)
        else:
            unlocked_output += message[i]
    return unlocked_output