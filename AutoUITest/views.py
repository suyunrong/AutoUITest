from django.http import HttpResponseRedirect
from django.shortcuts import render
from data.models import UserInfo
import logging
import json
from utils.operation import add_register_data
from django.http import JsonResponse

logger = logging.getLogger('AutoUITest')


def register(request):
    if request.is_ajax():
        user_json = json.loads(request.body.decode('utf-8'))
        ajax_dict = add_register_data(**user_json)
        return JsonResponse(ajax_dict)
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
            return HttpResponseRedirect('/data/index/')
        else:
            logger.info('{username} 登录失败, 请检查用户名或者密码'.format(username=username))
            request.session["login_status"] = False
            return render(request, "login.html")
    elif request.method == 'GET':
        return render(request, "login.html")


def logout(request):
    if request.method == 'GET':
        logger.info('{username}退出'.format(username=request.session['now_account']))
        try:
            request.session["login_status"] = False
            del request.session['now_account']
        except KeyError:
            logging.error('session invalid')
        return HttpResponseRedirect("/login/")
