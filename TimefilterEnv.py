from TestEnv import *
from LinkbaseConfMaker import *
import sys
import os
import subprocess


class TimefilterEnv(TestEnv):

    def __init__(self, modulename, hdfsConfMaker, lb=RECV_LB):
        super(TimefilterEnv, self).__init__(modulename, lb)
        self.modulename = modulename

        self.mod_home = self.wksp + '/timefilter'
        self.mod_bin = self.mod_home + '/bin'
        self.mod_conf = self.mod_home + '/conf'
        self.getDataPath = self.mod_home + '/GetData'
        self.dataPath = self.mod_home + '/data'
        self.Index = self.mod_home + '/Index'

        self.saver_pack_result = self.result_dir + \
            '/saver_result_pack_' + self.version
        self.linkcache_pack_result = self.result_dir + \
            '/linkcache_result_pack_' + self.version

        self.mergdict_name = 'mergdict_%s' % self.modulename
        self.signserver_name = 'signserver_%s' % self.modulename
        self.signdict_name = 'signdict_%s' % self.modulename
        self.table_list = []
        self.table_list.append(self.mergdict_name)
        self.table_list.append(self.signserver_name)
        self.table_list.append(self.signdict_name)

        self.table_dic = dict(zip(self.table_list, SCHEMA_DIC[self.module]))
        print self.table_dic
        mkdir_if_not_exists(self.mod_home)
        mkdir_if_not_exists(self.Index)

    def cleanData(self):
        remove_data_cmd = 'rm -rf %s/*' % self.dataPath
        self.logger.info(remove_data_cmd)
        subprocess.call(remove_data_cmd, shell=True)

    def clean_env(self):
        clean_env_cmd = 'cd %s; ls | grep -v bin | grep -v conf | grep -v Index | xargs rm -rf' %self.mod_home
        self.logger.info(clean_env_cmd)
        subprocess.call(clean_env_cmd, shell = True)
        mkdir_if_not_exists('%s/log' % self.mod_home)
        mkdir_if_not_exists('%s/status' % self.mod_home)
        mkdir_if_not_exists('%s/GetData' % self.mod_home)

    def deploy_modules(self):

        # wget from publish machine
        wget_modules_cmd = 'cd %s; %s/bin; %s/conf' % (self.mod_home, self.path, self.path)
        self.logger.info(wget_modules_cmd)
        subprocess.call(wget_modules_cmd, shell=True)
        if self.version == 'test':
            # GetProduct wget from agile
            get_product_cmd = 'cd %s;  %s ;cp -rf %s/output/bin/ %s' % (
                self.Index, self.productPath, self.Index, self.mod_home)
            self.logger.info(get_product_cmd)
            subprocess.call(get_product_cmd, shell=True)

        # LocalConf
        # ModifyIndexConf
        deploy_conf_cmd = 'cd %s; cp dictclient.conf dictmerge.conf signclient.conf tera.flag users timefilter.conf  %s' % (
            self.localConfPath, self.mod_conf)
        self.logger.info(deploy_conf_cmd)
        subprocess.call(deploy_conf_cmd, shell=True)

        deploy_mail_cmd = 'cd %s; cp sendmail.sh  %s' % (
            self.localConfPath, self.result_dir)
        self.logger.info(deploy_mail_cmd)
        subprocess.call(deploy_mail_cmd, shell=True)

        fetch_startshell_cmd = 'cd %s; cp -rf start-timefilter.sh stop-timefilter.sh teracli trap_tf.sh %s/bin' % (
            self.localConfPath, self.mod_home)
        self.logger.info(fetch_startshell_cmd)
        ret = subprocess.call(fetch_startshell_cmd, shell=True)

    def config_module_conf(self, per_small_lb=True):

        user_define_confdict = self.confToModifyDic
        # configure timefilter.conf
        filename = 'timefilter.conf'
        confname = '%s/%s' % (self.mod_conf, filename)
        self.logger.info('configuring %s' % confname)

        confdict = {
            'esp_port': str(PORT_DIC[self.modulename][1]),
            'dc_port': str(PORT_DIC[self.modulename][0])
        }
        if filename in user_define_confdict.keys() and user_define_confdict[filename]:
            confdict = dict(confdict, **user_define_confdict[filename])
            user_define_confdict.pop(filename)
        mod_conf(confname, confdict, separator=':')

        # configure dictclient.conf
        filename = 'dictclient.conf'
        confname = '%s/%s' % (self.mod_conf, filename)
        self.logger.info('configuring %s' % confname)

        confdict = {
            'tera_table_name': self.mergdict_name
        }
        if filename in user_define_confdict.keys() and user_define_confdict[filename]:
            confdict = dict(confdict, **user_define_confdict[filename])
            user_define_confdict.pop(filename)
        mod_conf(confname, confdict, separator=':')

        # configure dictmerge.conf
        filename = 'dictmerge.conf'
        confname = '%s/%s' % (self.mod_conf, filename)
        self.logger.info('configuring %s' % confname)

        confdict = {
            'tera_table_name': self.signserver_name
        }
        if filename in user_define_confdict.keys() and user_define_confdict[filename]:
            confdict = dict(confdict, **user_define_confdict[filename])
            user_define_confdict.pop(filename)
        mod_conf(confname, confdict, separator=':')

        # configure signclient.conf
        filename = 'signclient.conf'
        confname = '%s/%s' % (self.mod_conf, filename)
        self.logger.info('configuring %s' % confname)

        confdict = {
            'tera_table_name': self.signdict_name
        }
        if filename in user_define_confdict.keys() and user_define_confdict[filename]:
            confdict = dict(confdict, **user_define_confdict[filename])
            user_define_confdict.pop(filename)
        mod_conf(confname, confdict, separator=':')

        # other file
        for key, value in user_define_confdict.items():
            if not value:
                continue
            confname = '%s/%s' % (self.mod_conf, key)
            if '.xml' in key:
                mod_normal_file(confname, value)
            else:
                mod_conf(confname, value, separator=':')
