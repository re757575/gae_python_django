# coding=utf-8

from django.template import RequestContext
from django.shortcuts import render_to_response

import logging


class FilterIPMiddleware(object):
    # Check if client IP is allowed

    def process_request(self, request):

        allowed_ips = ['127.0.0.1', '::1']  # Authorized ip's
        ip = request.META.get('REMOTE_ADDR')  # Get client IP
        msg = 'IP: {ip} 無權限瀏覽'.format(ip=request.META.get('REMOTE_ADDR'))

        if ip not in allowed_ips:
            response = render_to_response(
                '403.html', {'msg': msg}, context_instance=RequestContext(request))
            response.status_code = 403
            return response

       # If IP is allowed we don't do anything
        return None

    def process_response(self, request, response):
        return response
