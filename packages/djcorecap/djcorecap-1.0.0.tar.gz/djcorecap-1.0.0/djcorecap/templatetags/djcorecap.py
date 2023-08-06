 # -*- coding: utf-8 -*-

'''
djcorecap/templatetags/core
---------------------------

core templatetags for the djcorecap app
'''

import re

from django import template
from django.urls import reverse, NoReverseMatch


register = template.Library()


@register.simple_tag(takes_context=True)
def active_url(context, url):
    '''
    returns 'active' if url matches request.path in context
    '''

    path = getattr(context.get('request', object()), 'path', '')

    try:

        # if url reverses, use that as the pattern (e.g. '/foo/')
        pattern = '^%s$' % reverse(url)

    except NoReverseMatch as e:

        # otherwise use url as the pattern
        pattern = url

    return 'active' if re.search(pattern, path) else ''


@register.filter
def get(obj, key):
    '''
    returns value for key in dict, list, or object
    '''

    k = str(key)

    if isinstance(obj, dict):
        return obj.get(k)

    elif hasattr(obj, k):

        if hasattr(getattr(obj, k), '__call__'):
            return getattr(obj, k)()

        return getattr(obj, k)

    elif isinstance(obj, list):
        return obj[key]

    return obj  # django docs say to not raise exceptions on errors


@register.filter
def percent(dec, digits=2):
    '''
    transforms decimals into percentages to significant digits
    '''

    try:

        return round(float(dec) * 100, digits)

    except Exception as e:

        return dec
