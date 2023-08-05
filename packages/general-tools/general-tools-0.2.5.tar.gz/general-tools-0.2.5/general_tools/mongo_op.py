#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: xuwei
Email: 18810079020@163.com
Description:
date:
'''

import pymongo
from pymongo import UpdateOne
from .config_log import config


def get_client(label='mongo', **kwargs):
    if config(label, 'user', ''):
        my_client = pymongo.MongoClient(
            'mongodb://{0}:{1}@{2}:{3}/'. \
                format(
                config(label, 'user'), config(label, 'pass'),
                config(label, 'host'), config(label, 'port')
            ),
            **kwargs
        )
    else:
        my_client = pymongo.MongoClient(
            'mongodb://{0}:{1}/'. \
                format(config(label, 'host'), config(label, 'port')),
            **kwargs
        )
    return my_client


class MongoOp(object):
    def __init__(self, db, collection, label='mongo', limit=10):
        self.db = db
        self.col = collection
        self.client = get_client(label=label)
        self.limit = limit

    def show_db(self):
        dbs_list = self.client.database_names()
        return dbs_list

    def show_col(self):
        db = self.client[self.db]
        cols_list = db.collection_names()
        return cols_list

    def create_index(self, index_param):
        col = self.client[self.db][self.col]
        col.create_index(index_param)

    def view_index(self):
        col = self.client[self.db][self.col]
        indexs_list = col.list_indexes()
        for index in indexs_list:
            print(index)

    def drop_col(self):
        col = self.client[self.db][self.col]
        col.drop()

    def batch_write(self, write_list_dict):
        col = self.client[self.db][self.col]
        to_be_request = [UpdateOne({'_id': b['_id']}, {'$set': b}, upsert=True) for b in write_list_dict]
        col.bulk_write(to_be_request, ordered=False)

    def insert_one(self, write_dict):
        col = self.client[self.db][self.col]
        try:
            col.insert_one(write_dict)
        except:
            pass

    def find_one(self, *args, **kwargs):
        col = self.client[self.db][self.col]
        res = col.find_one(*args, **kwargs)
        return res

    def find(self, *args, **kwargs):
        col = self.client[self.db][self.col]
        yield_res = col.find(*args, **kwargs).limit(self.limit)
        res_list = [_ for _ in yield_res]
        return res_list

    def close(self):
        self.client.close()


if __name__ == '__main__':
    mg_op = MongoOp('xiaomu', 'knowledge_map', label='mongo')
    # mg_op.create_index([("other_name", pymongo.ASCENDING), ("stock_code", pymongo.ASCENDING)])
    r = mg_op.show_col()
    print(r)
    mg_op.view_index()
    r = mg_op.find_one({'type': 'teacher'})
    print(r)
    r = mg_op.find({'type': 'teacher'})
    print(r)
    mg_op.close()

