#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import re


def get_model_name(model):
    camel_back_name = model.__name__ if hasattr(model, '__name__') else model.__class__.__name__
    model_name = ' '.join(re.findall('[A-Z][^A-Z]*', camel_back_name))
    return model_name
