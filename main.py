from PerformTestPlat import *
import time
from Utils import *

######################################################
#version: 1.0
#author:  zhairui
#detail: saverng and timefilter ,perform or diff, alldone
#To do: check sendpack
#       add ec dc lc
#       maybe coverTest 
######################################################

## moduletype(0:saverng, 1: timefilter)
## version(0:online,1:test)
## testtype(0:no test,1:perform,2:diff,3:perform+diff)
## commonly, user need to set the follow two parameter, modType and testType
## specially, user can run only one test or online verion by set parameter version
modType = 1
testType = 3

if testType == 2 or testType == 3:
    diffEn = True
else: 
    diffEn = False

test = PerformTestPlat(moduletype = modType, version = 0, testtype = testType, redeploy = True)
test.restart_module()

#print "now you can do some operation ,eg change tera .."
#print " confirm your operation has done and Press any key to continue "
#a = raw_input()

test2 = PerformTestPlat(moduletype = modType, version = 1, testtype = testType, diffenable = diffEn, redeploy = True)
test2.restart_module()

if testType == 1 or testType == 3:
    diff_perform(test.modTest.task_id, test2.modTest.task_id, test2.modEnv.result_dir,test2.modEnv.module)

