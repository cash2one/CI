from Constants import *
from Utils import *


class TestEnv(object):

    def __init__(self, modulename, lb):
        self.lb = lb
        self.modulename = modulename
        self.module = self.modulename.split('-')[0]
        self.version = self.modulename.split('-')[1]
        self.wksp = '%s/%s/%s' % (WORKSPACE, self.module, self.version)

        self.localConfPath = '%s/%s' % (CONF_PATH, self.module)
        self.send_pack = '%s/send.pack' %self.localConfPath

        self.path = PATH_DIC[self.module]
        self.productPath = PRODUCT_PATH_DIC[self.module]
        self.confToModifyDic = CONF_DICT[self.modulename]

        self.linkbase_hdfs = '%s/%s' % (lb, self.modulename)

        self.temp_dir = '%s/temp' % (self.wksp)
        self.logdir = '%s' % LOG_PATH
        self.data_dir = '%s/data' % (self.wksp)
        self.env_log_dir = '%s/env/%s' % (self.logdir, self.modulename)
        self.test_log_dir = '%s/test/%s' % (self.logdir, self.modulename)
        self.result_dir = '%s/%s' %(RESULT_PATH, self.module)

        self.per_log_dir = '%s/per_log' %(self.result_dir)
        self.diff_result_dir = '%s/diff_result' %(self.result_dir)

        mkdir_if_not_exists(self.temp_dir)
        #mkdir_if_not_exists(self.env_log_dir)
        mkdir_if_not_exists(self.per_log_dir)
        mkdir_if_not_exists(self.data_dir)
        #mkdir_if_not_exists(self.result_dir)
        
        self.logger = self.get_logger(self.modulename)


    def deploy(self, clean_env=True, redeploy=True, per_small_lb=True):
        # if not judge_send_pack(self.send_pack):
        #     self.logger.info('send_pack is not exits!')
        #     return 

        if redeploy:
            self.clean_env()
            self.deploy_modules()
            self.config_module_conf(per_small_lb)
        else:
            self.cleanData()

        # if clean_env:
        #     self.clean_env()

    def cleanData(self):
        pass

    def clean_env(self):
        # clean env and create module dir
        clean_env_cmd = 'rm -rf %s; mkdir -p %s;' % (self.wksp, self.wksp)
        self.logger.info(clean_env_cmd)
        subprocess.call(clean_env_cmd, shell = True)
        mkdir_if_not_exists(self.mod_home)
        mkdir_if_not_exists('%s/log' % self.mod_home)
        mkdir_if_not_exists('%s/status' % self.mod_home)
        mkdir_if_not_exists('%s/GetData' % self.mod_home)


    def config_module_conf(self, per_small_lb = True):
        raise NotImplementedError('config_module_conf should call with subclass')

    def get_logger(self, cid):

        subprocess.call('mkdir -p %s' % (self.env_log_dir), shell=True)
        logfilename = '%s/env.log' % (self.env_log_dir)

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d : %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filemode='w')

        logger = logging.getLogger(cid + '-testenv')

        #file_hander = logging.FileHandler('%s/nosetest.log' %(self.env.wksp))
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
