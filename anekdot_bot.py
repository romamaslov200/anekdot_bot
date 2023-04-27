import random
import telebot
from telebot import *


#
import requests
from bs4 import BeautifulSoup
# наша страница на которую мы отправляем запрос
url = 'https://www.anekdotov-mnogo.ru/anekdoti_userov.php'
#url = 'https://eldvor.ru/electronics/pribory-ucheta/'
# словарь с заголовками
headers = {'user-agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
html = response.text
soup = BeautifulSoup(html, 'lxml')
# находим количество страниц
pages = '210'
print('Всего страниц: ' + pages)
# проходимся по всем страницам и получаем данные
data = []
def parser(url, headers, response, html, soup, pages):
    for page in range(1, int(pages)+1):
        # передаем наши headers и params, где params словарь с параметром ключ:значение)
        response = requests.get(url, headers=headers, params={'page': page})
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        blocks = soup.find_all('div', class_='tmpLineUnderContent tmpPaddingContent')
        print(f'Парсинг страницы {page} из {pages}...')
        for block in blocks:
            try:
                data.append({
                    block.find('p').get_text("\n"),
                })
            except:
                 print("") 
    print('Получили ' + str(len(data)) + ' позиций')
    print("\n")
    return data
#


list_of_jokets = parser(url, headers, response, html, soup, pages)
print(list_of_jokets)
random.shuffle(list_of_jokets)

TOKEN = '6120629335:AAF8ERXPC7rCzWccZbKwi1WxODAzqBPObx8'
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("😜Анекдот😜")
    item2=types.KeyboardButton("📝Помощь📝")
    markup.add(item1,item2)

    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEIqtVkQk6jdnyn7TbwMgoHgmirbLFdkwACpwIAAvEElxNzELAdFfmXJS8E')
    bot.send_message(message.chat.id,'❗Привет ' + message.from_user.first_name + "❗\n😜Ты попал в Anekdot Bot😜\n😁Который поможет тебе весело провести время😁", reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="📝Помощь📝":
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1=types.KeyboardButton("😜Анекдот😜")
                item2=types.KeyboardButton("📝Помощь📝")
                markup.add(item1,item2)
                bot.send_message(message.chat.id,'❗Привет ' + message.from_user.first_name + "❗\n😜Ты попал в Anekdot Bot😜\n😁Он поможет тебе весело провести время😁", reply_markup=markup)

    elif message.text=="😜Анекдот😜" or message.text=="/anecdote":
        try:
            if range(0, 9):
                global list_of_jokets
                bot.send_message(message.chat.id, list_of_jokets[0])
                print(message.from_user.username)
                print(list_of_jokets[0])
                del list_of_jokets[0]
            else:
                bot.send_message(message.chat.id, "Ошибка")
        except:
            bot.send_message(message.chat.id, "Пожалуйста подождите...")
            list_of_jokets = parser(url, headers, response, html, soup, pages)
            print(list_of_jokets)
            random.shuffle(list_of_jokets)

bot.polling()