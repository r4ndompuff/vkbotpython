import wikipedia
import text_gen
import random
from vkTools import send

wikipedia.set_lang("ru")
gen = text_gen.TextGenerator()

def changeTextByArina(message, event):
    text = gen.text(text=message, simplicity=0)
    send(text, '', event.chat_id)

def estimate(text, event):
    text = 'Оцениваю '+text[11:]+', как '+str(random.randint(0,10))+'/10'
    send(text, '', event.chat_id)

def wikiBot(text, event):
    try:
        textNew = wikipedia.summary(text)
    except wikipedia.DisambiguationError as e:
        textNew = "Возможно, вы имели в виду: " + str(e.options)[2:-2].replace("'",'')
    except wikipedia.exceptions.PageError as e:
        textNew = 'По запросу "'+text+'" ничего не найдено.'
    send(textNew, '', event.chat_id)