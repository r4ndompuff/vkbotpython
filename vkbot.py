import random, vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
vk_session = vk_api.VkApi(token='19ab16e3bc6d67d71f88137cd2a0f50588adad0720966c436813134074cffedab541e11f3a3d6cd42a2e0')
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
longpoll = VkBotLongPoll(vk_session, '203967942')
vk = vk_session.get_api()
from vk_api.longpoll import VkLongPoll, VkEventType
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Привет', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Клавиатура', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_location_button()
keyboard.add_line()
keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=203967942")

def getText(text):
    start = text.find('text') + 8
    end = text.find("'", start)
    return text[start:end]

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        vars = ['Да', 'да', 'дА', 'ДА']
        varss = ['Соси', 'соси']
        if getText(str(event)).lower() == "да":
            if event.from_chat:
                vk.messages.send(
                    key = (''),          #ВСТАВИТЬ ПАРАМЕТРЫ
                    server = (''),
                    ts=(''),
                    random_id = get_random_id(),
              	    message='Пизда.',
            	    chat_id = event.chat_id
                    )
        if getText(str(event)).lower() == "соси":
            if event.from_chat:
                vk.messages.send(
                    key = (''),          #ВСТАВИТЬ ПАРАМЕТРЫ
                    server = (''),
                    ts=(''),
                    random_id = get_random_id(),
                    message='Сам соси.',
                    chat_id = event.chat_id
                    )
        if getText(str(event)).lower() == "нет":
            if event.from_chat:
                vk.messages.send(
                    key = (''),          #ВСТАВИТЬ ПАРАМЕТРЫ
                    server = (''),
                    ts=(''),
                    random_id = get_random_id(),
                    message='Пидора ответ.',
                    chat_id = event.chat_id
                    )
'''
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