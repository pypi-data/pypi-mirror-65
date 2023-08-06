#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import re


def camel_case_to_snake_case(camel_case_word):
    """
    Turns a CamelCase word to a snake_case word

    :param camel_case_word: AWordInCamelCase
    :return: a_word_in_snake_case
    """
    return '_'.join(re.findall('[A-Z][^A-Z]*', camel_case_word)).lower()


def snake_case_to_camel_case(snake_case_word):
    """
    Turns a snake_case word to a CamelCase word

    :param snake_case_word: a_word_in_snake_case
    :return: AWordInCamelCase
    """
    return ''.join(fraction.capitalize() for fraction in snake_case_word.split('_'))


def camel_back_to_snake_case(camel_back_word):
    """
    Turns a camelBack word to a snake_case word

    :param camel_back_word: wordInCamelCase
    :return: a_word_in_snake_case
    """
    return '_'.join(re.findall('[a-zA-Z][^A-Z]*', camel_back_word)).lower()


def snake_case_to_camel_back(snake_case_word):
    """
    Turns a snake_case word to a camelBack word

    :param snake_case_word: a_word_in_snake_case
    :return: wordInCamelCase
    """
    return snake_case_word[0] + ''.join(fraction.capitalize() for fraction in snake_case_word.split('_'))[1:]
