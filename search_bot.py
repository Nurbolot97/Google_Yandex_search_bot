import lxml
import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
from time import sleep
from selenium import webdriver
from decouple import config
from klaviatura import start_nastroenie_klaviatura
from klaviatura import glavnoe_okno


bot = telebot.TeleBot(config('TOKEN'))
driver = webdriver.Firefox()

@bot.message_handler(commands=['start'])
def start_say_greeting(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Здравствуйте!")
    bot.send_message(chat_id, "Как ваше настроение?", reply_markup=start_nastroenie_klaviatura)

@bot.message_handler(commands=['next'])
def start_next(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Вы в главном окне \U0001F192", reply_markup=glavnoe_okno)
    bot.register_next_step_handler(msg, to_menu)

@bot.message_handler(commands=['help'])
def to_help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Здравствуйте, этот бот предназначен для поиска \nинформации по вашему запросу. \nЭтот бот объединил в себя такие поисковики \nкак Google, Yandex и Youtube для поиска видео. Для старта нажмите /start")
    
@bot.callback_query_handler(func=lambda call:True)
def process_callback_button1(call):
    code = call.data
    if code == "1":
        chat_id = call.message.chat.id
        msg = bot.send_message(chat_id, "Хорошо, выберите поисковик \U00002705", reply_markup=glavnoe_okno)
        bot.register_next_step_handler(msg, to_menu)
    elif code == "2":
        chat_id = call.message.chat.id
        f = open('anekdoty.txt')
        bot.send_message(chat_id, "Не расстраивайтесь! Специально для вас анекдоты... \U0001F609")
        bot.send_message(chat_id, f.read())
        msg = bot.send_message(chat_id, "Надеюсь наши анекдоты были смешными,\n если хотите продолжить нажмите нужное \U00002B07", reply_markup=glavnoe_okno)
        bot.register_next_step_handler(msg, to_menu)
    elif code == "3":
        chat_id = call.message.chat.id
        bot.send_message(chat_id, "До новых встреч!")

def to_menu(message):
    if message.text == "Google":
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, "Отлично, напишите чего хотите поискать \U0000270F")
        bot.register_next_step_handler(msg, poisk_google)
    elif message.text == "Yandex":
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, "Отлично, напишите чего хотите поискать \U0000270F")
        bot.register_next_step_handler(msg, poisk_yandex)
    elif message.text == "Youtube":
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, "Отлично, напишите чего хотите поискать \U0000270F")
        bot.register_next_step_handler(msg, poisk_youtube)
    elif message.text == "Выйти \U000026D4":
        chat_id = message.chat.id
        bot.send_message(chat_id, "Сожалеем что вы уходите ...")
        bot.send_message(chat_id, "До новых встреч!")
    else:
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, 'Вы в главном окне \U0001F192', reply_markup=glavnoe_okno)
        bot.register_next_step_handler(msg, to_menu)

def poisk_google(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Отлично, начинаю поиск ...")
    google = 'https://www.google.com/search?q=' + message.text
    driver.get(google)
    sleep(2)
    ssylki = driver.find_elements_by_tag_name('a')
    global otvety_google 
    otvety_google = []
    for i in range(len(ssylki)):
        otvety_google.append(ssylki[i].get_attribute('href'))
            
    def get_write_google():
        with open('google.txt', 'w') as f:
            for index in otvety_google[35:50:]:
                f.write('#))' + index + '\n')
    get_write_google()
    f = open('google.txt') 
    bot.send_message(chat_id, f"{f.read()}\n")
    bot.send_message(chat_id, "Надеюсь эти ссылки Вам помогут \U0001F609")
    bot.send_message(chat_id, "Для продолжения нажмите /next")

def poisk_yandex(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Отлично, начинаю поиск ...")
    chat_id = message.chat.id
    yandex = 'https://yandex.ru/search/?lr=10309&text=' + message.text
    driver.get(yandex)
    sleep(2)
    ssylki1 = driver.find_elements_by_tag_name('a')
    global otvety_yandex 
    otvety_yandex = []
    for i in range(len(ssylki1)):
        otvety_yandex.append(ssylki1[i].get_attribute('href'))

    def get_write_yandex():
        with open('yandex.txt', 'w') as f:
            for index in otvety_yandex[35:50:]:
                f.write('#))' + index + '\n')
    get_write_yandex()
    f = open('yandex.txt') 
    bot.send_message(chat_id, f"{f.read()}\n")
    bot.send_message(chat_id, "Надеюсь эти ссылки Вам помогут \U0001F609")
    bot.send_message(chat_id, "Для продолжения нажмите /next")

def poisk_youtube(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Отлично, начинаю поиск ...")
    youtube = 'https://www.youtube.com/results?search_query=' + message.text
    driver.get(youtube)
    sleep(2)
    ssylki2 = driver.find_elements_by_id('video-title')
    for i in range(len(ssylki2)):
        bot.send_message(chat_id, f"{ssylki2[i].get_attribute('href')}")
        if i == 10:
            break
    bot.send_message(chat_id, "Надеюсь эти видео Вам помогут \U0001F609")
    bot.send_message(chat_id, "Для продолжения нажмите /next")

def get_html(url):
    r = requests.get(url)
    return r.text

def get_soup(html):
    soup = BeautifulSoup(html, 'lxml')
    result = soup.find('div', class_= 'content').find_all('div', class_='text')
    global wutki_list
    wutki_list = []
    for i in result[:15:]:
        try:
            global wutki
            wutki = i.text.strip()
            wutki_list.append(wutki)
        except:
            print("Something went wrong")

def get_write():
    with open('anekdoty.txt', 'w') as f:
        for index in wutki_list:
            f.write('#)' + index + '\n')

def main():
    url = 'https://nekdo.ru/short/'
    get_soup(get_html(url))
    get_write()
    
if __name__ == '__main__':
    main()
    bot.polling()
    
