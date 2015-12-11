from django import template

register = template.Library()


@register.filter
def get_value_by_key(dict, key):
    try:
        return dict[key]
    except KeyError:
        return
