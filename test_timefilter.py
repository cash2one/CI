#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PerformTestPlat import *


test = None

def setup():
    global test
    moduleType = 1
    ver = 0
    test = PerformTestPlat(moduletype = moduleType, version = ver)
    test.restart_module()

def test_first_crawl_succ_time_packs():
    global test
    pass

def teardown():
    global test
    test.stopPerSample()
