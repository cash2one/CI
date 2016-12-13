#!/bin/env  python
# -*- coding: utf-8 -*- 

import time
from Constants import *
from Utils import *
import subprocess

class MakeDataError(Exception): pass

class LinkbaseConfMaker(object):
    """docstring for DataMaker"""
    def __init__(self, testcase):
        super(LinkbaseConfMaker, self).__init__()
        self.test = testcase
        self.hdfs_confs = []

    

    ###add tera conf pre saverng
    def add_tera_txt_conf(self, conf_content, dict_table_name, table_schema, 
        dict_meta_name, no_revert_key=''):
        '''
        使用tera_dict_importer工具导入文本词典
        输入格式：第一列为站点或者主域或者prefix或者url；后面N列为配置信息
        @param conf_content - 配置内容list列表
        @param dict_table_name - 字典名称
        @param table_schema - 字典表的schema
        @param dict_meta_name - 字典在saverng_dict_meta里面注册的名称
        @param no_revert_key - 是否反转的url,默认是反转url
        '''
        #first create table
        self.test.recreate_tera_table(dict_table_name, table_schema)
     
        #then import conf content
        temp_conf_file = '%s/%s.%s' %(self.test.modEnv.temp_dir, 
                                    dict_table_name, str(time.time()))
        with open(temp_conf_file, 'w') as temp_conf:
            for item in conf_content:
                temp_conf.write(item + '\n')

        import_dict_cmd = 'cd %s && cat %s | ./%s -t %s %s' %(self.test.modEnv.mod_bin, 
            temp_conf_file, DICT_IMPORTER_BIN, dict_table_name, no_revert_key)
        self.test.logger.info(import_dict_cmd)
        ret = subprocess.call(import_dict_cmd, shell = True)

        if ret != 0:
            self.test.logger.error('import dict [%s] failed! please check...' %dict_meta_name)
            return False

        #update saverng_dict_meta
        ret = self.test.update_dict_meta(dict_meta_name, dict_table_name)
        if not ret:
            self.test.logger.error('update dict meta [%s] failed! please check...' %dict_meta_name)
            return False

        return True

    def add_hdfs_txt_conf(self, conf_content, hdfs_conf_path, reduce_num = 1, index_step=2):
        conf_property = {}
        conf_property['content'] = conf_content
        conf_property['path'] = hdfs_conf_path
        conf_property['reduce_num'] = reduce_num
        conf_property['index_step'] = index_step
        self.hdfs_confs.append(conf_property)

    def upload_hdfs_raw_txt_conf(self, conf_content, hdfs_conf_path, seperator='\t'):
        if hdfs_conf_path[-1] == '/':
            hdfs_conf_path = hdfs_conf_path[:-1]

        hdfs_conf_name = hdfs_conf_path[hdfs_conf_path.rfind('/')+1:]
        hdfs_conf_dir = hdfs_conf_path[:hdfs_conf_path.rfind('/')]
        temp_conf_file = '%s/%s.%s' %(self.test.env.temp_dir, hdfs_conf_name, str(time.time()))
        with open(temp_conf_file, 'w') as temp_conf:
            for item in conf_content:
                split_item = item.split(seperator)
                m_url = split_item[0]
                    
                key = m_url
                if is_url_a_prehold(m_url):
                    key = m_url
                    m_url = self.test.env.m_url_map[m_url]

                    item = m_url + seperator + seperator.join(split_item[1:])
                    item = item.strip()

                temp_conf.write(item + '\n')

        #upload the conf to hdfs: remove old files, put new files into hdfs
        upload_cmd = 'hadoop fs -rmr %s*;  hadoop fs -mkdir %s; hadoop fs -put %s %s; rm -rf %s' %(hdfs_conf_path, hdfs_conf_dir, temp_conf_file, hdfs_conf_path, temp_conf_file)
        subprocess.call(upload_cmd, shell = True)
        self.test.logger.info(upload_cmd)

    def make_hdfs_conf(self):
         for conf in self.hdfs_confs:
            self.upload_and_spilt_hdfs_conf(conf['content'], conf['path'], conf['reduce_num'], conf['index_step'])

    def upload_and_spilt_hdfs_conf(self, conf_content, hdfs_conf_path, reduce_num = 1, index_step=2):
        '''
        upload hdfs conf, then split the conf to generate conf index
        @parameter:
            conf_content    list of conf content, each item at one line
            hdfs_conf_name  name of conf
            hdfs_conf_path  hdfs path of the conf
            reduce_num      reduce number per the splitter
            index_step      index step for splitter to write index file

        @note: this function only support the situation that there is only one part of conf file, 
                all conf_content will be wrote into a file(part-00000).
        '''
        if hdfs_conf_path[-1] == '/':
            hdfs_conf_path = hdfs_conf_path[:-1]

        hdfs_conf_name = hdfs_conf_path[hdfs_conf_path.rfind('/')+1:]
        temp_conf_file = '%s/%s.%s' %(self.test.env.temp_dir, hdfs_conf_name, str(time.time()))
        with open(temp_conf_file, 'w') as temp_conf:
            for item in conf_content:
                temp_conf.write(item + '\n')

        #upload the conf to hdfs: mkdir, remove old files, put new files into hdfs
        subprocess.call('hadoop fs -rmr %s*; hadoop fs -mkdir %s; hadoop fs -put %s %s/part-00000' %(hdfs_conf_path, hdfs_conf_path, temp_conf_file, hdfs_conf_path), shell = True)


        sample_path = '%s/sample_sort_url' %(hdfs_conf_path)
        l1_linkbase_sample_sort_url = '%s/data/0/sample_sort_url' %(self.test.env.l1_linkbase_hdfs)
        
        if hadoop_exists(l1_linkbase_sample_sort_url):
            sample_path = l1_linkbase_sample_sort_url
        else:
            #cd dlb-saver/bin/dlb-sampleurl
            dlb_sampleurl = "cd %s/bin/dlb-sampleurl/; sh -x run_dlb_sampleurl.sh %s/part-* %s SUC %s %s_tmp &>%s/dlb_sampleurl.log; cd -" %(self.test.env.dlb_saver_home, hdfs_conf_path, sample_path, 2, sample_path, self.test.env.wksp)

            self.test.logger.info(dlb_sampleurl)
            ret = subprocess.call(dlb_sampleurl, shell = True)
            if ret != 0:
                self.test.logger.error('dlb_sampleurl failed, ret=%s, please check the log: [dlb_sampleurl.log]' %(ret))

        #split the conf
        dlb_splitter = "%s/dlb-splitter/run_dlb_splitter.sh -i %s/part-* -o %s/temp/ -S %s -t 0 -x -r %s -L 1 -P 150000000 -D 50000000 -s %s &>%s/dlb_splitter.log" %(self.test.env.dlb_linktools, hdfs_conf_path, hdfs_conf_path, sample_path, reduce_num, index_step, self.test.env.wksp)

        self.test.logger.info(dlb_splitter)
        ret = subprocess.call(dlb_splitter, shell = True)

        if ret != 0:
            self.test.logger.error('conf_dlb_splitter failed, ret=%s, please check the log: [conf_dlb_splitter.log]' %(ret))

        #restore splitted conf to its right place
        #for zombie set
        restore_splitted_conf = "hadoop fs -rmr %s/part-*; hadoop fs -cp %s/temp/part-* %s; hadoop fs -cp %s/temp.index %s.index;" %(hdfs_conf_path, hdfs_conf_path, hdfs_conf_path, hdfs_conf_path, hdfs_conf_path)

        self.test.logger.info(restore_splitted_conf)
        ret = subprocess.call(restore_splitted_conf, shell = True)

        if ret != 0:
            self.test.logger.error('restore_splitted_conf failed, ret=%s' %(ret))
