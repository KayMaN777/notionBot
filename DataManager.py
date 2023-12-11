import os
import shutil
from random import randint

import re
import requests
from bs4 import BeautifulSoup

class User:

    def ValidateDirectory(self):
        path = './data'
        if not os.path.exists(path):
            os.mkdir(path)
        path += '/users'
        if not os.path.exists(path):
            os.mkdir(path)

        path += '/' + str(self.user_id_)
        if not os.path.exists(path):
            os.mkdir(path)
        filename = path + '/info'
        if not os.path.exists(filename):
            f = open(filename, 'w')
            shutil.copyfile('./data/default_info', filename)
            f.close()

    def ReadInfo(self):
        self.ValidateDirectory()
        path = './data/users/' + str(self.user_id_)

        filename = path + '/info'
        f = open(filename, 'r')
        while True:
            st = f.readline()
            if (not st) or (st == '\n'):
                break
            var_name, var_val = st.split()
            self.user_info_[var_name] = var_val
        f.close()

    def WriteInfo(self):
        self.ValidateDirectory()
        path = './data/users/' + str(self.user_id_)

        filename = path + '/info'
        f = open(filename, 'w')
        for key in self.user_info_:
            f.write(key + ' ' + str(self.user_info_[key])+'\n')
        f.close()

    def GetFlagVal(self, flag_name):
        chat_id = self.user_id_
        user1 = User(chat_id)
        user1.ReadInfo()
        return user1.user_info_[flag_name]

    def SetFlagVal(self, flag_name, flag_val):
        chat_id = self.user_id_
        user1 = User(chat_id)
        user1.ReadInfo()
        user1.user_info_[flag_name] = flag_val
        user1.WriteInfo()

    def __init__(self, user_id = 0):
        self.user_id_ = int(user_id)
        self.user_info_ = {}
        self.ValidateDirectory()
