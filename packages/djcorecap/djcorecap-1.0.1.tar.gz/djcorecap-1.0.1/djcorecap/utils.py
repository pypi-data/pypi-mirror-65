# -*- coding: utf-8 -*-

'''
djcorecap/utils
---------------

utility functions, etc. for the djcorecap app
'''


def get_client_ip(request):
    '''
    extracts external IP from HTTP requests
    '''

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()

    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip
