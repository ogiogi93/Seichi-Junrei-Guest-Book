# -*- coding: utf-8 -*-
import requests
import json
from config import key


class FindSimilarFace(object):
    def __init__(self):
        self.header_json = {
            'content-type': 'application/json',
            'ocp-apim-subscription-key': key.microsoft_key,
        }
        self.header_octet = {
            'content-type': 'application/json',
            'ocp-apim-subscription-key': key.microsoft_key,
        }

    def get_similar_face(self, face_id, face_list_id):
        """
        類似した顔画像を返す
        :param face_id:
        :param face_list_id:
        :return:
        """
        url = "https://westus.api.cognitive.microsoft.com/face/v1.0/findsimilars"
        body = json.dumps({
            "faceId": face_id,
            "faceListId": face_list_id,
            "maxNumOfCandidatesReturned": 10,
            "mode": "matchFace"
        })
        return requests.post(url, data=body, headers=self.header_json)
