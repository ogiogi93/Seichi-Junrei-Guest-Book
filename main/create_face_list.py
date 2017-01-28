# -*- coding: utf-8 -*-
import requests
import json
import urllib
from config import key


class CreateFaceList(object):
    def __init__(self):
        self.header_json = {
            'content-type': 'application/json',
            'ocp-apim-subscription-key': key.microsoft_key,
        }
        self.header_octet = {
            'content-type': 'application/octet-stream',
            'ocp-apim-subscription-key': key.microsoft_key,
        }

    def create_face_list(self, face_list_id):
        """
        類似度計算用の顔画像リストを生成する
        :param face_list_id:
        :return:
        """
        url = ("https://westus.api.cognitive.microsoft.com/face/v1.0/facelists/%s" % face_list_id)
        body = json.dumps({
            "name": "pwc_hackton_face_list",
            "userData": "Face List for pwc hackthon",
        })
        return requests.put(url, data=body, headers=self.header_json).json()

    def delete_face_list(self, face_list_id):
        """
        類似度計算用の顔画像リストを除去する
        :param face_list_id:
        :return:
        """
        url = ("https://westus.api.cognitive.microsoft.com/face/v1.0/facelists/%s" % face_list_id)
        return requests.delete(url, headers=self.header_json).json()

    def add_user_face(self, file_path):
        """
        顔写真を追加する
        :param file_path:
        :return:
        """
        param = urllib.urlencode({
            # Request parameters
            'analyzesFaceLandmarks': 'true',
            'analyzesAge': 'true',
            'analyzesGender': 'true',
            'analyzesHeadPose': 'false',
        })
        url = "https://westus.api.cognitive.microsoft.com/face/v1.0/detect"
        r = requests.post(url, params=param, data=open(file_path, 'rb'), headers=self.header_octet).json()
        try:
            print('face detected and added')
            return r[0]['faceId']
        except:
            print("no face detected")
            return 'null'

    def add_picture_to_facelist(self, face_list_id, file_path):
        """
        顔写真を類似度計算用の顔画像リストに追加する
        :param face_list_id:
        :param file_path:
        :return:
        """
        url = ("https://westus.api.cognitive.microsoft.com/face/v1.0/facelists/%s/persistedFaces/" % face_list_id)
        r = requests.post(url, data=open(file_path, 'rb'), headers=self.header_octet).json()
        try:
            print('face detected and added')
            return r['persistedFaceId']
        except:
            print("no face detected")
            return 'null'

    def get_facelist(self, face_list_id):
        """
        類似度計算の顔画像リストに登録されている情報を返す
        :param face_list_id:
        :return:
        """
        url = ("https://westus.api.cognitive.microsoft.com/face/v1.0/facelists/%s" % face_list_id)
        return requests.get(url, headers=self.header_json).json()
