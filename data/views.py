from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .utils.pagination import get_pager_info
from .models import ProjectInfo, ModuleInfo, TestCaseInfo,EnvInfo
from .utils.operation import add_project_data
from .utils.common import get_ajax_msg, set_filter_session
import logging
import json

logger = logging.getLogger('AutoUITest')


def index(request):
    if request.session.get('login_status'):
        project_length = ProjectInfo.objects.count()
        module_length = ModuleInfo.objects.count()
        testcase_length = TestCaseInfo.objects.count()
        env_length = EnvInfo.objects.count()
        manage_info = {
            'project_length': project_length,
            'module_length': module_length,
            'testcase_length': testcase_length,
            'env_length': env_length,
            'account': request.session["now_account"]
        }
        return render(request, 'index.html', manage_info)
    else:
        return HttpResponseRedirect("/login/")


def add_project(request):
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            try:
                project_json = json.loads(request.body.decode('utf-8'))
            except ValueError:
                logger.error('项目信息解析异常: {project_info}'.format(project_info=project_json))
                return JsonResponse(get_ajax_msg('sorry', '项目信息解析异常'))
            ajax_dict = add_project_data(**project_json)
            return JsonResponse(ajax_dict)
        elif request.method == 'GET':
            manage_info = {
                'account': account
            }
            return render(request, "add_project.html", manage_info)
    else:
        return HttpResponseRedirect("/login/")


def project_list(request, id):
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            try:
                project_json = json.loads(request.body.decode('utf-8'))
            except ValueError:
                logger.error('项目信息解析异常: {project_info}'.format(project_info=project_json))
                return JsonResponse(get_ajax_msg('sorry', '项目信息解析异常'))
            # 包含mode为删除，不包含则为添加
            if 'mode' in project_json.keys():
                pass
            else:
                ajax_dict = add_project_data(type=False, **project_json)
                return JsonResponse(ajax_dict)
        else:
            filter_query = set_filter_session(request)
            pro_list = get_pager_info(
                ProjectInfo, filter_query, '/data/project_list/', id)
            manage_info = {
                'account': account,
                'project': pro_list[1],
                'page_list': pro_list[0],
                'info': filter_query,
                'sum': pro_list[2],
            }
            return render(request, 'project_list.html', manage_info)
    else:
        return HttpResponseRedirect("/login/")