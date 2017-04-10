# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from elasticsearch import Elasticsearch


class EsApi:
    def __init__(self, hosts=["localhost:9200"]):
        self.es = Elasticsearch(hosts)

    def add_data(self, index, doc_type, _id, data_insert):
        self.es.index(index=index, doc_type=doc_type, id=_id, body=data_insert)
