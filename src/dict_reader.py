# -*- coding: utf-8 -*-
import pymorphy2
import nltk
import random

class DictReader:
    """
    Dictionary reader class.

    Methods:

    - get_word(amount=1) - gets a random word from dictionary.
    
    - get_simple(amount=1) - gets a random simple word from dictionary.
    
    - get_standart(amount=1) - gets a random standart word from dictionary.

    - get_hard(amount=1) - gets a random hard word from dictionary.

    - get_name(amount=1) - gets a name from dictionary.
    """
    
    def get_word(self, amount = 1):
        """
        Gets a random word from the dictionary. 

        Params: amount - amount of words that is being returned. By default is 1.

        Return value: list of random words.
        """
        if len(self.__words) != 0 and self.__words_read  == len(self.__words):
            self.__words_read = 1

        if self.__words_read == 0:
            with open("dict/words.txt", 'r') as f:
                self.__words = f.read()
                self.__words = self.__words.split("\n")
                self.__words_read = random.randint(0, 50785)

        result = self.__words[self.__words_read:self.__words_read + amount]
        self.__words_read += amount
        return list(result)

    def get_simple(self, amount = 1):
        """
        Gets a random simple word from the dictionary. 

        Params: amount - amount of words that is being returned. By default is 1.

        Return value: list of random simple words.
        """
        if len(self.__simple) != 0 and self.__simple_read  == len(self.__simple):
            self.__simple_read = 1

        if self.__simple_read == 0:
            with open("dict/simple.txt", 'r') as f:
                self.__simple = f.read()
                self.__simple = self.__simple.split("\n")
                self.__simple_read = random.randint(0, 32724)

        result = self.__simple[self.__simple_read:self.__simple_read + amount]
        self.__simple_read += amount
        return list(result)

    def get_standart(self, amount = 1):
        """
        Gets a random standart word from the dictionary. 

        Params: amount - amount of words that is being returned. By default is 1.

        Return value: list of random standart words.
        """
        if len(self.__standart) != 0 and self.__standart_read  == len(self.__standart):
            self.__standart_read = 1

        if self.__standart_read == 0:
            with open("dict/standart.txt", 'r') as f:
                self.__standart = f.read()
                self.__standart = self.__standart.split("\n")
                self.__standart_read = random.randint(0, 26598)

        result = self.__standart[self.__standart_read:self.__standart_read + amount]
        self.__standart_read += amount
        return list(result)

    def get_hard(self, amount = 1):
        """
        Gets a random hard word from the dictionary. 

        Params: amount - amount of words that is being returned. By default is 1.

        Return value: list of random hard words.
        """
        if len(self.__hard) != 0 and self.__hard_read  == len(self.__hard):
            self.__hard_read = 1

        if self.__hard_read == 0:
            with open("dict/hard.txt", 'r') as f:
                self.__hard = f.read()
                self.__hard = self.__hard.split("\n")
                self.__hard_read = random.randint(0, 21281)

        result = self.__hard[self.__hard_read:self.__hard_read + amount]
        self.__hard_read += amount
        return list(result)


    def get_name(self, amount = 1):
        """
        Gets a name from the dictionary. 

        Params: amount - amount of words that is being returned. By default is 1.

        Return value: list of names.
        """
        if len(self.__names) != 0 and self.__names_read  == len(self.__names):
            self.__names_read = 1

        if self.__names_read == 0:
            with open("dict/names.txt", 'r') as f:
                self.__names = f.read()
                self.__names = self.__names.split("\n")
                self.__names_read = random.randint(0, 387)

        result = self.__names[self.__names_read:self.__names_read + amount]
        self.__names_read += amount
        return list(result)

    def __init__(self):
        random.seed()
        self.__MorphAnalyzer = pymorphy2.MorphAnalyzer(lang="ru")
        self.__standart_read = 0
        self.__simple_read = 0
        self.__names_read = 0
        self.__words_read = 0
        self.__hard_read = 0
        self.__standart = ""
        self.__simple = ""
        self.__names = ""
        self.__words = ""
        self.__hard = ""