from telebot import types



def get_empty():
    return types.ReplyKeyboardRemove()



def get_main():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
    btn_1 = types.KeyboardButton("Парсинг")
    btn_2 = types.KeyboardButton("Ч/Б")
    keyboard.add(btn_1, btn_2)
    return keyboard