#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.queries.csv_to_db.consts.consts import NVARCHAR_HEBREW_ENCODINGS, TIMESTAMP_FORMATS


class NoTableError(Exception):
    _EXCEPTION_STR = """No table '{table_name}" found for owner '{owner}'!"""

    def __init__(self, table_name, owner):
        super().__init__(self._EXCEPTION_STR.format(table_name=table_name, owner=owner))


class BadDateFormatError(Exception):
    _EXCEPTION_STR = """The date '{date}' isn't of any known date format!\nKnown date formats:\n{date_formats}"""

    def __init__(self, date):
        super().__init__(self._EXCEPTION_STR.format(date=date, date_formats=TIMESTAMP_FORMATS))


class BadNVarCharFormatError(Exception):
    _EXCEPTION_STR = """The non-english string '{string}' isn't of any known encodings!
Known encodings:\n{encodings}"""

    def __init__(self, string):
        super().__init__(self._EXCEPTION_STR.format(string=string,
                                                                                date_formats=NVARCHAR_HEBREW_ENCODINGS))


class MissingFieldError(Exception):
    _EXCEPTION_STR = """The given field '{field_name}' does not appear in table '{table_name}'"""

    def __init__(self, field_name, table_name):
        super().__init__(self._EXCEPTION_STR.format(field_name=field_name,
                                                                           table_name=table_name))


class DataInsertionCancelled(Exception):
    _EXCEPTION_STR = """User cancelled data insertion."""

    def __init__(self):
        super().__init__(self._EXCEPTION_STR)


class NoTableDataError(Exception):
    _EXCEPTION_STR = """There are 0 rows in the csv!"""

    def __init__(self):
        super().__init__(self._EXCEPTION_STR)


class NotThisDatatypeError(Exception):
    _EXCEPTION_STR = """This is not the right datatype!"""

    def __init__(self):
        super().__init__(self._EXCEPTION_STR)


class TableCreationCancelled(Exception):
    _EXCEPTION_STR = """User cancelled table creation."""

    def __init__(self):
        super().__init__(self._EXCEPTION_STR)


class NoInsertQuery(Exception):
    _EXCEPTION_STR = """There is no insert query for this row!"""

    def __init__(self):
        super().__init__(self._EXCEPTION_STR)
