#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.base import InputChecker
from yutils.conn.sql_connection_details import OracleConnectionDetails


class GiveTablePermissions(InputChecker):
    _INPUT_TYPES = {'connection_details': OracleConnectionDetails,
                    'table_name': str,
                    'user_to_escalate': str,
                    'print_queries': bool}

    _GIVE_SELECT_PERMISSIONS = "GRANT SELECT ON {table_name} TO {user_to_escalate}"
    _CREATE_SYNONYM = "CREATE PUBLIC SYNONYM {table_name} FOR {owner}.{table_name}"

    def __init__(self, connection_details, table_name, user_to_escalate, print_queries):
        """
        Gives the user user_to_escalate the permissions to query on db_username's table.

        !!! WARNING !!!
        !!! AUTOMATICALLY COMMITS !!!

        :param connection_details: Details for connection to the wanted Oracle DB
        :type connection_details: yutils.conn.sql_connection_details.OracleConnectionDetails
        :param table_name: the name of the table to insert the data into
        :type table_name: str
        :param user_to_escalate: the username to give permissions to
        :type user_to_escalate: str
        :param print_queries: if to print queries during run
        :type print_queries: bool
        :return: None
        """
        self.connection_details = connection_details
        self.table_name = table_name
        self.user_to_escalate = user_to_escalate
        self.print_queries = print_queries

        super().__init__()

    def _verbose_print(self, text):
        if self.print_queries:
            print(text)

    def give_permissions(self):
        permissions_query = self._GIVE_SELECT_PERMISSIONS.format(table_name=self.table_name,
                                                                 user_to_escalate=self.user_to_escalate)
        self._verbose_print(permissions_query)
        self.connection_details.query(permissions_query)

        synonym_query = self._CREATE_SYNONYM.format(table_name=self.table_name,
                                                    owner=self.db_username)
        self._verbose_print(synonym_query)
        self.connection_details.query(synonym_query)

        self.connection_details.commit()

        self._verbose_print('\nDone.')
