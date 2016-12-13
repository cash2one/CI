#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from TestMethod import *


class TimefilterTest(TestMethod):
    # saverng 模块的功能测试diff实现，后续可添加其他测试diff功能，例如覆盖率

    def __init__(self, testtype, env, sender, diffenable):
        super(TimefilterTest, self).__init__(testtype, env, sender, diffenable)

    def startFuncTest(self):
        # start trap.sh (kill trap first)
        kill_trap_cmd = 'killall -9 trapec.pl'
        self.logger.info(kill_trap_cmd)
        subprocess.call(kill_trap_cmd, shell=True)
        # send pack
        self.sendPack(self.env.send_pack)

        # start trap.sh (kill trap first)
        trap_saver_cmd = 'rm %s;sh %s/trap_tf.sh %s 1 %s/saver_new saver; mv %s/saver_new_ok %s; comawk "{print _}" %s > %s_formal' % (
            self.env.saver_pack_result, self.env.mod_bin, self.env.dataPath, self.env.getDataPath, self.env.getDataPath, self.env.saver_pack_result, self.env.saver_pack_result, self.env.saver_pack_result)
        self.logger.info(trap_saver_cmd)
        subprocess.call(trap_saver_cmd, shell=True)
        trap_linkcache_cmd = 'rm %s;sh %s/trap_tf.sh %s 1 %s/linkcache_new linkcache; mv %s/linkcache_new_ok %s; comawk "{print _}" %s > %s_formal' % (
            self.env.linkcache_pack_result, self.env.mod_bin, self.env.dataPath, self.env.getDataPath, self.env.getDataPath, self.env.linkcache_pack_result, self.env.linkcache_pack_result, self.env.linkcache_pack_result)
        self.logger.info(trap_linkcache_cmd)
        subprocess.call(trap_linkcache_cmd, shell=True)

        # diff
        if self.diffenable:
            saver_online_pack = '%s/saver_result_pack_online' % (
                self.env.result_dir)
            saver_test_pack = '%s/saver_result_pack_test' % (
                self.env.result_dir)
            linkcache_online_pack = '%s/linkcache_result_pack_online' % (
                self.env.result_dir)
            linkcache_test_pack = '%s/linkcache_result_pack_test' % (
                self.env.result_dir)

            if not judge_file_exits(saver_online_pack):
                self.logger.info('error: ' + 'online pack result not exits!')
                return False

            if not judge_file_exits(saver_test_pack):
                self.logger.info(
                    'error: ' + 'test_pack_result' + ' not exits!')
                return False

            diffsaverPath = '%s/diffsaver' % self.env.result_dir
            difflinkcachePath = '%s/difflinkcache' % self.env.result_dir
            mkdir_if_not_exists(diffsaverPath)
            mkdir_if_not_exists(difflinkcachePath)
            diff_cmd = 'rm -rf %s/*; rm -rf %s/*; cd %s ; diffpacket ../saver_result_pack_online ../saver_result_pack_test > %s/diffsaver; cd %s ; diffpacket ../linkcache_result_pack_online ../linkcache_result_pack_test > %s/difflinkcache' % (
                diffsaverPath, difflinkcachePath, diffsaverPath, diffsaverPath, difflinkcachePath, difflinkcachePath)
            self.logger.info(diff_cmd)
            subprocess.call(diff_cmd, shell=True)

        # sendmail
            # with open(diffsaverPath + '/summary','rb') as f:
            # send_mail_cmd = 'cd %s; sh makediff.sh' %self.env.result_dir
            # self.logger.info(send_mail_cmd)
            # subprocess.call(diff_cmd, shell = True)
            saver_online_formal_pack = saver_online_pack + '_formal'
            saver_test_formal_pack = saver_test_pack + '_formal'
            linkcache_online_formal_pack = linkcache_online_pack + '_formal'
            linkcache_test_formal_pack = linkcache_test_pack + '_formal'

    #		url_num_saver_online = len(open(saver_online_formal_pack).readlines())
    #		url_num_saver_test = len(open(saver_test_formal_pack).readlines())
    #		url_num_linkcache_online = len(open(linkcache_online_formal_pack).readlines())
    #		url_num_linkcache_test = len(open(linkcache_test_formal_pack).readlines())

            url_num_saver_online = statTargetURL(saver_online_formal_pack)
            url_num_saver_test = statTargetURL(saver_test_formal_pack)
            url_num_linkcache_online = statTargetURL(
                linkcache_online_formal_pack)
            url_num_linkcache_test = statTargetURL(linkcache_test_formal_pack)

            saver_diff_summary = diffsaverPath + '/diffpacket_result/summary'
            linkcache_diff_summary = difflinkcachePath + \
                '/diffpacket_result/summary'
            saver_detail = 'ftp://' + HOST_NAME + saver_diff_summary
            linkcache_detail = 'ftp://' + HOST_NAME + linkcache_diff_summary
            saver_summary = ''
            s_diff = str(0)
            f = open(saver_diff_summary, 'rb')
            for line in f:
                if "DIFF_ITEMS" in line:
                    s_diff = line.split('=')[1].strip()
                saver_summary = saver_summary + line.strip() + '<br/>'
            f.close()
            lc_summary = ''
            lc_diff = str(0)
            f = open(linkcache_diff_summary, 'rb')
            for line in f:
                if "DIFF_ITEMS" in line:
                    lc_diff = line.split('=')[1].strip()
                lc_summary = lc_summary + line.strip() + '<br/>'
            f.close()

            diff_result_html = self.env.result_dir + '/diff_result_html'
            f = open(diff_result_html, 'wb')
            f.write('<table border="1">\n')
            f.write('<caption>\n')
            f.write("timefilter diff结果\n")
            f.write('</caption>\n')
            f.write(
                '<thead><tr><th>TF下游项</th><th>新版url数量</th><th>旧版url数量</th><th>DIFF字段数量</th><th>详情地址</th></thead><tbody>')
            f.write('<tr><td>saver</td><td>' + str(url_num_saver_test) + '</td><td>' + str(url_num_saver_online) + '</td><td>' +
                    s_diff + '</td><td>' + saver_detail + '</td></tr><td>saver_summary:</td><td colspan="4">' + saver_summary + '</td></tr>')
            f.write('<tr><td>linkcache</td><td>' + str(url_num_linkcache_test) + '</td><td>' + str(url_num_linkcache_online) + '</td><td>' +
                    lc_diff + '</td><td>' + linkcache_detail + '</td></tr><td>linkcache_summary:</td><td colspan="4">' + lc_summary + '</td></tr>')
            f.write('</tbody></table>')
            f.close()

            send_mail_cmd = 'cd %s; sh -x sendmail.sh %s Timefilter_Diff_Result' % (
                self.env.result_dir, diff_result_html)
            self.logger.info(send_mail_cmd)
            subprocess.call(send_mail_cmd, shell=True)
