#!/usr/bin/env python
# -*- coding: utf-8 -*-
from TestEnv import *
from LinkbaseConfMaker import *
import sys
import os
import subprocess

class DCEnv(TestEnv):
	def __init__(self, modulename, hdfsConfMaker, lb = RECV_LB):
		super(DCEnv, self).__init__(modulename, lb)
		self.modulename = modulename

		self.mod_home = self.wksp + '/DC'
		self.mod_bin  = self.mod_home + '/bin'
		self.mod_conf = self.mod_home + '/conf'
		self.dataPath = self.mod_home + '/data'
		self.getDataPath = self.mod_home + '/GetData'
		self.Index = self.mod_home + '/Index'

		self.productFramePath = self.productPath['frame']
		self.productStrategyPath = self.productPath['strategy']
		self.productFramePath2 = self.productPath['frame2'] 
		self.productStrategyPath2 = self.productPath['strategy2']

		self.framePath = self.Index + '/frame'
		self.strategyPath = self.Index + '/strategy'

		mkdir_if_not_exists(self.mod_home)
		mkdir_if_not_exists(self.framePath)
		mkdir_if_not_exists(self.strategyPath)

	def deploy_modules(self):
		#wget from publish and product machine
		wget_modules_cmd = 'cd %s; %s/bin; %s/conf; %s/lib' %(self.mod_home, self.path, self.path, self.path)
		self.logger.info(wget_modules_cmd)
		subprocess.call(wget_modules_cmd, shell = True)

		if self.version == 'test':
			get_product_cmd = 'cd %s; rm -rf ./*; %s; cd %s; rm -rf ./*; %s' %(self.framePath, self.productFramePath, self.strategyPath, self.productStrategyPath)
			self.logger.info(wget_modules_cmd)
			subprocess.call(wget_modules_cmd, shell = True)

			## 判断是否成功wget，该目录下是否有文件。若没有，则使用路径2.

			merge_bin_cmd = 'cp -rf %s/output/bin/ %s; cp -rf %s/output/bin/ %s' %(self.framePath, self.mod_home, self.strategyPath, self.mod_home)
			self.logger.info(merge_bin_cmd)
			subprocess.call(merge_bin_cmd, shell = True)

		deploy_conf_cmd = 'cd %s; cp wap_dup_ss.conf dedup_domain.conf bigpipe.conf redir_type_ss.conf %s' %(self.localConfPath, self.mod_conf)
		self.logger.info(deploy_conf_cmd)
		subprocess.call(deploy_conf_cmd, shell = True)

		deploy_mail_cmd = 'cd %s; cp sendmail.sh  %s' % (self.localConfPath, self.result_dir)
                self.logger.info(deploy_mail_cmd)
                subprocess.call(deploy_mail_cmd, shell=True)

                fetch_startshell_cmd = 'cd %s; cp -rf start-DC.sh stop-DC.sh teracli trap_dc.sh %s' % (
                    self.localConfPath, self.mod_bin)
                self.logger.info(fetch_startshell_cmd)
                subprocess.call(fetch_startshell_cmd, shell=True)


        def config_module_conf(self, per_small_lb=True):
            # configure timefilter.conf
            user_define_confdict = self.confToModifyDic
            filename = 'distribute2.conf'
            confname = '%s/%s' %(self.mod_conf, filename)
            self.logger.info('configuring %s' % confname)

            confdict = {
                'esp_port': str(PORT_DIC[self.modulename][1]),
                'ec_listen_port': str(PORT_DIC[self.modulename][0]),
                'ec_listen_urgent_port' : str(PORT_DICT[self.modulename][2]),
            }
            if filename in user_define_confdict.keys() and user_define_confdict[filename]:
                confdict = dict(confdict, **user_define_confdict[filename])
                user_define_confdict.pop(filename)
    
            mod_conf(confname, confdict, separator=':')
    
    
            # configure policy.xml or other file
            for key,value in user_define_confdict.items():
                if not value:
                    continue
                confname = '%s/%s' %(self.mod_conf, key)
                if '.xml' in key:
                    mod_normal_file(confname, value)
                else:
                    mod_conf(confname, value, separator = ':')
    
