from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from DataServer.models import UserInfo
import logging
from django import forms
from django.db import DataError

# Create your views here.

logger = logging.getLogger('AutoUITest')


# 表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=12)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            try:
                user_info = UserInfo.objects
                user_info.create(username=username, password=password)
                logger.info('新增用户: {user_info}'.format(user_info=user_info))
                return render_to_response()
            except DataError:
                logger.error('信息输入有误：{user_info}'.format(user_info=user_info))