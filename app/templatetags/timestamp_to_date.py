from datetime import datetime, timedelta
from django import template
from django.conf import settings
from pytz.gae import pytz

register = template.Library()


@register.filter("utc_to_loacltz")
def utc_to_loacltz(value):
    try:
        localtz = pytz.timezone(settings.TIME_ZONE)
        return datetime.fromtimestamp(value, localtz)
    except AttributeError:
        return ''
