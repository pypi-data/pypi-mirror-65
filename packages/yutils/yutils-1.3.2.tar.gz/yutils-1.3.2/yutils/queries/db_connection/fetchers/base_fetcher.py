#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from abc import ABCMeta, abstractmethod


class BaseFetcher(object):
    """
    A base fetcher for all fetchers for use in a DBConnection
    """
    __metaclass__ = ABCMeta

    _EXPECTED_ENCODING = 'utf-8'
    _FIELD_TYPES_NOT_TO_DECODE = []

    def __init__(self, connection_details, verbose=True):
        self.connection_details = connection_details
        self.verbose = verbose

    @abstractmethod
    def execute(self, query):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    def commit(self):
        raise NotImplementedError()

    def _organize_results(self, results, fields, field_types=None):
        results = self._decode_results(results, fields, field_types)
        return results

    def _decode_results(self, results, fields, field_types):
        for i in range(len(results)):
            for j in range(len(results[i])):
                if field_types and field_types[fields[j]] in self._FIELD_TYPES_NOT_TO_DECODE:
                    continue
                if isinstance(results[i][j], bytes):
                    try:
                        results[i][j] = results[i][j].decode(self._EXPECTED_ENCODING)
                    except UnicodeDecodeError:
                        self.verbose_print("Cell value '{}' in row {} cannot be decoded with utf-8!".format(
                            fields[j], i
                        ))
                if isinstance(results[i][j], str):
                    results[i][j] = results[i][j].strip()
        return results

    def verbose_print(self, *messages):
        if self.verbose:
            print(*messages)
