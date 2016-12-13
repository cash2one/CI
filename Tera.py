#!/bin/env  python
# -*- coding: utf-8 -*- 

import subprocess

'''
A simple wrapper class per teracli
'''
class Tera(object):
    def __init__(self, cli_home):
        self.cli_home = cli_home

    def table_exists(self, table_name):
        tera_cmd = "cd %s && ./teracli show %s" %(self.cli_home, table_name)
        ret = subprocess.call(tera_cmd, shell=True)
        if ret == 0:
            return True
        else:
            return False

    def drop_table(self, table_name):
        tera_cmd = 'cd %s && ./teracli disable %s' %(self.cli_home, table_name)
        subprocess.call(tera_cmd, shell=True)
        tera_cmd = 'cd %s && ./teracli drop %s' %(self.cli_home, table_name)
        ret = subprocess.call(tera_cmd, shell=True)
        if ret == 0:
            return True
        else:
            return False

    def recreate_table(self, table_name, create_table_cmd):
        if self.table_exists(table_name):
            self.drop_table(table_name)

        if self.table_exists(table_name):
            self.drop_table(table_name)
            
        if self.table_exists(table_name):
            self.drop_table(table_name)

        return self.create_table(create_table_cmd)


    def create_table(self, create_table_cmd):
        tera_cmd = "cd %s && ./teracli %s" %(self.cli_home, create_table_cmd)
        ret = subprocess.call(tera_cmd, shell=True)
        sleep_cmd = "sleep 5"
        i = 0
        if ret == 0:
            return True
        while(i < 5):
            subprocess.call(sleep_cmd, shell=True)
            ret = subprocess.call(tera_cmd, shell=True)
            if ret == 0:
                return True
            else:
                i = i + 1
        return False

        # if ret == 0:
        #     return True
        # else:
        #     for i in range(0,5):
        #         subprocess.call(sleep_cmd, shell=True)
        #         subprocess.call(tera_cmd, shell=True)
        #     return False
