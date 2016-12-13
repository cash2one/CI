#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from SaverngConf import *
MODULES_NAME_DIC = {0: ['saverng-online', 'saverng-test'], 1: ['timefilter-online', 'timefilter-test'],
                    2: ['EC-online', 'EC-test'], 3: ['DC-online', 'DC-test'], 4: ['LC-online', 'LC-test']}
# 各模块监听端口号
PORT_DIC = {'saverng-online': [12345, 12346],
            'saverng-test': [12347],
            'timefilter-online': [9958, 9959],
            'timefilter-test': [19958, 19959],
            'DC-online': [19235, 19236, 19237],
            'DC-test': [29235, 29236, 29237]}
# 部署目录 以及 机器名称
HOST_NAME = 'nmg01-ps-ps-hunbu1wm2290.nmg01.baidu.com'
HOME = '/home/spider/workspacezr/performTestPlat'
PERFORM_TEST_TIME = 120

# 发布机地址
PATH_DIC = {
    'saverng': 'wget ftp://yq01-spi-fabu0.yq01.baidu.com//home/spider/saverng/saverng_online/saver_ng.tar.gz',
    'timefilter': 'wget -r -nH -N --preserve-permissions --level=0 --cut-dirs=3 --retr-symlinks  ftp://yq01-spi-tfss20.yq01.baidu.com/home/spider/timefilter',
    'DC': 'wget -r -nH --preserve-permissions --level=0 --cut-dirs=3 --retr-symlinks  ftp://yq01-spi-ddc8.yq01.baidu.com/home/spider/dc',
}

#产品库地址
PRODUCT_PATH_DIC = {
        'saverng' : 'wget -r -nH --level=0 --cut-dirs=9 getprod@buildprod.scm.baidu.com:/temp/data/prod-64/ps/spider/saver-ng/CITASK/r138392-2555437/  --user getprod --password getprod --preserve-permissions',
        'timefilter' : 'wget -r -nH -N --level=0 --cut-dirs=9 getprod@buildprod.scm.baidu.com:/temp/data/prod-64/ps/spider/timefilter/CITASK/r138366-2537780/  --user getprod --password getprod --preserve-permissions',
        'DC' : {
                'frame' : 'wget -r -nH --preserve-permissions --level=0 --cut-dirs=9 ftp://getprod:getprod@product.scm.baidu.com:/data/prod-unit/prod-64/ps/spider/frame-dc/frame/frame_1-0-67-0_PD_BL/product',
                'strategy' : 'wget -r -nH --preserve-permissions --level=0 --cut-dirs=9 ftp://getprod:getprod@product.scm.baidu.com:/data/prod-unit/prod-64/ps/spider/frame-dc/strategy/strategy_1-0-116-0_PD_BL/product',
                'frame2' : 'wget -r -nH --preserve-permissions --level=0 --cut-dirs=7 ftp://getprod:getprod@product.scm.baidu.com:/data/prod-64/ps/spider/frame-dc/frame/frame_1-0-67-0_PD_BL',
                'strategy2' : 'wget -r -nH --preserve-permissions --level=0 --cut-dirs=7 ftp://getprod:getprod@product.scm.baidu.com:/data/prod-64/ps/spider/frame-dc/strategy/strategy_1-0-116-0_PD_BL'
        }
}

# 配置文件的修改项
CONF_DICT = {
    'saverng-online': {
        'dlb-receiver.conf': {'dc_port': str(PORT_DIC['saverng-online'][0])},
        'saver_ng.flag': {},
        'tera.flag': {}
    },
    'saverng-test': {
        'dlb-receiver.conf': {},
        'saver-ng.flag': {},
        'tera.flag': {}
    },
    'timefilter-online': {
        'timefilter.conf': {},
        'dictmerge.conf': {},
        'signclient.conf': {},
        'dictclient' : {}
    },
    'timefilter-test': {
        'timefilter.conf': {},
        'dictmerge.conf': {},
        'signclient.conf': {},
        'dictclient' : {}
    },
    'DC-online': {
        'distribute2.conf': {
            'ec_thread_num': '10',
            'COMLOG_DEVICE_NUM': '2',
            'ip_access_control': '127.0.0.1',
            'info_collect_level': '3'
        },
        'policy.xml': {
            '<DupDomain usededup="1"': '<DupDomain usededup="0"'
        }
    },
    'DC-test': {
        'distribute2.conf': {
            'ec_thread_num': '10',
            'COMLOG_DEVICE_NUM': '2',
            'ip_access_control': '127.0.0.1',
            'info_collect_level': '3'
        },
        'policy.xml': {}
    }
}

BASE_LB = '/user/spider/deployment/linkbase_autotest'
LINKBASE = '/user/spider/autotest'
RECV_LB = '%s/dlb-receiver' % LINKBASE

WORKSPACE = '%s/data' % HOME
CONF_PATH = '%s/conf' % HOME
LOG_PATH = '%s/log' % HOME
RESULT_PATH = '%s/result' % HOME

SCHEMA_DIC = {
    'saverng': [DLB_LINKBASE_SCHEMA, L2LINKBASE_SCHEMA, BOGUS_RESET_SCHEMA, PROC_SCHEMA, DICT_META_SCHEMA, DOMAIN_STAT_SCHEMA, DOMAIN_LIMIT_SCHEMA, SITE_STAT_SCHEMA, SITE_LIMIT_SCHEMA],
    'timefilter': ['', '', '']
}

ONEBOX_TERA = True
TERA_ZK_ADDR_LIST = 'nmg01-ps-ps-hunbu1wm2284.nmg01.baidu.com:18682'
TERA_ZK_ROOT_PATH = '/qa-test/tera'

TIME_NOW_FOR_TEST = str(time.time()).split('.')[0]

DICT_IMPORTER_BIN = 'tera_dict_importer'
