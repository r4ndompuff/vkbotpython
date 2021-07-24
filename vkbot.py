from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from google_trans_new import google_translator
import vk_api
import random
import sys
import os
import requests
sys.path.append("./src")
from vkTools import send, getText, fromId, wallGet, modMessage
from faceSwap import faceChanger
from otherTools import changeTextByArina, estimate, wikiBot
from gpt3 import gpt3
from xlsxTools import getMessage, newCMD
from markov import Markov
from aboba import getYAML

from vk_api.utils import get_random_id

vk_session = vk_api.VkApi(
    token='ТОКЕН')
longpoll = VkBotLongPoll(vk_session, 'АЙДИ')
vk = vk_session.get_api()
tools = vk_api.VkTools(vk_session)
translator = google_translator()
captcha = 0

def adminCMD(text, evnt):
    newCMD(text, evnt)

def staticCMD(text, idS, chat_id):
    answer = getMessage(text)
    print("Ответ: ", answer)
    if answer[0] != "None":
        if answer[2] != '':
            if answer[2] == idS:
                send(answer[0], answer[1], chat_id)
        else:
            if answer[3] == True:
                send(answer[0], answer[1], chat_id)
            elif random.randint(0, 100) > 80:
                send(answer[0], answer[1], chat_id)

def decodeFun(text, chat_id):
    file = open('dict/sortWords.txt', 'r')  
    lines = file.readlines()
    message = ''
    for i in range(len(text)):
        wordsLetter = [value for value in lines if value[0] == text[i].lower()]
        message += text[i] + ' - ' + wordsLetter[random.randint(0, len(wordsLetter)-1)]
    send(message,'',chat_id)
    
def moisha(text):
    text = modMessage(text)
    if ((text != '') and not ("http" in text) and (len(text) > 1)):
        file = open('dict/messages.txt', 'a')
        file.write(text+'\n')
        file.close()

def moishaMarkov(text, chat_id):
    message = markov(text)
    send(message,'',chat_id)

def agro(text, chat_id):
    if ("club203967942" in text):
        send('Нихуя ты умный, пошёл нахуй!', '', chat_id)
        return
    phrases = ['Как говорил мой дед: "Любишь кататься - катись на хуй '+text+'"',
            'Да, я могу допускать ошибки в тексте. Но какие же они пиздатые, что так и ебут тебя в глаза, как сучку. '+text, 
            'Ноги есть, '+text+'? Тогда съебался нахуй.','Извини, но мама учила меня не разговаривать с таким говном, как '+text+'.',
            text+', ты как муравей, несёшь всякую хуйню.', 
            text+', ты всегда так глуп или сегодня особый случай?',
            'Я видел людей, как '+text+', но тогда мне надо было заплатить за билет в цирк.',
            text+', кто поджёг запал на твоём тампоне?',
            text+', тебе не хватает тампона во рту, потому что если собираешься вести себя, как пизда, то выгляди соотвествующе.',
            text+', шокируй меня. Скажи что-нибудь умное.',
            text+', не знаю, что делает тебя таким дебилом. Однако это точно работает.',
            'Бог создал горы, Бог создал деревья, Бог создал '+text+', но все мы совершаем ошибки.',
            text+', клуб мазохизма на два этажа ниже...']
    send(random.choice(phrases),'',chat_id)


def textToEmoji(text, chat_id):
    headers = {
        'authority': 'textgenerator.ru',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
        'origin': 'https://textgenerator.ru',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://textgenerator.ru/font/emoji',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_ym_uid=1624568435313291772; _ym_d=1624568435; _ym_isad=1',
        'dnt': '1',
        'sec-gpc': '1',
    }

    data = {
      'text': text
    }

    response = requests.post('https://textgenerator.ru/font/emoji/ajax', headers=headers, data=data)
    send(response.text,'',chat_id)


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        #print(event.message_id)
        evnt = str(event)
        
        #print(evnt)
        newMessage = getText(evnt)
        print("Сама команда: ", newMessage)
        print(evnt)
        if "Введите каптчу:" in evnt:
            print("Попало сюда")
            captcha.try_again(newMessage)
        idSender = fromId(evnt)
        newMessageLower = newMessage.lower()
        
        print("Нижняя команда: ", newMessageLower)

        if idSender == "90662083":
            moisha(newMessageLower)
        if (newMessage.count(' ') >= 10) and (random.randint(0, 100) == 1):
            changeTextByArina(newMessage, event)
        if ("бот, оцени" in newMessage): # Оценка
            estimate(newMessage, event)
        elif newMessageLower[:5] == '/roll':
            if len(newMessageLower) == 5:
                send(str(random.randint(0,10)),'', event.chat_id)
            else:
                fd = newMessageLower[6:newMessageLower.find('-')]
                sd = newMessageLower[newMessageLower.find('-')+1:]
                if (fd.isdigit()) and (sd.isdigit()):
                    fd = int(fd)
                    sd = int(sd)
                    if (fd < sd):
                        send(str(random.randint(fd,sd)),'', event.chat_id)
                    else:
                        send('Хочешь наебать меня, дешёвка?','',event.chat_id)
                else:
                    send('Хочешь наебать меня, дешёвка?','',event.chat_id)
        elif (newMessageLower[:12] == "мойша марков"):
            n = newMessageLower[13:]
            if n.isdigit():
                n = int(n)
                if (n<1) or (n>9):
                    send('Неверный размер окна, иди нахуй, дешёвка', '', event.chat_id)
                else:
                    moysha = Markov('dict', n)
                    answer = moysha.generate(n)
                    send(answer, '', event.chat_id)
            else:
                moysha = Markov('dict', 4)
                answer = moysha.generate(query=newMessageLower[13:])
                send('> ' + newMessageLower[13:].capitalize()+'\n> ' + answer, '', event.chat_id)
        elif (random.randint(0, 10) <= -3) and (newMessageLower[-1] == '?'):
            send('Мойша услышал Ваш вопрос... Мойша думает...', '', event.chat_id)
            moysha = Markov('dict', 4)
            answer = moysha.generate(query=newMessageLower[:-1])
            send('> ' + newMessageLower.capitalize()+'\n> ' + answer, '', event.chat_id)
        elif (newMessageLower[:9] == "расшифруй"): # Расшифровка
            print(event.chat_id)
            decodeFun(newMessageLower[10:], event.chat_id)
        elif (newMessageLower[:len("текст в эмодзи")] == "текст в эмодзи"):
            textToEmoji(newMessageLower[len("текст в эмодзи")+1:], event.chat_id)
        elif (newMessageLower[:14] == 'бот, быкани на'):
            agro(newMessageLower[15:], event.chat_id)
        elif (newMessageLower[:5] == 'абоба'):
            try:
                text = getYAML(newMessageLower[8:], newMessageLower[6])
                send("🅰🅱🅾🅱🅰: " + text,'', event.chat_id)
            except:
                send("Ошибка ввода для абобы", '', event.chat_id)
        elif (newMessageLower[:4] == "гпт3"): # GPT3
            gpt3(newMessage, event)
        elif (newMessageLower[:4] == "вики"): # Wiki
            wikiBot(newMessage[5:], event)
        elif (newMessageLower == "тайлер, цитату"): # Тайлер
            #send("Больше парсить группы нельзя, скажите спасибо обнове vk для разрабов.",'', event.chat_id)
            captcha = wallGet("203127230", event)
        elif (newMessageLower == "томас, цитату"): # Тайлер
            #send("Больше парсить группы нельзя, скажите спасибо обнове vk для разрабов.",'', event.chat_id)
            captcha = wallGet("194937912", event)
        elif (newMessageLower == "че там у фемок?"): # Тайлер
            #send("Больше парсить группы нельзя, скажите спасибо обнове vk для разрабов.",'', event.chat_id)
            captcha = wallGet("72036785", event)
        elif newMessage == "бот держи два фото": # FaceSwap
            faceChanger(evnt, event)
        elif (idSender == "50990514") and (newMessage[:5] == "админ"): # Admin
            adminCMD(newMessage[6:], event)
        else: # Табличные команды
            staticCMD(newMessageLower, idSender, event.chat_id)


''' Это на будущее, чтобы он в личку отвечал
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()
for event in Lslongpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        vars1 = ['Привет', 'Ку', 'Хай', 'Хеллоу']
        if event.text in vars1:
            if event.from_user:
                Lsvk.messages.send(
                    user_id = event.user_id,
                    message = 'Привет)',
                    random_id = get_random_id()
                    )
        vars2 = ['Клавиатура', 'клавиатура']
        if event.text in vars2:
            if event.from_user:
                Lsvk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    keyboard = keyboard.get_keyboard(),
                    message = 'Держи'
                    )
'''
