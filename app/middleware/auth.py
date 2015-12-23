# coding=utf-8

from django.http import HttpResponseRedirect

from google.appengine.api import users

import logging


class GoogleAuthMiddleware(object):
    # 檢查是否已登入

    def process_request(self, request):

        # logging.info(request.get_full_path())
        user = users.get_current_user()
        if user is None:
            return HttpResponseRedirect(users.create_login_url('/'))

        return None

    def process_response(self, request, response):
        return response
