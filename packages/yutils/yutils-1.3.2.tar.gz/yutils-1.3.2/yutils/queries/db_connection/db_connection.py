#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.conn import ConnectionDetails
from yutils.queries.db_connection.fetchers.oracle import OracleFetcher
from yutils.queries.db_connection.fetchers.mssql import MSSQLFetcher
from yutils.queries.db_connection.fetchers.mysql import MySQLFetcher
from yutils.queries.db_connection.fetchers.elastic import ElasticSearchFetcher


class DBConnection(object):
    """
    Wraps a connection to a DB, for executing SQL queries, using given connection_details.
    """
    _FETCHERS = {'oracle': OracleFetcher,
                 'mssql': MSSQLFetcher,
                 'mysql': MySQLFetcher,
                 'elastic': ElasticSearchFetcher}

    def __init__(self, connection_details, verbose=True):
        """
        :param connection_details: Details for connection to the wanted DB
        :type: connection_details: yutils.conn.sql_connection_details.ConnectionDetails
        :param verbose: If to print warnings or not
        :type verbose: bool
        """
        self.connection_details = connection_details
        self.verbose=verbose

        self.fetcher = self._FETCHERS[self.connection_details.TYPE](
            connection_details=self.connection_details,
            verbose=self.verbose
        )

    def query(self, query):
        """
        Runs the wanted query.

        :param query: the query you wish to run
        :type query: str
        :return: Query results: pandas DataFrame
        :rtype: pandas.DataFrame
        """
        return self.fetcher.execute(query)

    def _connect(self):
        """
        Connects to the DB
        """
        self.fetcher.connect()

    def disconnect(self):
        """
        Disconnects connection to the DB.
        """
        self.fetcher.disconnect()

    def commit(self):
        """
        Commits the transaction to the DB.
        """
        self.fetcher.commit()
