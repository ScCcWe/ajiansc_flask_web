# !/usr/bin/env python
# -*- coding: utf-8 -*-
# file_name: test_for_foo.py
# author: ScCcWe
# time: 2020/4/19 11:05


import unittest

from .foo import sayhello


class SayHelloTestCase(unittest.TestCase):
    def setUp(self) -> None:  # 测试固件，在每个测试方法前被调用
        pass

    def tearDown(self) -> None:  # 测试固件，在每个测试方法后被调用
        pass

    def test_sayhello(self):
        rv = sayhello()  # rv return value
        self.assertEqual(rv, 'Hello!')

    def test_sayhello_to_somebody(self):
        rv = sayhello(to='Grey')
        self.assertEqual(rv, 'Hello, Grey!')


if __name__ == '__main__':
    unittest.main()
