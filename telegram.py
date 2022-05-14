# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, SoupStrainer
import time
from selenium import webdriver
import telebot

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)

MainDomain = 'https://induo.store'

def get_pages_links():
    items_pages = []
    ChapterList = ['/bags', '/shoes', '/accessories', '/clothes']
    for Chapter in ChapterList:
        url = MainDomain + Chapter

        browser.get(url)
        time.sleep(2)
        response = browser.page_source

        soup = BeautifulSoup(response, "lxml")

        pageBlocks = soup.find('div', class_='t786').find_all('div',
                                                              class_='js-product t-store__card t-store__stretch-col t-store__stretch-col_33 t-align_left t-item')
        for pageBlock in pageBlocks:
            pages = pageBlock.find_all('a')

            for page in pages:
                p = page.get('href')
                if p[0] == '/':
                    # print(p)
                    pageURL = MainDomain + p
                    items_pages.append({"URL": pageURL, "Chapter": url})

    return len(items_pages)

#########
bot = telebot.TeleBot('5218536240:AAH1egMFH_RVSOLhFZAUgnZCbfHxDJhFhT4')

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, f'Сейчас посчитаю...')
    numPages = get_pages_links()
    bot.send_message(message.chat.id, f'Количество карточек: {numPages}')


# Запускаем бота
bot.polling(none_stop=True, interval=0)