from google.appengine.ext import ndb


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
    createTimeStamp  = ndb.FloatProperty(required=True)


def AllCustomers():
    return Customers.query()


def UpdateCustomers(id, type, clientName, clientAddress, note):
    customers = Customers(id=id, type=type, clientName=clientName, clientAddress=clientAddress, note=note)
    customers.put()
    return customers


def InsertCustomers(type, clientName, clientAddress, note, createOperatorAccount, createTimeStamp):
    customers = Customers(type=type, clientName=clientName, clientAddress=clientAddress, note=note, createOperatorAccount=createOperatorAccount, createTimeStamp=createTimeStamp)
    customers.put()
    return customers


def DeleteCustomers(id):
    key = ndb.Key(Customers, id)
    key.delete()
