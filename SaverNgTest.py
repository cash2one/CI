#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import subprocess
from Utils import *
from TestMethod import *


class SaverNgTest(TestMethod):
    # saverng 模块的功能测试diff实现，后续可添加其他测试diff功能，例如覆盖率

    def __init__(self, testtype, env, sender, diffenable):
        super(SaverNgTest, self).__init__(testtype, env, sender, diffenable)

    def generate_tr(self, aname, ascore):
        if ascore > 1:  # 如果diff率大于1%，表格输出时标红
            return '<tr><td>%s</td><td style="color:red">%s %%</td></tr>' % (aname, ascore)
        else:
            return '<tr><td>%s</td><td>%s %%</td></tr>' % (aname, ascore)

    def startFuncTest(self):
            # merge save.pack and send.pack send pack
        with open(self.env.send_pack, 'a') as pack:
            pack.write('\n' + str(open(self.env.save_pack, 'r').read()))
        # send pack
        self.sendPack(self.env.send_pack)

        keyword = LB_FIELD_NAMES
        for ele in NO_NEED_FIELD:
            keyword = keyword.remove(ele)
    #	keyword = list(set(LB_FIELD_NAMES).difference(set(NO_NEED_FIELD)))
        # get pack from linkcache
        str_field = ' '.join(keyword)
        get_pack_cmd = 'rm %s;cd %s && ./dlb_client -s %s -o "%s" -b \'%s\' -e \'%s\' >%s 2>%s/select_url.log' % (
            self.env.pack_result, self.env.mod_bin, self.env.l1linkbase, FIELDS, BEGIN_URL, END_URL, self.env.pack_result, self.env.test_log_dir)
        self.logger.info(get_pack_cmd)
        subprocess.call(get_pack_cmd, shell=True)

        if self.diffenable == True:
            online_pack_result = '%s/online_result_pack' % self.env.result_dir
            test_pack_result = '%s/test_result_pack' % self.env.result_dir

            strdate = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

            result_pack_dir = '%s/%s' % (self.env.result_dir, strdate)
            mkdir_if_not_exists(result_pack_dir)
            copy_result_cmd = 'cp %s %s %s' % (
                online_pack_result, test_pack_result, result_pack_dir)
            self.logger.info(copy_result_cmd)
            subprocess.call(copy_result_cmd, shell=True)
            if not judge_file_exits(online_pack_result):
                self.logger.info(
                    'error: ' + online_pack_result + ' not exits!')
                return False

            if not judge_file_exits(test_pack_result):
                self.logger.info('error: ' + test_pack_result + ' not exits!')
                return False

            wordsum = len(keyword) - 1
            f1 = open(online_pack_result, 'rb')
            f2 = open(test_pack_result, 'rb')
            lineon = {}
            lineoff = {}
            for line in f1:
                line_list = line.split()
                if len(line_list) != len(keyword):
                    line_list = newSplit(line)
                if len(line_list) != len(keyword):
                    line_list = shlex.split(line)

                key, value = [line_list[0], line_list[1:]]
                if len(value) != wordsum:
                    self.logger.info('saverng diff failed, wordsum is wrong, please check LB_FIELD_NAMES in Constants.py, value len is ' + str(
                        len(value)) + 'wordsum is ' + str(wordsum))
                   # return
                lineon[key] = value
            for line in f2:
                line_list = line.split()
                if len(line_list) != len(keyword):
                    line_list = newSplit(line)
                if len(line_list) != len(keyword):
                    line_list = shlex.split(line)

                key, value = [line_list[0], line_list[1:]]
                if len(value) != wordsum:
                    self.logger.info('saverng diff failed, wordsum is wrong, please check LB_FIELD_NAMES in Constants.py, value len is ' + str(
                        len(value)) + 'wordsum is ' + str(wordsum))
                    # return
                lineoff[key] = value

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
            word_list = keyword[1:]
            stat_word_result = '%s/stat_word_result.txt' % result_pack_dir
            f3 = open(stat_word_result, 'wb')
            for i in range(0, len(res_list)):
                if res_list[i] > 0:
                    mail_dic[word_list[i]] = float(
                        '%.3f' % (float(res_list[i] * 100 / LineOnLink)))
                    f3.write(word_list[i] + ':')
                    f3.write(str(res_list[i]) + '\n')
            f3.close()

            tds = [self.generate_tr(k, v) for (k, v) in mail_dic.items()]
            detail_ftp = 'ftp://%s%s' % (HOST_NAME, result_pack_dir)

            res_html = '%s/stat_word_res.html' % self.env.result_dir
            f4 = open(res_html, 'w')
            f4.write('<table border="1">\n')
            f4.write('<caption>\n')
            f4.write("saver-ng diff结果\n")
            f4.write('</caption>\n')
            f4.write(
                '<thead><tr><th>项目名称</th><th>线上版本url入库数量</th><th>测试版本url入库数量</th><th>相同url数量</th></thead>')
            f4.write('<tbody>\n')
            f4.write('<tr align="center"><td>"saver-ng diff模块"</td><td>'+str(LineOnLink)+'</td><td>'+str(LineOffLink) +
                     '</td><td>'+str(repeatLink)+'</td></tr><tr align="center"><td>详细地址:</td><td colspan="3">'+detail_ftp+'</td></tr>')
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

            send_mail_cmd = 'cd %s ; sh -x sendmail.sh %s SaverNg_Diff_Result' % (
                self.env.result_dir, res_html)
            self.logger.info(send_mail_cmd)
            subprocess.call(send_mail_cmd, shell=True)
