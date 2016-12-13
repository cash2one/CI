#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PerformTestPlat import *


test = None

def setup():
    global test
    print "what module you want to test?  Please input the moduleType(0-5) which (represent saverng timefilter EC DC LC)"
    moduleType = 0
    print "Please choose which version you want to test. (0 for online, 1 for test)"
    ver = 1
    test = PerformTestPlat(moduletype = moduleType, version = ver)
    test.restart_module()

def test_first_crawl_succ_time_packs():
    global test
    pass

def teardown():
    global test
    pass
