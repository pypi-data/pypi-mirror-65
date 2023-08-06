# -*- coding: utf-8 -*-

'''
djcorecap/models
----------------

django model and manager helper functions
'''

from django.db import connection


class SqlExecuteDict(object):
    '''
    mixin for raw SQL queries returning a dict
    '''

    def query_dict(self, query, *args):
        '''
        execute raw sql and return list of dicts
        '''

        with connection.cursor() as cursor:

            cursor.execute(query, params=args)

            columns = [c[0] for c in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
