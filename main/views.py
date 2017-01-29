# -*- coding: utf-8 -*-
import os
import pandas as pd
from django.shortcuts import render
from main.models import Face, PersistedFace
from django.conf import settings
from create_face_list import CreateFaceList
from main.get_face import GetFaceList
from main.form import UploadFaceImage
from main.find_similar_face import FindSimilarFace
from main.emotion import DetectEmotion
from main.chat_bot import ChatBot
from django.shortcuts import render_to_response, redirect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADE__FACE_DIR = BASE_DIR + '/static/images/face/'
UPLOADE__IMAGE_DIR = BASE_DIR + '/static/images/picture/'
FACE_LIST_ID = 'pwc_hackthon_face_list'


def top_page(request):
    return render(request, 'main/top.html')


def cate_page(request):
    return render(request, 'main/cate.html')


def setting_page(request):
    return render(request, 'main/settings.html')


def pic_page(request):
    if request.POST:
        chat = request.POST.get('chat')
        replay = ChatBot().replay_chat(word=chat)
        context ={
            'replay': replay
        }
        return render(request, 'main/pic.html', context)
    return render(request, 'main/pic.html')


def all_picture_page(request):
    """
    画像を返す
    :param request:
    :return:
    """
    # face_list = CreateFaceList().get_facelist(face_list_id=FACE_LIST_ID)
    # df_face = pd.DataFrame(face_list['face_id'])
    df_face_path = GetFaceList().get_face_list(db_table='main_persistedface')
    path_list = []
    for path in list(df_face_path['path']):
        path_dict = {}
        path_dict['path'] = path
        path_list.append(path_dict)

    context = {
        'face_list': path_list
    }

    return render(request, 'main/all-pic.html', context)

def move_page(request):
    return render(request, 'main/move.html')


def ubser_assging(request):
    return render(request, 'main/uber-assign.html')


def uper_page(request):
    return render(request, 'main/uper.html')


def sel_pic_page(request):
    """
    プロフィール画像を返す
    :param request:
    :return:
    """
    df_face_path = GetFaceList().get_face_list(db_table='main_face')
    path_list = []
    for path in list(df_face_path['path']):
        path_dict = {}
        path_dict['path'] = path
        path_list.append(path_dict)

    context = {
        'face_list': path_list
    }

    return render(request, 'main/sel-pic.html', context)


def my_pic_page(request):
    """
    類似度計算をして自分の画像を抽出する
    :param request:
    :return:
    """
    if request.GET:
        user_face_path = request.GET['path']
        face_id = Face.objects.get(path=user_face_path).face_id
        r = FindSimilarFace().get_similar_face(face_id=face_id, face_list_id=FACE_LIST_ID).json()
        sim_list = []
        for sim in r:
            temp = sim['persistedFaceId'], sim['confidence']
            sim_list.append(temp)
        # 類似度計算結果を取得
        df_similar_picture = (pd.DataFrame(sim_list, columns=['persisted_id', 'confidence']))
        # 画像を取得
        df_picture_path = GetFaceList().get_face_list(db_table='main_persistedface')
        df_similar_merged = pd.merge(df_similar_picture, df_picture_path, on='persisted_id')

        # 類似度が0.6以上が同一人物だと判断
        df_similar_merged = df_similar_merged[df_similar_merged['confidence'] > 0.6].reset_index()

        similer_list = []
        for index in df_similar_merged.index:
            _dict = {}
            _dict['path'] = df_similar_merged['path'].ix[index]
            _dict['conf'] = df_similar_merged['confidence'].ix[index]
            _dict['anger'] = df_similar_merged['anger'].ix[index]
            _dict['contempt'] = df_similar_merged['contempt'].ix[index]
            _dict['disgust'] = df_similar_merged['disgust'].ix[index]
            _dict['fear'] = df_similar_merged['fear'].ix[index]
            _dict['happiness'] = df_similar_merged['happiness'].ix[index]
            _dict['neutral'] = df_similar_merged['neutral'].ix[index]
            _dict['sadness'] = df_similar_merged['sadness'].ix[index]
            _dict['surprise'] = df_similar_merged['surprise'].ix[index]
            similer_list.append(_dict)
        context = {
            'similer_list': similer_list
        }
        return render(request, 'main/my-pic.html', context)
    return None


def user_face_file_upload(request):
    """
    プロフィール写真をアップロードする
    :param request:
    :return:
    """
    form_image = UploadFaceImage()

    # POSTであった場合、顔写真を登録する
    if request.POST:
        # まず一旦画像を保存する
        face_image = request.FILES.get('face_image_path')
        insert_data = Face(face_id='null', path=face_image)
        insert_data.save()

        # Face APIに登録する
        face_image_path = UPLOADE__FACE_DIR + str(request.FILES.get('face_image_path'))
        face_id = CreateFaceList().add_user_face(file_path=face_image_path)
        # 顔が検出されなかった場合, nullが返ってくる
        insert_data = Face.objects.all().filter(face_id='null')
        insert_data.update(face_id=face_id) if face_id != 'null' else insert_data.update(face_id='no face')

        df_face_path = GetFaceList().get_face_list(db_table='main_face')
        path_list = []
        for path in list(df_face_path['path']):
            path_dict = {}
            path_dict['path'] = path
            path_list.append(path_dict)

        context = {
            'face_list': path_list
        }

        return render(request, 'face_list.html', context)
    context = {
        'form': form_image
    }
    return render(request, 'upload_user_face.html', context)


def file_upload(request):
    """
    写真をアップロードする
    :param request:
    :return:
    """
    form_image = UploadFaceImage()

    # POSTであった場合、顔写真を登録する
    if request.POST:
        # まず一旦画像を保存する
        image = request.FILES.get('image_path')
        insert_data = PersistedFace(persisted_id='null', path=image)
        insert_data.save()

        # Face APIに登録する
        image_path = UPLOADE__IMAGE_DIR + str(request.FILES.get('image_path'))
        picture_id = CreateFaceList().add_picture_to_facelist(face_list_id=FACE_LIST_ID, file_path=image_path)
        # 顔が検出されなかった場合, nullが返ってくる
        insert_data = PersistedFace.objects.all().filter(persisted_id='null')
        insert_data.update(persisted_id=picture_id) if picture_id != 'null' else insert_data.update(
            persisted_id='no face')

        # 感情を推定し、DBに保管する
        if picture_id != 'null':
            emotion = DetectEmotion().detect_emotion(file_path=image_path)
            insert_data = PersistedFace.objects.all().filter(persisted_id=picture_id)
            insert_data.update(anger=emotion['anger'],
                               contempt=emotion['contempt'],
                               disgust=emotion['disgust'],
                               fear=emotion['fear'],
                               happiness=emotion['happiness'],
                               neutral=emotion['neutral'],
                               sadness=emotion['sadness'],
                               surprise=emotion['surprise'])

        df_face_path = GetFaceList().get_face_list(db_table='main_persistedface')
        path_list = []
        for path in list(df_face_path['path']):
            path_dict = {}
            path_dict['path'] = path
            path_list.append(path_dict)

        context = {
            'face_list': path_list
        }

        return render(request, 'picture_list.html', context)

    context = {
        'form': form_image
    }
    return render(request, 'upload_picture.html', context)


def get_face_list(request):
    """
    プロフィール画像を返す
    :param request:
    :return:
    """
    # face_list = CreateFaceList().get_facelist(face_list_id=FACE_LIST_ID)
    # df_face = pd.DataFrame(face_list['face_id'])
    df_face_path = GetFaceList().get_face_list(db_table='main_face')
    path_list = []
    for path in list(df_face_path['path']):
        path_dict = {}
        path_dict['path'] = path
        path_list.append(path_dict)

    context = {
        'face_list': path_list
    }

    return render(request, 'face_list.html', context)


def get_picture_list(request):
    """
    画像を返す
    :param request:
    :return:
    """
    # face_list = CreateFaceList().get_facelist(face_list_id=FACE_LIST_ID)
    # df_face = pd.DataFrame(face_list['face_id'])
    df_face_path = GetFaceList().get_face_list(db_table='main_persistedface')
    path_list = []
    for path in list(df_face_path['path']):
        path_dict = {}
        path_dict['path'] = path
        path_list.append(path_dict)

    context = {
        'face_list': path_list
    }

    return render(request, 'picture_list.html', context)


def get_similar_list(request):
    """
    アップロードされた画像と対象画像の類似度を計算する
    :param request:
    :return:
    """
    if request.GET:
        user_face_path = request.GET['path']
        face_id = Face.objects.get(path=user_face_path).face_id
        r = FindSimilarFace().get_similar_face(face_id=face_id, face_list_id=FACE_LIST_ID).json()
        sim_list = []
        for sim in r:
            temp = sim['persistedFaceId'], sim['confidence']
            sim_list.append(temp)
        # 類似度計算結果を取得
        df_similar_picture = (pd.DataFrame(sim_list, columns=['persisted_id', 'confidence']))
        # 画像を取得
        df_picture_path = GetFaceList().get_face_list(db_table='main_persistedface')
        df_similar_merged = pd.merge(df_similar_picture, df_picture_path, on='persisted_id')

        similer_list = []
        for index in df_similar_merged.index:
            _dict = {}
            _dict['path'] = df_similar_merged['path'].ix[index]
            _dict['conf'] = df_similar_merged['confidence'].ix[index]
            _dict['anger'] = df_similar_merged['anger'].ix[index]
            _dict['contempt'] = df_similar_merged['contempt'].ix[index]
            _dict['disgust'] = df_similar_merged['disgust'].ix[index]
            _dict['fear'] = df_similar_merged['fear'].ix[index]
            _dict['happiness'] = df_similar_merged['happiness'].ix[index]
            _dict['neutral'] = df_similar_merged['neutral'].ix[index]
            _dict['sadness'] = df_similar_merged['sadness'].ix[index]
            _dict['surprise'] = df_similar_merged['surprise'].ix[index]
            similer_list.append(_dict)
        context = {
            'similer_list': similer_list
        }
        return render(request, 'similer_list.html', context)
    return None


def take_picture(request):
    """
    Webカメラを通じて写真を撮影する
    :param request:
    :return:
    """
    file_upload(request)
    return render(request, 'main/templates/camera.html')
