#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from elasticsearch import Elasticsearch

from yutils.queries.db_connection.fetchers.base_fetcher import BaseFetcher


class ElasticSearchFetcher(BaseFetcher):
    def __init__(self, connection_details, verbose=True):
        super().__init__(connection_details, verbose)
        self.connection = None
        self.connect()

    def execute(self, query):
        search = self.connection.search(index=self.connection_details.INDEX, body=query)
        return self._analyze_results(search)

    def _analyze_results(self, search):
        if search['timed_out']:
            return []

        results = []
        for hit in search['hits']['hits']:
            results.append(hit['_source'])
        return results

    def connect(self):
        self.connection = Elasticsearch(self.connection_details.HOST)

    def disconnect(self):
        pass
