from telebot import types

start_nastroenie_klaviatura = types.InlineKeyboardMarkup(row_width=2)
button1 = types.InlineKeyboardButton("Отлично \U0001F60A", callback_data="1")
button2 = types.InlineKeyboardButton("Так себе \U0001F614", callback_data="2")
button3 = types.InlineKeyboardButton("Выйти \U000026D4", callback_data="3")
start_nastroenie_klaviatura.add(button1, button2, button3)

glavnoe_okno = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
knopka = types.KeyboardButton("Google")
knopka1 = types.KeyboardButton("Yandex")
knopka2 = types.KeyboardButton("Youtube")
knopka3 = types.KeyboardButton("Выйти \U000026D4")
glavnoe_okno.add(knopka, knopka1, knopka2, knopka3)















