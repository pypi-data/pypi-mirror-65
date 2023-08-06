#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

NVARCHAR_HEBREW_ENCODINGS = ['utf8', 'cp1255', 'utf-16-le', 'utf32', 'ascii']

DATETIME_FORMATS = ['%d/%m/%y %H:%M:%S', '%d.%m.%y %H:%M:%S', '%d-%m-%y %H:%M:%S',
                    '%d/%m/%Y %H:%M:%S', '%d.%m.%Y %H:%M:%S', '%d-%m-%Y %H:%M:%S',
                    '%y/%m/%d %H:%M:%S', '%y.%m.%d %H:%M:%S', '%y-%m-%d %H:%M:%S',
                    '%Y/%m/%d %H:%M:%S', '%Y.%m.%d %H:%M:%S', '%Y-%m-%d %H:%M:%S',
                    '%d/%m/%y %H:%M', '%d.%m.%y %H:%M', '%d-%m-%y %H:%M',
                    '%d/%m/%Y %H:%M', '%d.%m.%Y %H:%M', '%d-%m-%Y %H:%M',
                    '%y/%m/%d %H:%M', '%y.%m.%d %H:%M', '%y-%m-%d %H:%M',
                    '%Y/%m/%d %H:%M', '%Y.%m.%d %H:%M', '%Y-%m-%d %H:%M',
                    '%d/%m/%y', '%d.%m.%y', '%d-%m-%y',
                    '%d/%m/%Y', '%d.%m.%Y', '%d-%m-%Y',
                    '%y/%m/%d', '%y.%m.%d', '%y-%m-%d',
                    '%Y/%m/%d', '%Y.%m.%d', '%Y-%m-%d'
                    ]
DB_DATETIME_FORMAT_PYTHON = '%d/%m/%Y %H:%M:%S'
DB_DATETIME_FORMAT_SQL = 'dd/mm/yyyy hh24:mi:ss'

TIMESTAMP_FORMATS = ['%d/%m/%y %H:%M:%S.%f', '%d.%m.%y %H:%M:%S.%f', '%d-%m-%y %H:%M:%S.%f',
                     '%d/%m/%Y %H:%M:%S.%f', '%d.%m.%Y %H:%M:%S.%f', '%d-%m-%Y %H:%M:%S.%f',
                     '%y/%m/%d %H:%M:%S.%f', '%y.%m.%d %H:%M:%S.%f', '%y-%m-%d %H:%M:%S.%f',
                     '%Y/%m/%d %H:%M:%S.%f', '%Y.%m.%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S.%f'
                     ]
DB_TIMESTAMP_FORMAT_PYTHON = '%d/%m/%Y %H:%M:%S.%f'
DB_TIMESTAMP_FORMAT_SQL = 'dd/mm/yyyy hh24:mi:ss.ff6'
