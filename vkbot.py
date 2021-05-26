from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from google_trans_new import google_translator
import vk_api
import random
import sys
sys.path.append("./src")
from vkTools import send, getText, fromId, wallGet
from faceSwap import faceChanger
from otherTools import changeTextByArina, estimate, wikiBot
from gpt3 import gpt3
from xlsxTools import getMessage, newCMD

vk_session = vk_api.VkApi(
    token='TOKEN') # Сюда вставить токен на группу
longpoll = VkBotLongPoll(vk_session, '203967942')
vk = vk_session.get_api()
tools = vk_api.VkTools(vk_session)
translator = google_translator() 

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
            elif random.randint(0, 100) > 50:
                send(answer[0], answer[1], chat_id)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        evnt = str(event)
        newMessage = getText(evnt)
        print("Сама команда: ", newMessage)
        idSender = fromId(evnt)
        newMessageLower = newMessage.lower()
        newMessageLower2 = (translator.translate(newMessage, lang_tgt="ru")[:-1]).lower().replace('.', '') # Переведённое сообщение с низкими буквами
        print("Нижняя команда: ", newMessageLower)

        if (newMessage.count(' ') >= 10) and (random.randint(0, 100) > 80):
            changeTextByArina(newMessage, event)
        elif ("бот, оцени" in newMessage): # Оценка
            estimate(newMessage, event)
        elif (newMessageLower[:4] == "гпт3"): # GPT3
            gpt3(newMessage, event)
        elif (newMessageLower[:4] == "вики"): # Wiki
            wikiBot(newMessage[5:], event)
        elif (newMessageLower == "тайлер, цитату"): # Тайлер
            wallGet(event)
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
