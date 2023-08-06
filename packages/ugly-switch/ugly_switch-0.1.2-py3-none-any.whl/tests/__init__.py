#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-03-20"
__version__ = "0.0.0"

__all__ = ('MyTestCase',)

import unittest
from ugly_switch import switch


class MyTestCase(unittest.TestCase):
    test: bool

    def setUp(self) -> None: self.test = False

    def test_just_switch(self):
        _ = switch[
            'a', lambda: None,
            'b', lambda: setattr(self, 'test', True)
        ]

        self.assertFalse(self.test, 'just creating the switch altered data')

    def test_no_default(self):
        s = switch[
            'a', lambda: None,
            'b', lambda: setattr(self, 'test', True)
        ]
        s('c')
        self.assertFalse(self.test, 'calling with a non-existing value without default altered data')

    def test_no_change(self):
        s = switch[
            'a', lambda: None,
            'b', lambda: setattr(self, 'test', True)
        ]
        s('a')
        self.assertFalse(self.test, 'calling a "wrong" value altered data')

    def test_change(self):
        s = switch[
            'a', lambda: None,
            'b', lambda: setattr(self, 'test', True)
        ]
        s('b')
        self.assertTrue(self.test, 'calling a "right" value did not change data')

    def test_string(self):
        s = switch[
            'setup', self.setUp,
            'b', lambda: setattr(self, 'test', True),
            self.test_change
        ]

        self.assertMultiLineEqual(
            first='switch ?:\n'
                  '\tcase setup: setUp\n'
                  '\tcase b: <lambda>\n'
                  '\tdefault: test_change',
            second=str(s),
            msg='The string method is not correct'
        )


if __name__ == '__main__': pass
