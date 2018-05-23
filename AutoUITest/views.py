from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from DataServer.models import UserInfo
import logging
import json
from django.db import DataError
from django.http import JsonResponse

# Create your views here.

logger = logging.getLogger('AutoUITest')


def register(request):
    if request.is_ajax():
        try:
            user_json = json.loads(request.body.decode('utf-8'))
            user_info = UserInfo.objects
            username = user_json.pop('account')
            password = user_json.pop('password')
            if user_info.filter(username__exact=username).filter(status=1).count() > 0:
                logger.debug('{username} 已被其他用户注册'.format(username=username))
                return '该用户名已被注册，请更换用户名'
            user_info.create(username=username, password=password)
            logger.info('新增用户：{user_info}'.format(user_info=user_info))
            return JsonResponse({"status": "success"}, safe=False)
        except DataError:
            logger.error('信息输入有误：{user_info}'.format(user_info=user_info))
        return '字段长度超长，请重新编辑'
    elif request.method == 'GET':
        return render(request, "register.html")


def login(request):
    if request.method == 'POST':
        username = request.POST.get('account')
        password = request.POST.get('password')

        if UserInfo.objects.filter(username__exact=username).filter(password__exact=password).count() == 1:
            logger.info('{username} 登录成功'.format(username=username))
            request.session["login_status"] = True
            request.session["now_account"] = username
            return HttpResponseRedirect('/api/index/')
        else:
            logger.info('{username} 登录失败, 请检查用户名或者密码'.format(username=username))
            request.session["login_status"] = False
            return render(request, "login.html")
    elif request.method == 'GET':
        return render(request, "login.html")
