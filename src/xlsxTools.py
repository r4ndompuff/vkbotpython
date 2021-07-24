import pandas as pd
import random
from openpyxl import load_workbook
from vkTools import send

# Упаковываем сообщение
def packMessage(row):
	text = row["Message"]
	att = row["Attachment"]
	Id = row["Id"]
	alwAns = row["Always answer"]
	message = []
	if text != "Null": # Собираем отправляемый текст
		if row["Random answer"] == False: # Проверяем на то должен ли быть случайный ответ (случайный текст)
			message.append(text.replace("\\n","\n"))
		else:
			text = text.split(';')
			k = random.randint(1, len(text)) - 1
			message.append(text[k])
	else:
		message.append('')
	if att != "Null": # Собираем отправляемые приложения (фото, видио, аудио, документы)
		combAtt = att.split(", ")
		message.append(f'{combAtt[0]}{combAtt[1]}_{combAtt[2]}')
	else:
		message.append('')
	if  Id != "Null": # Собираем айди к которому привязана команда (то есть, чтобы реагировало только на 1 человека)
		message.append(Id)
	else:
		message.append('')
	message.append(alwAns) # Узнаём всегда ли бот должен реагировать на эту команду
	return(message)

# Получаем ответ на команду
def getMessage(text):
	df = pd.read_excel("./commands.xlsx")
	for i in range(len(df["Command"])):
		cmds = str(df["Command"][i]).split(', ')
		for cmd in cmds:
			if ((text == cmd) and (df["Fully include"][i] == True)) or ((cmd in text.replace(',','').split(' ')) and (df["Fully include"][i] == False)): # Нашли команду
				row = df.iloc[i]
				message = packMessage(row)
				return message
	return ["None"]


# Добавляем новую команду
def newCMD(text, evnt):
	text = text.split(';')
	sizeCMD = len(text)
	if sizeCMD != 7:
		send("Должно быть 7 параметров: команда;ответ;приложение;айди;RandAns;FulInc;AlwAns", '', event.chat_id)
	else:
		new_row_data = [text[0],text[1],text[2],text[3],text[4],text[5],text[6]]
		wb = load_workbook("./commands.xlsx")
		ws = wb.worksheets[0]
		ws.append(new_row_data)
		wb.save("./commands.xlsx")
		send("Команда "+text[0]+" добавлена", '', evnt.chat_id)