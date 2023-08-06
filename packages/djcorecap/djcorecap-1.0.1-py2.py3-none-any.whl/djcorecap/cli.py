# -*- coding: utf-8 -*-

'''
cli
---

console script for djcorecap.
'''


import collections
import click
import datetime as dt
import re
import sys

from django.utils import timezone


def since(since, start=None):
    '''
    calculates starting date using a list of "since" strings
    '''

    if not isinstance(since, collections.abc.Sequence):
        raise TypeError('since arg must be a list or sequence of strings')

    start = timezone.now() if start is None else start
    tzinfo = start.tzinfo

    for s in since:

        hours = re.search('(\d+?)h', s)
        days = re.search('(\d+?)d', s)
        months = re.search('(\d+?)m', s)
        years = re.search('(\d+?)y', s)

        if hours:
            start -= dt.timedelta(hours=int(hours[1]))

        if days:
            start -= dt.timedelta(days=int(days[1]))

        if months:
            for i in range(0, int(months[1])):
                start = dt.datetime(
                    year=start.year - 1 if start.month == 1 else start.year,
                    month=start.month - 1 if start.month > 1 else 12,
                    day=start.day,
                    tzinfo=tzinfo,
                )

        if years:
            start = dt.datetime(
                year=start.year-1,
                month=start.month,
                day=start.day,
                tzinfo=tzinfo,
            )

    return start


@click.command()
def main(args=None):
    '''
    djcorecap command line interface
    '''

    click.echo("update djcorecap.cli.main")
    return 0


def entry_point():
    '''
    required to make setuptools and click play nicely (context object)
    '''

    return sys.exit(main())  # add obj={} to create in context


if __name__ == "__main__":
    entry_point()
