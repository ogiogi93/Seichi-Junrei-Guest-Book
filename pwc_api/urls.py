"""pwc_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from main.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', top_page, name='top_page'),
    url(r'^cate/', cate_page, name='cate_page'),
    url(r'^setting/', setting_page, name='setting_page'),
    url(r'^pic/', pic_page, name='pic_page'),
    url(r'^move/', move_page, name='move_page'),
    url(r'^uber/', ubser_assging, name='uber_page'),
    url(r'^uper/', uper_page, name='uper_page'),
    url(r'^sel_pic/', sel_pic_page, name='sel_pic_page'),
    url(r'^my_pic/', my_pic_page, name='my_pic_page'),
    url(r'^all_pic/', all_picture_page, name='all_picture_page'),
    url(r'^camera/', take_picture, name='take_picture'),
    url(r'^upload/user/$', user_face_file_upload, name='user_face_file_upload'),
    url(r'^upload/picture/$', file_upload, name='file_upload'),
    url(r'^get/face_list/$', get_face_list, name='get_face_list'),
    url(r'^get/picture_list/$', get_picture_list, name='get_picture_list'),
    url(r'^get/similar_list/$', get_similar_list, name='get_similar_list'),
]
