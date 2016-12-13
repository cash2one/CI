#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import logging
import subprocess
import json

from Constants import *
from PacketSender import *
from Tera import *
from Utils import *
from LinkbaseConfMaker import *

from SaverNgEnv import *
from TimefilterEnv import *
from ECEnv import *
from DCEnv import *
from LCEnv import *
from SaverNgTest import *
from TimefilterTest import *
MODULES_ENV_CLASS_DIC = {
    0: SaverNgEnv, 1: TimefilterEnv, 2: ECEnv, 3: DCEnv, 4: LCEnv}

MODULES_TEST_CLASS_DIC ={0: SaverNgTest, 1: TimefilterTest}
# 每个模块的环境配置都新建一个类，并且都继承自类TestmodEnv
# 测试不同模块输入不同moduletype ,对应关系见Constans


class PerformTestPlat(object):

    def __init__(self, moduletype, version, testtype, diffenable = False ,hostname=HOST_NAME, redeploy=True, clean_modEnv=True):
        self.hostname = hostname
        self.redeploy = redeploy
        self.clean_modEnv = clean_modEnv
        self.moduletype = moduletype
        self.version = version
        self.testtype = testtype
        self.diffenable = diffenable

        self.modulename = MODULES_NAME_DIC[moduletype][version]
        self.port = []
        self.port = PORT_DIC[self.modulename]

        self.hdfsConfMaker = LinkbaseConfMaker(self)
        self.modEnv = MODULES_ENV_CLASS_DIC[self.moduletype](self.modulename, hdfsConfMaker=self.hdfsConfMaker)
        self.logger = self.__get_logger__(self.modulename)
        self.packet_sender = PacketSender(self.hostname, self.port[0])
        self.tera = Tera(self.modEnv.mod_bin)
        self.modEnv.deploy(self.clean_modEnv, self.redeploy) 

        
        # hdfsConfMaker checker

        # 性能采点程序

        # 对于不同modules要建的tera表是否一样？
        # 若不一样则由modEnv返回一个表名称的dic,然后传入到_prepare_tera_table中

        self._prepare_tera_tables(self.modEnv.table_dic)

        # 对于词典与table进行一样的处理。
         #self.update_dict_meta(dict_name,table_name)

    def restart_module(self):
        self.stop_module()
#        self.clean()
        self.start_module()
#        self.start_test()

    def start_test(self):
        if self.testtype != 0:
            self.modTest = MODULES_TEST_CLASS_DIC[self.moduletype](self.testtype, self.modEnv, self.packet_sender, self.diffenable)
            self.modTest.startTest()
        if self.testtype == 1 or self.testtype == 3:
            self.modTest.stopPerSample()

    def start_module(self):

        start_mod_cmd = 'cd %s/bin;sh -x start-%s.sh %s %s' % (
            self.modEnv.mod_home, self.modEnv.module, self.port[0], self.version)
        self.logger.info(start_mod_cmd)
        ret = subprocess.call(start_mod_cmd, shell=True)
        if ret != 0:
            self.logger.info("start module %s failed!" % self.modulename)
            return False
        else:
            self.logger.info("start module %s ok!" % self.modulename)
        self.start_test()

    def stop_module(self):
        stop_mod_cmd = 'cd %s/bin;sh -x stop-%s.sh %s ' % (
            self.modEnv.mod_home, self.modEnv.module, self.port[0])
        self.logger.info(stop_mod_cmd)
        ret = subprocess.call(stop_mod_cmd, shell=True)
        if ret != 0:
            self.logger.info("stop module %s failed!" % self.modulename)
            return False
        else:
            self.logger.info("stop module" + self.modulename + "ok!")

    def clean(self):
        #self.modEnv.clean_env()
        pass

    def modify_conf(self, confname, confdict, separator='='):
        confpath = "%s/%s" % (self.modEnv.mod_home, confname)
        self.logger.info('configuring', confpath)
        mod_conf(confpath, confdict, separator)

    def _create_tera_table(self, table_name, table_schema):
        tables_path = '%s/tables' % self.modEnv.mod_home
        table_schema_file = '%s/%s.scm' % (tables_path, table_name)
        if not os.path.exists(tables_path):
            os.mkdir(tables_path)

        with open(table_schema_file, 'w') as schema:
            schema.write("%s%s" % (table_name, table_schema))

        create_table_cmd = "createbyfile %s" % (table_schema_file)
        self.logger.info(create_table_cmd)
        ret = self.tera.recreate_table(table_name, create_table_cmd)
        if not ret:
            self.logger.error('create table %s failed!' % table_name)
            sys.exit(1)
        else:
            self.logger.info('create table %s success!' % table_name)

    def recreate_tera_table(self, table_name, table_schema):
        self._create_tera_table(table_name, table_schema)

    def _prepare_tera_tables(self, table_dic):
        # here we need build tera tables per linkbase
        self.logger.info('first create testcase specific tera tables')
        for table in table_dic.keys():
            self._create_tera_table(table,table_dic[table])

    def update_dict_meta(self, dict_name, table_name):
        #./teracli put  test_saverng_dict_meta  saverng_len_domain_del_dict2 cf:v eee
        update_cmd = 'cd %s && ./teracli put %s %s cf:v %s' % (self.modEnv.mod_bin, self.modEnv.saverng_dict_meta, dict_name, table_name)
        self.logger.info(update_cmd)
        ret = subprocess.call(update_cmd, shell=True)
        if ret != 0:
            self.logger.info("update saverng dict_meta failed!")
            return False

        return True

    # def performSample(self):
    #     perSample_cmd = 'cd %s && sh  perSample.sh %s %s' %(self.modEnv.localConfPath, self.modEnv.module, self.modEnv.per_log_dir) 
    #     self.logger.info(perSample_cmd)
    #     subprocess.Popen(perSample_cmd, shell = True)
    #     return True


    # def stopPerSample(self):
    #     start = time.time()
    #     while True:
    #         self.sendPack()
    #         now = time.time()
    #         print "start is : ", start
    #         print "now is :", now
    #         print "period is :", self.period
    #         if (now - start) > self.period:
    #             break;
    #     stop_perSample_cmd = 'cd %s && sh stopPerSample.sh' %self.modEnv.localConfPath
    #     self.logger.info(stop_perSample_cmd)
    #     ret = subprocess.call(stop_perSample_cmd, shell = True)
    #     if ret != 0:
    #         self.logger.info('stop perform sample failed!')
    #         return False
    #     #send perform log to pat
    #     self.per_result_path = '%s/per_result_%s' %(self.modEnv.result_dir, self.modEnv.version)
    #     self.per_log_file = '%s/%s.log' %(self.modEnv.per_log_dir, self.modEnv.module)

    #     curl_cmd = 'sed -i "1d" %s ;curl "http://cp01-cq01-testing-ps7109.epc.baidu.com:8911/?r=performance/API&task_name=%s&data_user=liuwenli&comment=testcomment&data_method=ps_method&data_path=ftp://%s/%s">%s' %(self.per_log_file, self.modEnv.modulename, self.hostname ,self.per_log_file, self.per_result_path)
    #     self.logger.info(curl_cmd)
    #     ret = subprocess.call(curl_cmd, shell = True)
    #     if ret != 0:
    #         self.logger.info('get perform report failed! ')
    #         return False
    #     f = open(self.per_result_path,'r')
    #     s = json.load(f)
    #     self.task_id = s['task_id']
    #     print self.task_id
    #     f.close()
    #     return True

    def sendPack(self):
        ret = self.packet_sender.send(self.modEnv.send_pack)
        if ret != 0:
            return False
        return True

    def __get_logger__(self, cid):

        case_log_dir = '%s/' % (self.modEnv.logdir)
        subprocess.call('mkdir -p %s' % (case_log_dir), shell=True)
        logfilename = '%s/auto_plat_test.log' % (case_log_dir)

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d : %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filemode='a')

        logger = logging.getLogger(cid + '-RecvTestCase')

        #file_hander = logging.FileHandler('%s/nosetest.log' %(self.modEnv.wksp))
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
