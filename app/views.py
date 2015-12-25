# coding=utf-8

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import render_to_response

from datetime import datetime
from random import randint
import logging
import time
import json
import math

from google.appengine.api import users
from google.appengine.ext import ndb

from models import Customers
from lib.helper import helper_pager


def error404(request):
    response = render_to_response(
        '404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def error500(request):
    response = render_to_response(
        '500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response


def home(request):

    user = users.get_current_user()

    user = {
        'admin': True if (users.is_current_user_admin() == True) else False,
        'userName': user.nickname(),
        'logoutUrl': users.create_logout_url('/')
    }

    return render(request, "index.html", locals())


# 客戶資料列表
def customers(request):

    user = users.get_current_user()

    if request.method == 'GET':

        user = {
            'admin': True if (users.is_current_user_admin() == True) else False,
            'userName': user.nickname(),
            'logoutUrl': users.create_logout_url('/')
        }

        q = query_type = client_type = ''

        # 查詢值
        if 'q' in request.GET:
            q = request.GET['q'].encode('utf-8').strip()

        # 查詢條件
        if 'query_type' in request.GET:
            query_type = request.GET['query_type']

        # 客戶類型
        if 'client_type' in request.GET:
            client_type = request.GET['client_type']

        # 目前頁數
        if 'current_page' in request.GET:
            current_page = int(request.GET['current_page'])
        else:
            current_page = 1

        # 分頁設定
        Customers.page = current_page
        Customers.limit = 10

        params = {
            'q': q,
            'query_type': query_type,
            'client_type': client_type
        }
        customers = Customers._get_all_customers(params)

        # 搜尋結果筆數
        total = customers['total']

        # 取得分頁
        pager = helper_pager(current_page, total, Customers.limit, params)

        resp_data = {
            'user': user,
            'customers': customers['result'],
            'action': '新增',
            'clientType': {1: '政府', 2: '企業', 3: '個人'},
            'pager': pager,
            'customers_count': total
        }

        return render(request, "customers.html", locals())


# 客戶資料新增
def customers_add(request):

    user = users.get_current_user()

    if request.method == 'GET':

        user = {
            'admin': True if (users.is_current_user_admin() == True) else False,
            'userName': user.nickname(),
            'logoutUrl': users.create_logout_url('/')
        }

        resp_data = {
            'user': user,
            'action': '新增',
            'clientType': {1: '政府', 2: '企業', 3: '個人'}
        }
        return render(request, "customers/customers-data-handle.html", locals())

    else:
        clientName = request.POST['clientName']
        type = int(request.POST['type'])
        clientAddress = request.POST['clientAddress']
        clientTel = request.POST['clientTel']

        createTimeStamp = time.mktime(datetime.now().timetuple())
        Customers._insert_customers(
            type, clientName, clientAddress, clientTel, '備註...', user, createTimeStamp)

        resp_data = {
            'title': '客戶資料',
            'message': '新增成功。 (三秒後自動返回)'
        }

        response = render_to_response('success.html', locals())
        response['refresh'] = '3;URL=/customers/'
        return response


# 客戶資料刪除
def customers_delete(request, id):
    if request.method == 'DELETE':
        Customers._delete_customers(int(id))

        response_data = {}
        response_data['result'] = 1
        response_data['message'] = 'success'

        return HttpResponse(json.dumps(response_data), content_type="application/json")


# 客戶資料修改
def customers_modify(request, id):

    user = users.get_current_user()

    if request.method == 'GET':
        customer = ndb.Key('Customers', int(id)).get()

        user = {
            'admin': True if (users.is_current_user_admin() == True) else False,
            'userName': user.nickname(),
            'logoutUrl': users.create_logout_url('/')
        }

        resp_data = {
            'customer': customer,
            'action': '修改',
            'clientType': {1: '政府', 2: '企業', 3: '個人'}
        }
        return render(request, "customers/customers-data-handle.html", locals())

    elif request.method == 'POST':

        clientName = request.POST['clientName']
        type = int(request.POST['type'])
        clientAddress = request.POST['clientAddress']
        clientTel = request.POST['clientTel']

        _c = Customers()
        customer = _c.get_by_id(int(id))

        customer.clientName = clientName
        customer.type = type
        customer.clientAddress = clientAddress
        customer.clientTel = clientTel
        customer.put()

        resp_data = {
            'title': '客戶資料',
            'message': '修改成功。 (三秒後自動返回)'
        }

        response = render_to_response('success.html', locals())
        response['refresh'] = '3;URL=/customers/'
        return response


# 產生資料
def create(request):
    user = users.get_current_user()
    for i in range(100):
        createTimeStamp = time.mktime(datetime.now().timetuple())
        Customers._insert_customers(
            randint(1, 3), 'Alex', '123', '0975', '備註...', user, createTimeStamp)

    return HttpResponse('Done!!!')
