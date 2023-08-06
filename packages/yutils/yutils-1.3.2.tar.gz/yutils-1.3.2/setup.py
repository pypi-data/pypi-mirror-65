#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')

setup(
    name='yutils',
    version='1.3.2',
    description='A Python utility package written by Yuval Arbel',
    author='Yuval Arbel',
    author_email='yuval@arbels.net',
    url='https://github.com/yuvalarbel',
    download_url='https://github.com/yuvalarbel/yutils/archive/1.3.2.tar.gz',
    keywords=['utils', 'utilities', 'queries', 'ml', 'tools'],
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'sqlalchemy', 'elasticsearch', 'xlsxwriter', 'pymysql', 'cx_Oracle'],
    long_description=open(README_PATH, 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]

)
