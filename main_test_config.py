from PerformTestPlat import *
import time
from Utils import *
# configure saver_ng.flag
confname = '/home/spider/workspacezr/performTestPlat/data/saverng/online/saver_ng/conf/saver_ng.flag' 

confdict = {
    '--zk_support': 'false',

}
mod_conf(confname, confdict, separator='=')

 
