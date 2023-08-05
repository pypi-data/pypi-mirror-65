#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (C)2018 SenseDeal AI, Inc. All Rights Reserved
Author: xuwei
Email: weix@sensedeal.ai
Description:
'''

from elasticsearch_dsl import Document, Keyword, Text, Float, Nested, Date, Integer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search, Q
from elasticsearch.helpers import bulk
from .config_log import config


class OtherName(Document):
    company_code = Keyword()
    other_name = Text(analyzer='ik_max_word')
    company_full_name = Text(analyzer='ik_max_word')

    class Index:
        name = 'other_name'
        using = 'es'

    def save(self, **kwargs):
        return super(OtherName, self).save(**kwargs)


def get_es_client(label='', host='', user='', password=''):
    if label:
        host = config(label, 'host')
        user = config(label, 'user', '')
        password = config(label, 'pass', '')
    else:
        host = host
        user = user
        password = password
        label = 'default'
    if user and password:
        return connections.create_connection(alias=label, hosts=[host], http_auth=(user, password), timeout=300)
    return connections.create_connection(alias=label, hosts=[host], timeout=300)


class EsOperate(object):
    def __init__(self, conn, index, doc_type='doc', doc_model=Document, size=2000):
        self.conn = conn
        self.index = index
        self.doc_type = doc_type
        self.doc_model = doc_model
        self.size = size

    def get_es_state(self):
        print(self.conn.cluster.state())
        print(self.conn.cluster.health())

    def delete_index(self):
        self.conn.indices.delete(self.index, ignore=[400, 404])

    def init(self):
        self.doc_model.init(index=self.index)

    def delete_by_model_id(self, publish_id):
        es_news = self.doc_model.get(id=publish_id)
        es_news.delete()

    def delete_by_id(self, id):
        self.conn.delete(index=self.index, doc_type=self.doc_type, id=id, ignore=[400, 404])

    def set_alias(self, other_name):
        self.conn.indices.put_alias(index=self.index, name=other_name)

    def delete_alias(self, other_name):
        self.conn.indices.delete_alias(index=self.index, name=other_name, ignore=[400, 404])

    def add_one_data(self, body, id=None):
        self.conn.index(index=self.index, doc_type=self.doc_type, body=body, id=id)

    def __query_iterator(self, query):
        total = query['hits']['total']  # es查询出的结果总量
        print(total)
        scroll_id = query['_scroll_id']  # 游标用于输出es查询出的所有结果
        for i in range(0, int(total / self.size) + 1):
            # scroll参数必须指定否则会报错
            query_list = self.conn.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']
            if query_list:
                res_list = [_obj['_source'] for _obj in query_list]
                yield res_list
            else:
                query_list = query['hits']['hits']
                res_list = [_obj['_source'] for _obj in query_list]
                yield res_list

    def __query_iterator_origin(self, query):
        total = query['hits']['total']  # es查询出的结果总量
        print(total)
        scroll_id = query['_scroll_id']  # 游标用于输出es查询出的所有结果
        for i in range(0, int(total / self.size) + 1):
            # scroll参数必须指定否则会报错
            query_list = self.conn.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']
            if not query_list:
                query_list = query['hits']['hits']
            yield query_list

    def get_all_data_iterator(self):
        query = self.conn.search(index=self.index, doc_type=self.doc_type, scroll='5m', size=self.size, ignore=[400, 404])
        return self.__query_iterator(query)

    def get_all_data_iterator_origin(self):
        query = self.conn.search(index=self.index, doc_type=self.doc_type, scroll='5m', size=self.size, ignore=[400, 404])
        return self.__query_iterator_origin(query)

    def get_all_data(self):
        query = self.conn.search(index=self.index, doc_type=self.doc_type, ignore=[400, 404])
        return query

    def get_query_iterator(self, body):
        query = self.conn.search(index=self.index, doc_type=self.doc_type, body=body, scroll='5m', size=self.size, ignore=[400, 404])
        return self.__query_iterator(query)

    def es_query(self, body):
        _data = self.conn.search(index=self.index, doc_type=self.doc_type, body=body, ignore=[400, 404], size=self.size)
        return _data

    def get_one_data(self, id):
        _data = self.conn.get(index=self.index, doc_type=self.doc_type, id=id, ignore=[400, 404])
        return _data

    def update_one_data(self, id, body=None):
        self.conn.update(index=self.index, doc_type=self.doc_type, id=id, body=body)

    # 查询field="python"或"android"的所有数据
    # term_name = {"field": ["python", "android"]}
    def terms_query(self, term_name):
        _body = {'query': {'term': term_name}, 'size': 10, 'from': 0}
        _data = self.conn.search(index=self.index, doc_type=self.doc_type, body=_body)
        return _data

    # term_name = {"field": ["python", "android"]}field包含python关键字的数据
    def match_query(self, term_name):
        # match:匹配name包含python关键字的数据
        _body = {'query': {'match': term_name}, 'size': 10}
        _data = self.conn.search(index=self.index, doc_type=self.doc_type, body=_body)
        return _data

    # 多个字段其一含有某个字符
    # term_name = {"query": "深圳", "fields": ["name", "addr"]}
    def multi_match(self, term_name):
        _body = {'query': {'multi_match': term_name}, 'size': 10}
        _data = self.conn.search(index=self.index, doc_type=self.doc_type, body=_body)
        return _data

    def bulk_to_es(self, bulk_list):
        _length = len(bulk_list)
        if _length > 100:
            for i in range(0, _length, 100):
                bulk(self.conn, bulk_list[i: i + 100], index=self.index, doc_type=self.doc_type)
        else:
            bulk(self.conn, bulk_list, index=self.index, doc_type=self.doc_type)


def test():
    es_client = get_es_client(label='es')
    indexer = EsOperate(es_client, 'other_name')
    for data in indexer.get_all_data_iterator():
        print(data)
        break


if __name__ == '__main__':
    test()
