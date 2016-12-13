#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
import subprocess
import json

from Constants import *
from Utils import *


class TestMethod(object):
        # commom test function,mainly for perform test

    def __init__(self, testtype, env, sender, diffenable):
        self.testtype = testtype
        self.env = env
        self.sender = sender
        self.diffenable = diffenable
        self.logger = self.get_logger(self.env.modulename)
        self.period = PERFORM_TEST_TIME
        self.hostname = HOST_NAME

    def startTest(self):
        if self.testtype == 2:
            self.startFuncTest()
        if self.testtype == 1:
            self.startPerformSample()
        if self.testtype == 3:
            self.startPerformSample()
            self.startFuncTest()

    def startFuncTest(self):
        pass

    def startPerformSample(self):
        perSample_cmd = 'cd %s && sh  perSample.sh %s %s' % (
            self.env.localConfPath, self.env.module, self.env.per_log_dir)
        self.logger.info(perSample_cmd)
        subprocess.Popen(perSample_cmd, shell=True)
        return True

    def sendPack(self, pack):
        ret = self.sender.send(pack)
        if ret != 0:
            self.logger.info('send pack failed!')
            return False
        return True

    def stopPerSample(self):
        start = time.time()
        while True:
            self.sendPack(self.env.send_pack)
            now = time.time()
            if (now - start) > self.period:
                break
        stop_perSample_cmd = 'cd %s && sh stopPerSample.sh' % self.env.localConfPath
        self.logger.info(stop_perSample_cmd)
        ret = subprocess.call(stop_perSample_cmd, shell=True)
        if ret != 0:
            self.logger.info('stop perform sample failed!')
            return False
        # send perform log to pat
        self.per_result_path = '%s/per_result_%s' % (
            self.env.result_dir, self.env.version)
        self.per_log_file = '%s/%s.log' % (
            self.env.per_log_dir, self.env.module)

        curl_cmd = 'sed -i "1d" %s ;curl "http://cp01-cq01-testing-ps7109.epc.baidu.com:8911/?r=performance/API&task_name=%s&data_user=liuwenli&comment=testcomment&data_method=ps_method&data_path=ftp://%s/%s">%s' % (
            self.per_log_file, self.env.modulename, self.hostname, self.per_log_file, self.per_result_path)
        self.logger.info(curl_cmd)
        ret = subprocess.call(curl_cmd, shell=True)
        if ret != 0:
            self.logger.info('get perform report failed! ')
            return False
        f = open(self.per_result_path, 'r')
        s = json.load(f)
        self.task_id = s['task_id']
        print self.task_id
        f.close()
        return True

    def get_logger(self, cid):

        subprocess.call('mkdir -p %s' % (self.env.test_log_dir), shell=True)
        logfilename = '%s/testMethod.log' % (self.env.env_log_dir)

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d : %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filemode='w')

        logger = logging.getLogger(cid + '-testMethod')

        # file_hander = logging.FileHandler('%s/nosetest.log' %(self.env.wksp))
        file_hander = logging.FileHandler(logfilename,  mode='w')
        file_hander.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(filename)s:%(lineno)d : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_hander.setFormatter(file_formatter)

        logger.addHandler(file_hander)

        # console printing
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # console formatter
        formatter = logging.Formatter(
            '%(asctime)s: %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console.setFormatter(formatter)
        logger.addHandler(console)

        return logger
