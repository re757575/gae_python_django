# coding=utf-8

from google.appengine.ext import ndb
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


# 取得客戶資料
def AllCustomers(param={}):
    # logging.info(param)

    customers = Customers.query()

    if param:
        if 'q' in param and 'query_type' in param and param['q'] and param['query_type']:
            customers = customers.filter(
                Customers._properties[param['query_type']] == str(param['q']))

        if 'customers_type' in param and param['customers_type']:
            customers = customers.filter(
                Customers._properties['type'] == int(param['customers_type']))

        # 排序
        if 'order_by' in param and param['order_by']:
            customers = customers.order(Customers._properties['order_by'])
        else:
            customers = customers.order(-Customers.createTimeStamp)

    return customers


# 更新客戶資料
def UpdateCustomers(id, type, clientName, clientAddress, clientTel, note):
    customers = Customers(id=id, type=type, clientName=clientName,
                          clientAddress=clientAddress, note=note)
    customers.put()
    return customers


# 新增客戶資料
def InsertCustomers(type, clientName, clientAddress, clientTel, note, createOperatorAccount, createTimeStamp):
    customers = Customers(type=type, clientName=clientName, clientAddress=clientAddress, clientTel=clientTel,
                          note=note, createOperatorAccount=createOperatorAccount, createTimeStamp=createTimeStamp)
    customers.put()
    return customers


# 刪除客戶資料
def DeleteCustomers(id):
    key = ndb.Key(Customers, id)
    key.delete()
