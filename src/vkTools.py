from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import vk_api
import vk
import os
import random

vk_session = vk_api.VkApi(
    token='19ab16e3bc6d67d71f88137cd2a0f50588adad0720966c436813134074cffedab541e11f3a3d6cd42a2e0')
longpoll = VkBotLongPoll(vk_session, '203967942')
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk_session)

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Привет', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Клавиатура', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_location_button()
keyboard.add_line()
keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=203967942")

def uploadPhoto():
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages('photoOut.jpg')
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    os.remove("photoOut.jpg")
    return attachment

def getText(text):
    start = text.find('text') + 8
    end = text.find("'", start)
    return text[start:end]

def fromId(text):
    start = text.find('from_id') + 10
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

def wallGet(event):
    login, password = 'ЛОГИН', 'ПАРОЛЬ' # Сюда логин и пароль от фейк акка, с которого парсить стенку
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    tools = vk_api.VkTools(vk_session)
    wall = tools.get_all('wall.get', 100, {'owner_id': -203127230})
    idW = wall['items'][random.randint(0, len(wall['items']))]['id']
    owner_id = 203127230
    wall_id = f'wall-{owner_id}_{idW}'
    send('', wall_id, event.chat_id)


    