#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import logging
import time
from datetime import datetime
import re
import string
from Constants import *
import os
import json
import shlex

import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib

def newSplit(value):
    lex = shlex.shlex(value)
    lex.quotes = '"'
    lex.whitespace_split = True
    lex.commenters = ''
    return list(lex)

def statTargetURL(filePath):
    num = 0;
    for line in open(filePath):
        if "target_url" in line:
            num += 1
    return num
def sendEmail(authInfo, fromAdd, toAdd, subject, plainText, htmlText):
    strFrom = fromAdd
    strTo = ', '.join(toAdd)
    server = authInfo.get('server')
    user = authInfo.get('user')
    passwd = authInfo.get('password')
    if not (server and user and passwd):
        print 'incomplete login info, exit now'
        return
    # 设定root信息
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    # 设定纯文本信息
    msgText = MIMEText(plainText, 'plain', 'utf-8')
    msgAlternative.attach(msgText)
    # 设定HTML信息
    msgText = MIMEText(htmlText, 'html', 'utf-8')
    msgAlternative.attach(msgText)
   # 设定内置图片信息
    #fp = open('test.jpg', 'rb')
    #msgImage = MIMEImage(fp.read())
    #fp.close()
    #msgImage.add_header('Content-ID', '<image1>')
    #msgRoot.attach(msgImage)
   ## 发送邮件
    smtp = smtplib.SMTP()
   # 设定调试级别，依情况而定
   # smtp.set_debuglevel(1)
    smtp.connect(server)
    smtp.login(user, passwd)
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()
    return


'''
根据配置文件名和要修改的配置字典对配置文件进行修改
参数：
    confname    修改的配置文件路径
    confdict    修改的配置字典
'''
def mod_mormal_file(file_name, mod_dict):
    logging.info('modifying conf: %s' %file_name)
    line2write = []
    f = open(filename)
    for line in f:
        for key in mod_dict.keys():
            if key in line:
                line.replace(key,mod_dict[key])
        line2write.append(line + '\n')
    f.close()
    fw = open(file_name, 'wb')
    fw.writelines(alllines)
    fw.close()




def mod_conf(conf_name, mod_dict, separator="="):
    logging.info('modifying conf: %s' %conf_name)     
    line2write = []
    file_h = file(conf_name, 'r')
    conf_keys = [] #all key in conffile
    alllines = file_h.readlines()
    for line_no in range(0,len(alllines)):
        line =  alllines[line_no]
        line = line.strip()
        line_list = line.split(separator)
        if len(line_list) <= 0:
            continue
        key = line_list[0].strip()
        conf_keys.append(key)
        if key in mod_dict.keys(): #MOD
            if separator == ':':
                line = key + ' ' + separator + ' ' + mod_dict[key]
            else:
                line = key + separator + mod_dict[key]
            logging.info('set %s to [%s]' %(key, mod_dict[key]))
            alllines[line_no] = line + '\n'
        
    for key in mod_dict.keys():
        if key == '__separator__':
            continue
            
        if key not in conf_keys: #ADD
            if separator == ':':
                line = key + ' ' + separator + ' ' + mod_dict[key]
            else:
                line = key + separator + mod_dict[key]
            logging.info('add %s to [%s]' %(key, mod_dict[key]))
                
            alllines.append(line + '\n')




    file_h.close()
    file_h = file(conf_name, 'w') 
    file_h.writelines(alllines)
    file_h.close()

'''
功能：修改脚本类型配置文件，修改关键字或者变量的值
参数：
    shell_file     脚本文件路径
    key         修改的关键字/变量名称
    num         关键字/变量名在文件中的位置（第几个）
    value       修改为的值
    separator   关键字/变量与值之间的分隔符
//TODO:
    也许修改一整行更好

'''

def diff_perform(taskid1,taskid2,path,module):
    diff_perform_log = '%s/diff_per_result' %path
    per_result_online = '%s/per_result_online' %path
    per_result_test = '%s/per_result_test' %path
    diff_per_cmd = 'curl "http://cp01-cq01-testing-ps7109.epc.baidu.com:8911/?r=performance/diffAPI&task1_id=%s&task2_id=%s" >%s' %(taskid1,taskid2,diff_perform_log)
    subprocess.call(diff_per_cmd, shell=True)
    f = open(diff_perform_log, 'r')
    s = json.load(f)
    f.close()
    task1_image_url = 'http://cp01-cq01-testing-ps7109.epc.baidu.com:8911/?r=performance/detail&taskid=%s' %taskid1
    task2_image_url = 'http://cp01-cq01-testing-ps7109.epc.baidu.com:8911/?r=performance/detail&taskid=%s' %taskid2
   ## send mail 
    htmlText = '<table border="1" width=800 height=100>\n'
    htmlText += '<caption>'
    tableBody = '<tbody>\n'
    online_row = '<tr align="center">\n'
    test_row = '<tr align="center">\n'
    diff_row = '<tr align="center">\n'
    if s['result'] == 2:
        key_list = ['v_min','v_max','v_avg','r_min','r_max','r_avg','c_min','c_max','c_avg']
        htmlText = htmlText + '<b><big>' + module.title() + ' Perform Diff Result\n' + '</big></b></caption>'
        htmlText += '<thead><tr>'
        htmlText += '<th>per_ind:</th>'
        online_row += '<td>per_old_version:</td>'
        test_row += '<td>per_new_version:</td>'
        diff_row += '<td>per_diff:</td>'
        for key in key_list:
            htmlText = htmlText + '<th>' + key + '</th>'           
            online_row = online_row + '<td>' + str(s[key][0]) + '</td>'
            test_row = test_row + '<td>' + str(s[key][1]) + '</td>'
            diff_row = diff_row + '<td>' + str(s[key][2]) + '</td>'
        htmlText += '</thead>'
        online_row += '</tr>'
        test_row += '</tr>'
        diff_row += '</tr>'
        tableBody = tableBody + online_row + test_row + diff_row + '<tr align="center"><td>old version detail:</td><td colspan="9">' + task1_image_url + '</td></tr>' 
        tableBody = tableBody + '<tr align="center"><td>new version detail:</td><td colspan="9">' + task2_image_url + '</td></tr>' 
        tableBody += '</tbody>\n'
        htmlText = htmlText + tableBody + '</table>'
    html_log = path + '/html_log'
    f2 = open(html_log,'w')
    f2.write(htmlText)
    f2.close()
    send_mail_cmd = 'cd %s ; sh -x sendmail.sh %s %s_Perform_Diff_Result' %(path, html_log, module.title())
    subprocess.call(send_mail_cmd, shell=True)
    
  #  sendEmail(authInfo,  fromAdd, toAdd, subject, plainText, htmlText)


def mod_shell_conf(shell_file, key, num, value, separator=" "):
    #usually source
    line2write = []
    shellfile = file(shell_file, 'r')
    key_count = 0
    alllines = shellfile.readlines()
    for line_no in range(0,len(alllines)):
        line =  alllines[line_no]
        line = line.strip()
        line_list = line.split(separator)
        if len(line_list) <= 0:
            continue
        if line_list[0] == key:
            key_count += 1
            if num == -1 or key_count == num:
                mod_line = line_list[0] + separator + str(value)
                alllines[line_no] = mod_line + '\n'
                logging.info('change %s to [%s]' %(line, mod_line))
    shellfile.close()
    shellfile = file(shell_file, 'w') 
    shellfile.writelines(alllines)
    shellfile.close()

def url_md5(url_string):
    import hashlib
    m = hashlib.md5()
    m.update(url_string)
    return m.hexdigest()

def get_available_port():
    try_list = [p for p in range(1314,2000)]
    for port in try_list:
        #check_cmd = 'netstat -a | grep %s' %port
        check_cmd = '/usr/sbin/lsof +c 0 -nPli TCP:%s' %port
        ret = subprocess.call(check_cmd, shell =True)
        if ret == 1:
            return port

def hadoop_exists(patch_path):
    check_exist_cmd = 'hadoop fs -test -e %s' %(patch_path)
    ret = subprocess.call(check_exist_cmd, shell = True)
    if ret != 0 :
        logging.error('patch doesnot exist:%s' % patch_path)
        return False
    else:
        return True

def is_force_patch(patch):
    '''determinate whether a patch is a force patch'''
    #return True
    for m_url, fields in patch.items():
        if len(fields.keys()) == 0:
            return False

    return True


def get_baidu_days(real = False, ret_type='int'):
    now = datetime.fromtimestamp(gettime(real))
    baidu_start_day = datetime(2000, 12, 31)
    baidu_days = (now - baidu_start_day).days
    return baidu_days


def gettime(real = False, ret_type='int'):
    
    nows = str(time.time())
    idx = nows.find('.')
    nowsec = nows[0:idx]
    if not real:
        nowsec = TIME_NOW_FOR_TEST

    if ret_type == 'int':
        return string.atoi(nowsec)
    else:
        return nowsec

def get_current_time():
    return str(time.time())

def get_seconds_before_now(secs, ret_type = 'str', real = False):
    btime = gettime(real) - secs
    if ret_type == 'int':
        return btime
    else:
        return str(btime)

def get_days_before_now(days, ret_type = 'str', real = False):
    btime = gettime(real) - 3600 * 24 * days
    if ret_type == 'int':
        return btime
    else:
        return str(btime)

def get_month_day_for_now(real = False):
    btime = gettime(real)
    dt = datetime.fromtimestamp(btime)
    return dt.day

def get_week_day_for_now(real = False):
    btime = gettime(real)
    dt = datetime.fromtimestamp(btime)
    return dt.weekday() + 1

def highlight(ret):
    if ret.upper() == "FAIL":
        return "\x1b[5m\x1b[1m\x1b[7m\x1b[31m[FAILED]\x1b[0m"
    elif ret.upper() == "PASS":
        return "\x1b[2m\x1b[1m\x1b[7m\x1b[32m[PASSED]\x1b[0m"
    elif ret.upper() == "ERROR":
        return "\x1b[2m\x1b[1m\x1b[7m\x1b[33m[ERROR]\x1b[0m"

def delete_nomeaning_zeros(returndata = ''):
    #iterate backward, delete right padding zeroes
    ret = returndata
    if(ret.find('.') == -1):#not a float number
        return ret

    for idx in reversed(xrange(len(returndata))):
        
        if returndata[idx] == '0':
            continue
        elif returndata[idx] == '.':
            ret = returndata[0 : idx]
            break

        else:
            ret = returndata[0: idx + 1]
            break

    return ret

def is_url_a_prehold(m_url):
    return re.match(PREHOLD_PATTERN, m_url)


def mkdir_if_not_exists(path):
    '''
    return 0 if make dir successfully
    '''
    ret = 0
    if not os.path.exists(path):
        ret = subprocess.call('mkdir -p %s' %path, shell = True)
    
    return ret

def judge_file_exits(path):
    return os.path.exists(path)

def force_mkdir(path):
    '''
    first remove the dir, then create it
    return 
         0  if passed
        -1 remove dir failed
        -2 mkdir failed
    '''
    
    ret = subprocess.call('rm -rf %s' %path, shell = True)
    if ret != 0 : return -1

    ret = subprocess.call('mkdir -p %s' %path, shell = True)
    if ret != 0 : return -2

    return ret

def get_latest_linkbase_path(conf):
    cmd = 'hadoop fs -cat %s | grep lastest_linkbase_path | awk -F= \'{print $2}\'' %conf
    logging.info(cmd)
    latest_lb_path = subprocess.check_output(cmd, shell = True).strip()
    return latest_lb_path

def get_crawlhist_not_use():
    '''crawlhist = crawl_seconds(first 28bit) + crawl_status(last 4bit)'''
    return str(int(bin(int(TIME_NOW_FOR_TEST))[:-4] + '0000', 2))

def get_crawlhist_not_not_use():
    '''crawlhist = crawl_seconds(first 28bit) + crawl_status(last 4bit)'''
    return str(int(bin(int(TIME_NOW_FOR_TEST))[:-4] + '1001', 2))

def get_crawlhist_ok():
    '''crawlhist = crawl_seconds(first 28bit) + crawl_status(last 4bit)'''
    return str(int(bin(int(TIME_NOW_FOR_TEST))[:-4] + '0001', 2))
