#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import subprocess
import datetime
import shlex
from Constants import *
from Utils import *
keyword = list(set(LB_FIELD_NAMES).difference(set(NO_NEED_FIELD)))
online_pack_result = '/home/spider/workspacezr/performTestPlat/result/saverng/online_result_pack' 
test_pack_result = '/home/spider/workspacezr/performTestPlat/result/saverng/test_result_pack' 
keystr = ' '.join(LB_FIELD_NAMES)
print keystr
#strdate = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

#result_pack_dir = '%s/%s' %(self.env.result_dir, strdate)
 #                       mkdir_if_not_exists(result_pack_dir)
#                        copy_result_cmd = 'cp %s %s %s' %(online_pack_result, test_pack_result, result_pack_dir)
 #                       self.logger.info(copy_result_cmd)
  #                      subprocess.call(copy_result_cmd, shell = True)
#			if not judge_file_exits(online_pack_result):
#				self.logger.info('error: ' + online_pack_result + ' not exits!')
#				return False
#
#			if not judge_file_exits(test_pack_result):
#				self.logger.info('error: ' + test_pack_result + ' not exits!')
#				return False
print len(keyword)
print keyword[117]
print len(LB_FIELD_NAMES)
print LB_FIELD_NAMES[117]
wordsum = len(keyword) - 1
f1 = open(online_pack_result,'rb')
f2 = open(test_pack_result,'rb')
lineon = {}
lineoff = {}
line_num = 0
for line in f1:
    #list_tmp = shlex.split(line)
    list_tmp = line.split()
    if len(list_tmp) != len(keyword):
        print 'WARINING:  value len is ' + str(len(list_tmp)) + 'wordsum is ' + str(len(keyword)) 
        print 'wrong line is %d' %line_num
        list_tmp = newSplit(line)
    if len(list_tmp) != len(keyword):
        print 'wrong line is %d' %line_num
        list_tmp = shlex.split(line)

    key,value = [list_tmp[0],list_tmp[1:]]
    if len(value) != wordsum:
        print 'saverng diff failed, wordsum is wrong, please check LB_FIELD_NAMES in Constants.py, value len is ' + str(len(value)) + 'wordsum is ' + str(wordsum) 
        print 'wrong line is %d' %line_num
    lineon[key] = value
    line_num += 1;
line_num = 0
for line in f2:
   # list_tmp = shlex.split(line)
    list_tmp = line.split()
    if len(list_tmp) != len(keyword):
        print 'WARINING:  value len is ' + str(len(list_tmp)) + 'wordsum is ' + str(len(keyword)) 
        print 'wrong line is %d' %line_num
        list_tmp = newSplit(line)
    if len(list_tmp) != len(keyword):
        print 'wrong line is %d' %line_num
        list_tmp = shlex.split(line)


    key,value = [list_tmp[0],list_tmp[1:]]
    if len(value) != wordsum:
        print 'saverng diff failed, wordsum is wrong, please check LB_FIELD_NAMES in Constants.py, value len is ' + str(len(value)) + 'wordsum is ' + str(wordsum) 
    lineoff[key] = value
    line_num += 1
LineOnLink = len(lineon)
LineOffLink = len(lineoff)
c = list(set(lineon.keys()).intersection(set(lineoff.keys())))
repeatLink = len(c)
f1.close()
f2.close()
res_list = [0]*wordsum
for key in c:
    for k in range(0, len(lineon[key])):
        if(lineon[key][k] != lineoff[key][k]):
            res_list[k] += 1
mail_dic = {}
word_list = LB_FIELD_NAMES[1:]
stat_word_result = '/home/spider/workspacezr/performTestPlat/result/saverng/stat_word_result.txt' 
f3 = open(stat_word_result,'wb')
for i in range(0, len(res_list)):
    if res_list[i] > 0:
        mail_dic[word_list[i]] = float('%.5f' %(float(res_list[i] * 100 / LineOnLink)))
        print str(word_list[i]) + ':' + str(res_list[i])
        print mail_dic[word_list[i]]
    f3.write(word_list[i] + ':')
    f3.write(str(res_list[i]) + '\n')
f3.close()

def generate_tr( aname, ascore):
    if ascore > 1:  #如果diff率大于1%，表格输出时标红
        return '<tr><td>%s</td><td style="color:red">%s %%</td></tr>'% (aname,ascore)
    else:
        return '<tr><td>%s</td><td>%s %%</td></tr>' %(aname,ascore)

tds = [generate_tr(k,v) for (k,v) in mail_dic.items()]
detail_ftp = 'ftp://HOST_NAME/home/spider/workspacezr/performTestPlat/result/saverng'
res_html = '/home/spider/workspacezr/performTestPlat/result/saverng/stat_word_res.html'
f4 = open(res_html,'w')
f4.write('<table border="1">\n')
f4.write('<caption>\n')
f4.write("saver-ng diff结果\n")
f4.write('</caption>\n')
f4.write('<thead><tr><th>项目名称</th><th>线上版本url入库数量</th><th>测试版本url入库数量</th><th>相同url数量</th></thead>')
f4.write('<tbody>\n')
f4.write('<tr align="center"><td>"saver-ng diff模块"</td><td>'+str(LineOnLink)+'</td><td>'+str(LineOffLink)+'</td><td>'+str(repeatLink)+'</td></tr><tr align="center"><td>详细地址:</td><td colspan="3">'+detail_ftp+'</td></tr>')
f4.write('</tbody>\n')
f4.write('</table>\n')

f4.write('<table border="1">\n')
f4.write('<caption>\n')
f4.write("各字段diff数\n")
f4.write('</caption>\n')
f4.write('<tr><th>字段</th><th>diff百分比</th><tr>\n')
f4.write('\n'.join(tds))
f4.write('</table>\n')
f4.close()

send_mail_cmd = 'cd /home/spider/workspacezr/performTestPlat/result/saverng ; sh -x sendmail.sh %s diff_saverng' %( res_html)
subprocess.call(send_mail_cmd, shell = True)


