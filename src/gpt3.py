import requests
from vkTools import send

def gpt3(message, event):
    headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            }
    text = message[5:].replace('\'', '')
    print("Текст в гпт: ", text)
    data = '{"text":"'+text.replace('"','')+'"}'
    response = requests.post('https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict', headers=headers, data=data.encode('utf-8'))
    while ("504 Gateway Time-out" in response.text):
        response = requests.post('https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict', headers=headers, data=data.encode('utf-8'))
    text = response.text[16:-2].replace('\\n', '').replace('\\', '')
    send(text, '', event.chat_id)