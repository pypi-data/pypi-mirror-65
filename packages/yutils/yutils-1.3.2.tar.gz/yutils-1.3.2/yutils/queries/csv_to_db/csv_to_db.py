#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import os

from yutils.exceptions import InputError
from yutils.queries.csv_to_db.stages.create_table import create_table
from yutils.queries.csv_to_db.stages.insert_data_to_table import insert_data_to_table
from yutils.queries.csv_to_db.stages.give_permissions import GiveTablePermissions


def insert_csv_to_db(connection_details, data_to_insert, data_to_insert_type='path', table_name=None, data_fields=None,
                     commit=True, check_duplicates=False, duplicate_field_check=None,
                     give_other_user_select_permissions=False, other_user_for_select_permissions=None,
                     force=False, print_queries=True):
    """
    Gets data from csv or list of lists, and inserts it into the table in the DB.

    :param connection_details: Details for connection to the wanted Oracle DB
    :type connection_details: yutils.conn.sql_connection_details.OracleConnectionDetails
    :param data_to_insert: the data you want to insert into the table
    :type data_to_insert: str / matrix (list of lists)
    :param data_to_insert_type: the type of the data ('path' / 'data')
    :type data_to_insert_type: str
    :param table_name: the name of the table to insert the data into -
                       When defaulted to None, table name is created by basename:
                       os.path.basename(csv_path).replace('.csv', '')
    :type table_name: str
    :param data_fields: the names of the fields of the data to insert
                        (if None, takes the values of the first line of the CSV as the field names)
    :type data_fields: list of str
    :param commit: whether or not to commit (default: True)
    :type commit: bool
    :param check_duplicates: if to ignore rows already inserted into the DB (default: False)
    :type check_duplicates: bool
    :param duplicate_field_check: the column name of the unique field in the table (for uniqueness check) -
                                  (usually is an ID field)
    :type duplicate_field_check: str
    :param give_other_user_select_permissions: if to give a different user select permissions on the table
                                               (for example, in order to upload as admin and give a query user
                                                permissions to only query)
                                               (default: False)
    :type give_other_user_select_permissions: bool
    :param other_user_for_select_permissions: a different user you want to give query permissions on the table to
    :type other_user_for_select_permissions: str
    :param force: if to force table creation (won't ask for permission) (default: False)
    :type force: bool
    :param print_queries: if to print queries (default: True)
    :type print_queries: bool

    :return: None
    """
    if not table_name:
        if data_to_insert_type != 'path':
            raise InputError('No table_name given!')
        table_name = os.path.basename(data_to_insert).replace('.csv', '')

    create_table(connection_details, table_name, data_to_insert, data_to_insert_type, data_fields, force, print_queries)

    insert_data_to_table(connection_details, table_name, data_to_insert, data_to_insert_type, data_fields, commit,
                         check_duplicates, duplicate_field_check, force, print_queries)

    if give_other_user_select_permissions and commit:
        GiveTablePermissions(connection_details, table_name, other_user_for_select_permissions, print_queries)\
            .give_permissions()
