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
    if user:
        user = {
            'userName': user.nickname(),
            'logoutUrl': users.create_logout_url('/')
        }
        return render(request, "index.html", user)
    else:
        return HttpResponseRedirect(users.create_login_url('/'))


# 客戶資料列表
def customers(request):
    user = users.get_current_user()

    if request.method == 'GET':

        q = query_type = query_client_type = ''

        # 查詢值
        if 'q' in request.GET:
            q = request.GET['q'].encode('utf-8').strip()

        # 查詢條件
        if 'query_type' in request.GET:
            query_type = request.GET['query_type']

        # 客戶類型
        if 'query_client_type' in request.GET:
            query_client_type = request.GET['query_client_type']

        # 目前頁數
        if 'currentPage' in request.GET:
            currentPage = int(request.GET['currentPage'])
        else:
            currentPage = 1

        # 分頁設定
        Customers.page = currentPage
        Customers.limit = 10

        params = {
            'q': q,
            'query_type': query_type,
            'customers_type': query_client_type,
        }
        customers = Customers._get_all_customers(params)

        # 搜尋結果筆數
        total = customers['total']
        # 總頁數
        total_page = int(math.ceil(float(total) / float(Customers.limit)))

        # previous
        if currentPage > 1:
            previous = '<li class="waves-effect"><a href="/customers?currentPage=' + str(currentPage - 1) + '&q=' + str(q) + '&query_type=' + str(
                query_type) + '&query_client_type=' + query_client_type + '"><i class="material-icons">chevron_left</i></a></li>'
        else:
            previous = '<li class="disabled"><a href="javascript:;"><i class="material-icons">chevron_left</i></a></li>'

        # 頁數
        page = ''
        page_conut = 1
        while page_conut <= total_page:
            if page_conut == currentPage:
                page += '<li class="active"><a href="/customers?currentPage=' + str(page_conut) + '&q=' + str(q) + '&query_type=' + str(
                    query_type) + '&query_client_type=' + query_client_type + '">' + str(page_conut) + '</a></li>\n'
            else:
                page += '<li class="waves-effect"><a href="/customers?currentPage=' + str(page_conut) + '&q=' + str(
                    q) + '&query_type=' + str(query_type) + '&query_client_type=' + query_client_type + '">' + str(page_conut) + '</a></li>\n'

            page_conut += 1
            pass

        # next
        if currentPage >= total_page:
            next = '<li class="disabled"><a href="javascript:;"><i class="material-icons">chevron_right</i></a></li>'
        else:
            next = '<li class="waves-effect"><a href="/customers?currentPage=' + str(currentPage + 1) + '&q=' + str(q) + '&query_type=' + str(
                query_type) + '&query_client_type=' + query_client_type + '"><i class="material-icons">chevron_right</i></a></li>'

        pager = '''
            <ul class="pagination">
                ''' + previous + page + next + '''
            </ul>
        '''

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

    if request.method == 'GET':
        customer = ndb.Key('Customers', int(id)).get()
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
