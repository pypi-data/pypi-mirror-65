#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test
----

unit tests for djcorecap package
'''

from click.testing import CliRunner
import datetime as dt
import unittest

from djcorecap import cli


class TestDjcorecap(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_since(self):
        start = dt.datetime(year=2019, month=1, day=1, hour=23, minute=59, second=59)
        since_1h = cli.since(['1h'], start)
        since_1d = cli.since(['1d'], start)
        since_1m = cli.since(['1m'], start)
        since_1y = cli.since(['1y'], start)
        self.assertIsInstance(since_1h, dt.datetime)
        self.assertEqual(since_1h.hour, 22)
        self.assertEqual(since_1d.day, 31)
        self.assertEqual(since_1m.month, 12)
        self.assertEqual(since_1y.year, 2018)

    def test_command_line_interface(self):
        result = self.runner.invoke(cli.main)
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(cli.main, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue('Show this message and exit.' in result.output)
