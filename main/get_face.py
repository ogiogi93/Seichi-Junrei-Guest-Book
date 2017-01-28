# -*- coding: utf-8 -*-
import pandas as pd
from django.db import connection


class GetFaceList(object):

    def dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]

    def get_face_list(self, db_table):
        """
        登録されている顔画像のpath情報を取得する
        :return:
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM "+db_table+"")

        return pd.DataFrame(self.dictfetchall(cursor))

