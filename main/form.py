# -*- coding: utf-8 -*-
from django import forms


class UploadFaceImage(forms.Form):
    path = forms.FileField(label='アイコンを変更注意： JPG、PNGのみ対応しています',
                           required=False)

