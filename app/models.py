# coding=utf-8

from google.appengine.ext import ndb
from google.appengine.api import memcache
import logging
import time


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

            """ 取得對應的 orders """
            # start_time = time.time()
            for c in result:
                customers_orders = c.get_orders.fetch()
                logging.info('orders: {}'.format(len(customers_orders)))
                for co in customers_orders:
                    logging.info(co)
            #
            # logging.info("--- %s seconds ---" % (time.time() - start_time))
            # exit()
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

        """ 寫入 orders """
        # 使用 StructuredProperty
        # order = Orders(ordersNo='151225001', ordersTitle='PS4*10', customer=customers)
        # order = Orders(ordersNo='151225001', ordersTitle='PS4*10', customer=[customers,customers])
        # order.put()

        # muitl put
        # 使用 KeyProperty (non-ancestor) 建立
        orders = Orders(ordersNo='151225001',
                        ordersTitle='PS4*10', customer=customers.key)
        orders2 = Orders(ordersNo='151225002',
                         ordersTitle='PS4*9', customer=customers.key)
        ndb.put_multi([orders, orders2])

        # 使用 ancestor 建立
        # orders = Orders(ordersNo='151225001',
        #                 ordersTitle='PS4*10', parent=customers.key)
        # orders2 = Orders(ordersNo='151225002',
        #                  ordersTitle='PS4*9', parent=customers.key)
        # ndb.put_multi([orders, orders2])

        # test runtime
        # start_time = time.time()
        # orders_array = []
        # for i in range(1000):
        #     orders = Orders(ordersNo=str(151225001+i),
        #                     ordersTitle='PS4*10', customer=customers.key)
        #     # orders = Orders(ordersNo=str(151225001+i),
        #     #                 ordersTitle='PS4*10', parent=customers.key)
        #     orders_array.append(orders)
        #
        # logging.info(orders_array)
        # ndb.put_multi(orders_array)
        #
        # logging.info("--- %s seconds ---" % (time.time() - start_time))
        # exit()

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

    # 取得該訂單
    @property
    def get_orders(self):
        # KeyProperty (non-ancestor)
        return Orders.query(Orders.customer == self.key)

        # ancestor
        # return Orders.query(ancestor=self.key)


class Orders(ndb.Model):
    ordersNo = ndb.StringProperty(required=True)
    ordersTitle = ndb.StringProperty(required=True)
    # 使用 KeyProperty (non-ancestor)
    customer = ndb.KeyProperty(kind=Customers, required=True)

    # 使用 StructuredProperty
    # customer = ndb.StructuredProperty(Customers, repeated=True)


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
