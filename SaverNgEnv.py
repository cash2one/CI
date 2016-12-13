from TestEnv import *
from SaverngConf import *
from LinkbaseConfMaker import *
import sys
import time
import os


class SaverNgEnv(TestEnv):

    def __init__(self, modulename, hdfsConfMaker, lb=RECV_LB):
        super(SaverNgEnv, self).__init__(modulename, lb)

        self.lb = lb
        self.modulename = modulename
        self.hdfsConfMaker = hdfsConfMaker

        self.mod_home = self.wksp + '/saver_ng'
        self.mod_bin = self.mod_home + '/bin'
        self.mod_conf = self.mod_home + '/conf'
        self.save_pack = self.localConfPath + '/save.pack'
        self.pack_result = '%s/%s_result_pack' % (
            self.result_dir, self.version)

        self.l1linkbase = '%s_dlb_linkbase' % self.modulename
        self.l2linkbase = '%s_l2linkbase' % self.modulename
        self.saverng_bogus_reset = '%s_saverng_bogus_reset' % self.modulename
        self.saverng_proc = '%s_saverng_proc' % self.modulename
        self.saverng_dict_meta = '%s_saverng_dict_meta' % self.modulename
        self.saverng_site_stat = '%s_saverng_site_stat' % self.modulename
        self.saverng_domain_stat = '%s_saverng_domain_stat' % self.modulename
        self.saverng_site_limit = '%s_saverng_site_limit' % self.modulename
        self.saverng_domain_limit = '%s_saverng_domain_limit' % self.modulename

        self.table_list = []
        self.table_list.append(self.l1linkbase)
        self.table_list.append(self.l2linkbase)
        self.table_list.append(self.saverng_bogus_reset)
        self.table_list.append(self.saverng_proc)
        self.table_list.append(self.saverng_dict_meta)
        self.table_list.append(self.saverng_domain_stat)
        self.table_list.append(self.saverng_domain_limit)
        self.table_list.append(self.saverng_site_stat)
        self.table_list.append(self.saverng_site_limit)

        self.table_dic = dict(zip(self.table_list, SCHEMA_DIC[self.module]))
        self.dlb_client = self.mod_bin + '/dlb_client'

    def deploy_modules(self):
        self.deploy_linkbase()

        deploy_modules_cmd = 'cp -prf %s/dlb-linktools %s/dlb-mrframework_new %s; mkdir -p %s/temp' % (
            self.localConfPath, self.localConfPath, self.wksp, self.wksp)
        self.logger.info(deploy_modules_cmd)
        subprocess.call(deploy_modules_cmd, shell=True)

        if self.version == 'test':
            wget_modules_cmd = 'cd %s; %s' % (self.wksp, self.productPath)
        else: 
            wget_modules_cmd = 'cd %s; %s' % (self.wksp, self.path)
        self.logger.info(wget_modules_cmd)
        subprocess.call(wget_modules_cmd, shell=True)

        # after wget we may need extra
        if self.version == 'test':
            deploy_conf_cmd = ' cp -rpf %s/output/saver_ng %s; cd %s ; sh -x deploy.sh %s %s' % (
                self.wksp, self.wksp, self.localConfPath, self.mod_home, self.localConfPath)
        else:
            deploy_conf_cmd = 'cd %s ; tar -xvzf saver_ng.tar.gz ; cd %s ; sh -x deploy.sh %s %s' % (
                self.wksp, self.localConfPath, self.mod_home, self.localConfPath)
        self.logger.info(deploy_conf_cmd)
        subprocess.call(deploy_conf_cmd, shell=True)
        # copy sendmail.sh
        deploy_mail_cmd = 'cd %s; cp sendmail.sh  %s' % (
            self.localConfPath, self.result_dir)
        self.logger.info(deploy_mail_cmd)
        subprocess.call(deploy_mail_cmd, shell=True)

        fetch_teracli_cmd = 'cp -prf %s/teracli %s/dlb_client %s/tera_dict_importer %s/save.pack %s/bin/ && chmod +x %s/bin/*' % (
            self.localConfPath, self.localConfPath, self.localConfPath, self.localConfPath, self.mod_home, self.mod_home)
        self.logger.info(fetch_teracli_cmd)
        ret = subprocess.call(fetch_teracli_cmd, shell=True)
        if ret != 0:
            self.logger.info('fectch teracli failed')
            sys.exit(1)

        fetch_startshell_cmd = 'cp -prf %s/start-saverng.sh %s/stop-saverng.sh %s/bin/' % (
            self.localConfPath, self.localConfPath, self.mod_home)
        self.logger.info(fetch_startshell_cmd)
        ret = subprocess.call(fetch_startshell_cmd, shell=True)

    def deploy_linkbase(self):
        deploy_lb_cmd = 'hadoop fs -rmr %s ; \
                        hadoop fs -mkdir %s ; \
                        hadoop fs -cp %s/* %s/' \
                        % (self.linkbase_hdfs, self.linkbase_hdfs, BASE_LB, self.linkbase_hdfs)
        self.logger.info(deploy_lb_cmd)
        subprocess.call(deploy_lb_cmd, shell=True)

    def bounary_test(self):
        ########################begin boundary test code#######################
        boundary_cache_enable = True
        # follow code will fail if zk channel 0 is occupied
        if boundary_cache_enable:
            self.logger.info("Begin to import boundaries")

            dict_table_name = 'saverng_boundary10'
            boundary = ['0\t!.!\t~.~']

            ret = self.hdfsConfMaker.add_tera_txt_conf(
                boundary,
                dict_table_name,
                TEXT_DICT_SCHEMA,
                DICT_META_BOUNDARY,
                'not_revert_key')

            if not ret:
                self.logger.error(
                    'import dict [%s] failed! please check...' % DICT_META_BOUNDARY)
                #self.checker.report_fail('import dict [%s] failed! please check...' %DICT_META_BOUNDARY)

            confdict = {
                '--zk_support': 'true',
                '--cache_boundary_check_enable': 'true',
                '--cache_boundary_check_debug_enable': 'true',
            }

            confpath = '%s/conf/saver_ng.flag' % self.mod_home
         #   mod_conf(confpath, confdict, '=')
            self.logger.info("Import boundaries end!")

        ##########End boundary test code ################

    def config_module_conf(self, per_small_lb=True):

        config_cmd = 'cd %s &&  python dlb_env_deploy.py -l %s -sng %s -t %s/dlb-linktools -mr %s/dlb-mrframework_new/ 1>%s/deploy.log 2>&1' % (
            self.localConfPath, self.linkbase_hdfs, self.mod_home, self.wksp, self.wksp, self.wksp)
        if per_small_lb:
            config_cmd = '%s --small' % (config_cmd)
        self.logger.info(config_cmd)
        subprocess.call(config_cmd, shell=True)

        # conf_to_modify defined by user
        user_define_confdict = self.confToModifyDic
        # configure dlb-receiver.conf
        filename = 'dlb-receiver.conf'
        confname = '%s/%s' % (self.mod_conf, filename)
        self.logger.info('configuring %s' % confname)

        confdict = {
            'dc_port': str(PORT_DIC[self.modulename][0]),
        }
        if filename in user_define_confdict.keys() and user_define_confdict[filename]:
            confdict = dict(confdict, **user_define_confdict[filename])
            user_define_confdict.pop(filename)
        mod_conf(confname, confdict, separator=':')

        # configure saver_ng.flag
        filename = 'saver_ng.flag'
        confname = '%s/%s' % (self.mod_conf, filename)
        self.logger.info('configuring %s' % confname)

        confdict = {
            '--l1linkbase_table_name': self.l1linkbase,
            '--l2linkbase_table_name': self.l2linkbase,
            '--l1linkbase_stat_table_name': self.saverng_site_stat,
            '--proc_table_name': self.saverng_proc,
            '--dict_meta_table_name': self.saverng_dict_meta,
            '--site_stat_table_name': self.saverng_site_stat,
            '--domain_stat_table_name': self.saverng_domain_stat,
            '--bogus_reset_table_name': self.saverng_bogus_reset,

            '--buf_proc_thread_num': '1',
            '--recv_proc_thread_num': '1',
            '--buf_pool_num': '2',
            '--dns_open': 'false',
            '--segdict_open': 'false',
            '--zk_support': 'false',
            '--zk_server_addr': SAVERNG_ZK_ADDR_LIST,
            '--node_counter': '1',
            '--enable_site_limit': 'false',
            '--enable_domain_limit': 'false',
            '--enable_pattern_del': 'false',
            '--enable_len_site_del': 'false',
            '--enable_len_domain_del': 'false',
            '--enable_pre_site_del': 'false',
            # pre del switch
            '--enable_pre_domain_del': 'false',
            '--enable_pre_stats': 'false',
            # tera read&write fail switch
            '--enable_tera_failed': 'false',
            '--enable_tera_read_failed': 'false',
            '--enable_tera_write_failed': 'false',
            '--cache_boundary_check_enable': 'false',
            '--cache_boundary_check_debug_enable': 'false',
            # spam dead
            '--enable_spam_site_del': 'false',
            '--enable_spam_domain_del': 'false',
            '--enable_dead_site_del': 'false',

        }
        if filename in user_define_confdict.keys() and user_define_confdict[filename]:
            confdict = dict(confdict, **user_define_confdict[filename])
            user_define_confdict.pop(filename)
        mod_conf(confname, confdict, separator='=')

        if not ONEBOX_TERA:

            # configure saver_ng.flag
            filename = 'tera.flag'
            confname = '%s/%s' % (self.mod_conf, filename)
            self.logger.info('configuring %s' % confname)

            confdict = {
                '--tera_zk_addr_list': TERA_ZK_ADDR_LIST,
                '--tera_zk_root_path': TERA_ZK_ROOT_PATH,
                '--tera_ins_enabled': 'false',
                '--tera_zk_enabled': 'true',
            }
            if filename in user_define_confdict.keys() and user_define_confdict['filename']:
                confdict = dict(confdict, **user_define_confdict[filename])
                user_define_confdict.pop(filename)
            mod_conf(confname, confdict, separator='=')

            # other file
        for key, value in user_define_confdict.items():
            if not value:
                continue
            confname = '%s/%s' % (self.mod_conf, key)
            if '.xml' in key:
                mod_normal_file(confname, value)
            else:
                mod_conf(confname, value, separator='=')
        self.bounary_test()

    # def clean_env(self):
    #     pass
