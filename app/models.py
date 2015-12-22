# coding=utf-8

from google.appengine.ext import ndb
from google.appengine.api import memcache
import logging


class Customers(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    clientName = ndb.StringProperty(required=True)
    clientAddress = ndb.StringProperty()
    clientTel = ndb.StringProperty()
    clientFax = ndb.StringProperty()
    vatNumber = ndb.StringProperty()
    status = ndb.BooleanProperty(required=True, default=True)
    billingAddress = ndb.StringProperty()
    note = ndb.TextProperty()
    createOperatorAccount = ndb.UserProperty()
    createDateTime = ndb.DateTimeProperty(auto_now_add=True)
    createTimeStamp = ndb.FloatProperty(required=True)
    page = 1
    limit = 10

    # 取得客戶資料
    @classmethod
    def _get_all_customers(cls, param):

        customers = cls.query()

        if param:
            if 'q' in param and 'query_type' in param and param['q'] and param['query_type']:
                customers = customers.filter(
                    Customers._properties[param['query_type']] == str(param['q']))

            if 'client_type' in param and param['client_type']:
                customers = customers.filter(
                    Customers._properties['type'] == int(param['client_type']))

            # 排序
            if 'order_by' in param and param['order_by']:
                customers = customers.order(Customers._properties['order_by'])
            else:
                customers = customers.order(-Customers.createTimeStamp)

            total = customers.count()

            """ 使用 cache """
            customers = customers.fetch(
                cls.limit, offset=(cls.page - 1) * cls.limit, keys_only=True, use_cache=True)
            result = get_data_from_cache(customers, 'customers_')

            """ 不使用 cache """
            # customers = customers.fetch(
            #     cls.limit, offset=(cls.page - 1) * cls.limit, use_cache=False)
            # result = customers

        return {'result': result, 'total': total}

    # 更新客戶資料 DOTO:需修改成動態參數
    @classmethod
    def _update_customers(cls, id, type, clientName, clientAddress, clientTel, note):
        customers = cls(id=id, type=type, clientName=clientName,
                        clientAddress=clientAddress, note=note)
        customers.put()
        return customers

    # 新增客戶資料
    @classmethod
    def _insert_customers(cls, type, clientName, clientAddress, clientTel, note, createOperatorAccount, createTimeStamp):

        customers = Customers(type=type, clientName=clientName, clientAddress=clientAddress, clientTel=clientTel,
                              note=note, createOperatorAccount=createOperatorAccount, createTimeStamp=createTimeStamp)
        customers.put()
        return customers

    # 刪除客戶資料
    @classmethod
    def _delete_customers(cls, id):
        key = ndb.Key(Customers, id)
        key.delete()

    # 刪除全部客戶資料
    @classmethod
    def _delete_all_customers(cls):
        ndb.delete_multi(cls.query().fetch(keys_only=True))


""" 共用 function """

# 從 cache 取得資料


def get_data_from_cache(entity, key_prefix):
    tk = []
    for k in entity:
        tk.append(str(k.urlsafe()))

    logging.info(tk)

    # get memcache: results
    cache_results = memcache.get_multi(
        keys=tk, key_prefix=key_prefix)

    result = []
    memcache_to_add = {}
    for wanted in tk:
        if not any(r == wanted for r in cache_results):
            # 沒有 cache
            logging.info('not found')
            memcache_to_add[wanted] = ndb.Key(urlsafe=wanted).get()
            result.append(memcache_to_add[wanted])
        else:
            # 有
            logging.info('found')
            result.append(cache_results[wanted])

    logging.info('memcache(s) to add: ' + str(len(memcache_to_add)))

    if len(memcache_to_add) > 0:
        memcache.add_multi(
            memcache_to_add, key_prefix=key_prefix, time=3600)

    return result
