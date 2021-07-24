from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import re
import vk_api
import vk
import os
import random
import requests
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io

vk_session = vk_api.VkApi(
    token='ТОКЕН')
longpoll = VkBotLongPoll(vk_session, 'АЙДИ')
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk_session)

def uploadPhoto(name='photoOut.jpg'):
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(name)
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    os.remove(name)
    return attachment

def getText(text):
    start = text.find('text') + 8
    end = text.find("'", start)
    return text[start:end]

def fromId(text):
    start = text.find('from_id') + 10
    end = text.find(",", start)
    return text[start:end]

def localMesId(text):
    start = text.find('conversation_message_id') + len('conversation_message_id') + 3
    end = text.find(",", start)
    return text[start:end]

def send(text, attachment, chat_id):
    vk.messages.send(
                    key=(''),
                    server=(''),
                    ts=(''),
                    message=text,
                    chat_id=chat_id,
                    attachment=attachment,
                    random_id=get_random_id()
                   )

def getFake(i):
    i = i % 9
    file = open("accounts.txt", "r")
    f = file.readlines()
    logpass = f[i].split(':')
    print(logpass)
    return [logpass[0], logpass[1].strip()]

captcha_sid = 0
captcha_ans = 0

def captchaSolver(captcha, event):
    captcha_sid = captcha.sid # Получение sid
    url = captcha.get_url() # Получить ссылку на изображение капчи
    img = captcha.get_image() # Получить изображение капчи (jpg)
    stream = io.BytesIO(img)
    img = Image.open(stream)
    draw = ImageDraw.Draw(img)
    img.save("captcha.png")
    img = uploadPhoto("captcha.png")
    send("Введите каптчу: ", img, event.chat_id)
    #time.sleep(5)
    #send("Шучу, не вводите, я не придумал, как это обрабатывать.",'', event.chat_id)
    return captcha

def wallGet(gr_id, event):
    print("2: ", captcha_sid)
    try:
        int(gr_id)
    except:
        send("Вам нужен именно айди группы, взять его можно, например, отсюда: https://regvk.com/id/", '', event.chat_id)
    login, password = getFake(0)
    vk_session = vk_api.VkApi(login, password)
    wall = '1'
    i = 0
    while (wall == '1') and (i <= 9):
        try:
            try:
                vk_session.auth(token_only=True)
                tools = vk_api.VkTools(vk_session)
                wall = tools.get_all('wall.get', 100, {'owner_id': int('-'+gr_id)})
                idW = wall['items'][random.randint(0, len(wall['items']))]['id']
                owner_id = int(gr_id)
                wall_id = f'wall-{owner_id}_{idW}'
                send('', wall_id, event.chat_id)
                break
            except vk_api.exceptions.Captcha as captcha:
            	return captchaSolver(captcha, event)
        except vk_api.AuthError as error_msg:
            i += 1
            login, password = getFake(i)
            vk_session = vk_api.VkApi(login, password)

def modMessage(message):
    if (message != ''):
        if message[0] == ' ':
            message = message[1:]
        if (message[:4] == 'гпт3') or (message[:4] == 'gpt3'):
            message = message[5:]
        while ('[' in message) and (']' in message):
            if message[0] == '[':
                message = message[message.find(']')+1:]
            elif (message[len(message)-1] == ']'):
                message = message[:message.find('[')]
            else:
                message = message[:message.find('[')-1]+message[message.find(']')+1:]
        message = message.replace('тайлер, цитату', '')
        message = message.replace('викто марков', '')
        message = message.lower()
        message = re.sub('[^а-я ]+', '', message)
        message = " ".join(message.split())
        if (len(message)>0) and (message[0] == ' '):
            message = message[1:]
        return message
    return ''


    