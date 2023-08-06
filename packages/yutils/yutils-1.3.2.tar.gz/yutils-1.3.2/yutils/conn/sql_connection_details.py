#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38


class ConnectionDetails(object):
    pass


class OracleConnectionDetails(object):
    TYPE = 'oracle'


class MSSQLConnectionDetails(object):
    TYPE = 'mssql'


class MySQLConnectionDetails(object):
    TYPE = 'mysql'


class ElasticConnectionDetails(object):
    TYPE = 'elastic'


# ########################
# ####### EXAMPLES #######
# ########################


class ORACLE_EXAMPLE(OracleConnectionDetails):
    DB = 'db'
    SCHEMA = 'schema'
    PASSWORD = 'password'


class MSSQL_EXAMPLE(MSSQLConnectionDetails):
    FREE_TDS = 'free_tds'
    SCHEMA = 'schema'
    PASSWORD = 'password'


class MYSQL_EXAMPLE(MySQLConnectionDetails):
    HOST = 'host'
    USERNAME = 'username'
    PASSWORD = 'password'
    SCHEMA = 'schema'


class ELASTIC_EXAMPLE(ElasticConnectionDetails):
    HOST = 'host'
    INDEX = 'index'


# ###############################
# ####### IMPLEMENTATIONS #######
# ###############################


class DABANK(MySQLConnectionDetails):
    HOST = 'localhost'
    USERNAME = 'root'
    PASSWORD = '4s92H%xdBZ$2'
    SCHEMA = 'bank'


class STOCKS(MySQLConnectionDetails):
    HOST = 'localhost'
    USERNAME = 'root'
    PASSWORD = '4s92H%xdBZ$2'
    SCHEMA = 'stocks'
