# -*- coding: utf-8 -*-
#from doco.client import Client
from config.key import docomo_key


class ChatBot(object):
    def replay_chat(self, word):
        """
        チャットを返す
        :param word:
        :return:
        """
        c = Client(apikey=docomo_key)
        res = c.send(utt=word, apiname='Dialogue')
        return res['utt']

