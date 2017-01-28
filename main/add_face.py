# -*- coding: utf-8 -*-
import requests
from config import key

class AddFace(object):
    def __init__(self):
        self.header = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': key.microsoft_key,
        }

    def add_face(self, url, param, file_path):
        """
        顔写真をFace APIに登録する
        :param url:
        :param file_path:
        :return:
        """
        return requests.post(url, params=param, data=open(file_path, 'rb'), headers=self.header).json()
