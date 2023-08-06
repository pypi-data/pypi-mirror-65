#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import csv
from collections import OrderedDict
from codecs import BOM_UTF8

from yutils.exceptions import WrongDatatype
from yutils.queries.csv_to_db.exceptions.csv_to_db_exceptions import NoTableDataError


class TableData(object):
    def __init__(self, data, datatype='path', fields=None):
        """
        Table Data from DB
        :param data: the data of the query
        :type data: str/list
        :param datatype: the type of the data ('path' / 'data')
        :type datatype: str
        :param fields: the name of the fields (if None, takes the values of the first line as the fields names)
        :type fields: list
        """
        self.data = data
        self.datatype = datatype
        self.fields = fields

        self._column_dicts = OrderedDict()
        self._row_dicts = []

        self._handle_data()
        self._handle_fields()

    @property
    def column_dicts(self):
        if not self._column_dicts:
            self._create_column_dicts()
        return self._column_dicts

    @property
    def row_dicts(self):
        if not self._row_dicts:
            self._create_row_dicts()
        return self._row_dicts

    def _handle_data(self):
        """
        Makes the data a list of lists
        """
        if self.datatype == 'data':
            return
        elif self.datatype == 'path':
            try:
                with open(self.data, 'rb') as csv_file:
                    self.data = list(csv.reader(csv_file))
            except csv.Error as e:
                if str(e) == 'line contains NULL byte':
                    self.data = list(csv.reader(csv.StringIO(open(self.data, 'rb').read().replace('\x00', ''))))
                else:
                    raise
        else:
            raise WrongDatatype('datatype', "path' or 'data", self.datatype)

    def _handle_fields(self):
        """
        Finds the fields of the query
        """
        if not self.fields:
            fields = self.data[0]
            self.data = self.data[1:]
            self.fields = [field.lower().replace(BOM_UTF8, '') for field in fields]

    def _create_column_dicts(self):
        """
        Orders the data in an OrderedDict: keys are field names and values are lists of column values
        """
        if not self.data:
            raise NoTableDataError()

        for i in range(len(self.fields)):
            self._column_dicts[self.fields[i]] = [row[i] for row in self.data]

    def _create_row_dicts(self):
        """
        Orders the data in a list of dicts -
        each row is an item in the list, and is a dict - keys are field names and values are field values in this row
        """
        if not self.data:
            raise NoTableDataError()

        self._row_dicts = [{self.fields[i]: row[i].strip() for i in range(len(self.fields))} for row in self.data]
