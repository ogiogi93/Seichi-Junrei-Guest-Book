# -*- coding: utf-8 -*-
import httplib, urllib, base64
import json
import requests
import urllib
import sys
import cv2
import numpy as np
import pandas as pd
import operator
import time

from config import key


class DetectEmotion(object):
    def __init__(self):
        self.url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
        self.key = key.microsoft_emotion_key
        self.maxNumRetries = 10

    def processRequest(self, json, data, headers, params):
        """
        https://github.com/Microsoft/Cognitive-Emotion-Python/blob/master/Jupyter%20Notebook/Emotion%20Analysis%20Example.ipynb
        Helper function to process the request to Project Oxford

        Parameters:
        json: Used when processing images from its URL. See API Documentation
        data: Used when processing image read from disk. See API Documentation
        headers: Used to pass the key information and the data type request
        """
        retries = 0
        result = None
        while True:
            response = requests.request('post', self.url, json=json, data=data, headers=headers, params=params)
            if response.status_code == 429:
                print("Message: %s" % (response.json()['error']['message']))
                if retries <= self.maxNumRetries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed after retrying!')
                    break
            elif response.status_code == 200 or response.status_code == 201:
                if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                    result = None
                elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                    if 'application/json' in response.headers['content-type'].lower():
                        result = response.json() if response.content else None
                    elif 'image' in response.headers['content-type'].lower():
                        result = response.content
            else:
                print("Error code: %d" % (response.status_code))
                print("Message: %s" % (response.json()['error']['message']))

            break
        return result

    def detect_emotion(self, file_path):
        """
        画像から感情を推定する
        :param file_path:
        :return:
        """
        with open(file_path, 'rb') as f:
            data = f.read()

        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = self.key
        headers['Content-Type'] = 'application/octet-stream'
        json = None
        params = None

        return self.processRequest(json, data, headers, params)[0]['scores']



