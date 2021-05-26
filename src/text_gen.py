# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
import dict_reader
import pymorphy2
import nltk
import re

class TextGenerator:
    """
    Text generator class.

    Methods:

    - text(text) - generate text from given input.
    """
    def text(self, text, simplicity = 0):
        """
        Method that generates text from given input.

        Params: 
        
        text - string with original text. 

        simplicity = 0 - simplicity of the text. 0 is unset, 1 is simple 
        (using short words), 2 is standart (using medium sized words), 3 
        is hard (using long words and scientific terms)

        Return value: string with generated text.
        """
        # Creating dict to store words
        translate_dict = dict()
        tokens = nltk.word_tokenize(text)

        # For statement in which we iterate over the text
        for token in tokens:
            # Creating a cycle counter
            counter = 0

            # Parsing the word
            current_word = self.__morph.parse(token)[0]
            current_normal = self.__morph.parse(current_word.normal_form)[0]

            # Getting the original word's unchangeable grammemes 
            params = set(current_normal.tag.grammemes)
            

            # Checking if it's actually a word and if it's a self.__stop-word
            if "LATN" in params or "PNCT" in params or "NUMB" in params or "intg" in params or "real" in params or "ROMN" in params or "UNKN" in params or current_word.normal_form in self.__stop:
                continue
            
            # Checking if it already exists in our dictionary
            if current_normal.word in translate_dict:
                dict_word = self.__morph.parse(translate_dict[current_normal.word])[0]
                if dict_word.inflect(current_word.tag.grammemes) == None:
                    for parse in self.__morph.parse(token):
                        if dict_word.inflect(parse.tag.grammemes) != None:
                            tokens[tokens.index(token)] = dict_word.inflect(parse.tag.grammemes).word
                            break
                    continue
                tokens[tokens.index(token)] = dict_word.inflect(current_word.tag.grammemes).word
                continue
            
            # If the word is name
            if "Name" in params:
                getword = self.__dr.get_name
            else:
                if simplicity == 0:
                    getword = self.__dr.get_word
                elif simplicity == 1:
                    getword = self.__dr.get_simple
                elif simplicity == 2:
                    getword = self.__dr.get_standart
                elif simplicity == 3:
                    getword = self.__dr.get_hard

            # Starting to cycle through the dictionary in search for compatible words
            dict_word = getword()
            while len(dict_word) != 0 and counter != 10000:
                # Incrementing counter
                counter += 1

                # Parsing words that we got from the dictionary
                dict_word = self.__morph.parse(dict_word[0])[0]
                dict_normal = self.__morph.parse(dict_word.normal_form)[0]

                # If the word is name
                if "Name" in params:
                    # Checking for unchangable parameters of the word
                    if dict_normal.tag == current_normal.tag:
                        break
                else:
                    # Checking for unchangable parameters of the word
                    if dict_normal.tag == current_normal.tag:
                        break
                dict_word = getword()
            else:
                continue
            
            # Continuing if we fell out of the cycle because we couldn't find proper replacement
            if counter == 10000:
                continue

            # Adding resulting word to the dictionary and replacing the original word
            translate_dict[current_normal.word] = dict_normal.word
            if dict_word.inflect(current_word.tag.grammemes) == None:
                for parse in self.__morph.parse(token):
                    if dict_word.inflect(parse.tag.grammemes) != None:
                        tokens[tokens.index(token)] = dict_word.inflect(parse.tag.grammemes).word
                        break
                continue
            
            tokens[tokens.index(token)] = dict_word.inflect(current_word.tag.grammemes).word

        tokens = " ".join(tokens)
        tokens = re.sub(r"\s+(?=[.,?!():;\"\'\\/»])", "", tokens, 0, re.MULTILINE)
        tokens = re.sub(r"[«]\s", " «", tokens, 0, re.MULTILINE)
        tokens = nltk.sent_tokenize(tokens, language="russian")
        result = ""

        for sent in tokens:
            if result != "":
                result += " "
            result += sent[0].capitalize() + sent[1:]

        return result

    def __init__(self):
        # Initializing and creating objects for later use
        self.__morph = pymorphy2.MorphAnalyzer(lang="ru")
        self.__dr = dict_reader.DictReader()
        stopwords_nltk = stopwords.words("russian")
        self.__stop = set()

        # Making our own set of stop words, because NLTK's list contains words not in normal from
        for word in stopwords_nltk:
            self.__stop.add(self.__morph.parse(word)[0].normal_form)
        self.__stop.add(self.__morph.parse("который")[0].normal_form)