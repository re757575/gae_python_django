#coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from datetime import datetime
import random
import logging
import models
import time
import json

from google.appengine.api import users

def home(request):

    # if request.method == 'GET':
    #     logging.info('GET')
    #     if 'section' in request.GET and request.GET['section'] is not None and request.GET['section'] != '':
    #         logging.info(request.GET['section'])
    # elif request.method == 'POST':
    #     logging.info('POST')

    user = users.get_current_user()
    if user:
        user = {
            'userName': user.nickname(),
            'logoutUrl': users.create_logout_url('/')
        }
        return render(request, "index.html", user)
    else:
        return HttpResponseRedirect(users.create_login_url('/'))

def customers(request):
    logging.basicConfig(level=logging.INFO)

    user = users.get_current_user()

    if request.method == 'GET':
        # if user is None:
        #     return HttpResponseRedirect(users.create_login_url('/'))

        excuses = [
            "It was working in my head",
            "I thought I fixed that",
            "Actually, that is a feature",
            "It works on my machine",
        ]
        excuse = random.choice(excuses)

        customers = models.AllCustomers()

        data = {
            'user': user,
            'excuse': excuse,
            'customers': customers
        }

        # cc = models.Customers.query().filter(models.Customers.clientName == '4').fetch()

        logging.info(customers)

        return render(request, "customers.html", data)

    elif request.method == 'POST':
        # logging.info(request.POST)

        clientName = request.POST['clientName']
        type = int(request.POST['type'])
        clientAddress = request.POST['clientAddress']
        clientTel = request.POST['clientTel']

        createTimeStamp = time.mktime(datetime.now().timetuple())
        models.InsertCustomers(type, clientName, clientAddress, '備註...', user, createTimeStamp)

        respData = {
            'title': '客戶資料',
            'message': '新增成功。 (三秒後自動返回)'
        }

        response = render_to_response('success.html', respData);
        response['refresh'] = '3'
        response['URL'] = '/customers/'
        return response


def customersDelete(request, id):
    if request.method == 'DELETE':
        models.DeleteCustomers(int(id));

        response_data = {}
        response_data['result'] = 1
        response_data['message'] = 'success'

        return HttpResponse(json.dumps(response_data), content_type="application/json")
