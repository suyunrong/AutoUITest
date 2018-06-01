from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .utils.pagination import get_pager_info
from .models import ProjectInfo, ModuleInfo, TestCaseInfo, EnvInfo
from .utils.operation import add_project_data, del_project_data, add_module_data, del_module_data, add_case_data, \
    choose_data, copy_case_data, del_case_data, add_env_data
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
                ajax_dict = del_project_data(id=project_json.get('id'))
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


def add_module(request):
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            try:
                module_json = json.loads(request.body.decode('utf-8'))
            except ValueError:
                logger.error('模块信息解析异常: {module_info}'.format(module_info=module_json))
                return JsonResponse(get_ajax_msg('sorry', '模块信息解析异常'))
            ajax_dict = add_module_data(**module_json)
            return JsonResponse(ajax_dict)
        elif request.method == 'GET':
            manage_info = {
                'account': account,
                'data': ProjectInfo.objects.all().values('project_name').order_by('-create_time')
            }
            return render(request, "add_module.html", manage_info)
    else:
        return HttpResponseRedirect("/login/")


def module_list(request, id):
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            try:
                module_json = json.loads(request.body.decode('utf-8'))
            except ValueError:
                logger.error('模块信息解析异常: {module_info}'.format(module_info=module_json))
                return JsonResponse(get_ajax_msg('sorry', '模块信息解析异常'))
            # 包含mode为删除，不包含则为添加
            if 'mode' in module_json.keys():
                ajax_dict = del_module_data(id=module_json.get('id'))
            else:
                ajax_dict = add_module_data(type=False, **module_json)
            return JsonResponse(ajax_dict)
        else:
            filter_query = set_filter_session(request)
            pro_list = get_pager_info(
                ModuleInfo, filter_query, '/data/module_list/', id)
            manage_info = {
                'account': account,
                'module': pro_list[1],
                'page_list': pro_list[0],
                'info': filter_query,
                'sum': pro_list[2],
            }
            return render(request, 'module_list.html', manage_info)
    else:
        return HttpResponseRedirect("/login/")


def add_case(request):
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            try:
                case_json = json.loads(request.body.decode('utf-8'))
            except ValueError:
                logger.error('用例信息解析异常: {case_info}'.format(case_info=case_json))
                return JsonResponse(get_ajax_msg('sorry', '用例信息解析异常'))
            ajax_dict = add_case_data(**case_json)
            return JsonResponse(ajax_dict)
        elif request.method == 'GET':
            manage_info = {
                'account': account,
                'project_data': ProjectInfo.objects.all().values('project_name').order_by('-create_time'),
            }
            return render(request, "add_case.html", manage_info)
    else:
        return HttpResponseRedirect("/login/")


def choose(request):
    if request.session.get('login_status'):
        if request.is_ajax():
            try:
                case_json = json.loads(request.body.decode('utf-8'))
            except ValueError:
                logger.error('用例信息解析异常: {case_info}'.format(case_info=case_json))
                return JsonResponse(get_ajax_msg('sorry', '用例信息解析异常'))
            ajax_dict = choose_data(**case_json)
            return JsonResponse(ajax_dict)
    else:
        return HttpResponseRedirect("/login/")


def case_list(request, id):
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            try:
                case_json = json.loads(request.body.decode('utf-8'))
            except ValueError:
                logger.error('模块信息解析异常: {case_info}'.format(case_info=case_json))
                return JsonResponse(get_ajax_msg('sorry', '模块信息解析异常'))
            # 包含mode为删除，不包含则为添加
            if  case_json.get('mode') == 'del':
                ajax_dict = del_case_data(id=case_json.get('id'))
            elif case_json.get('mode') == 'copy':
                ajax_dict = copy_case_data(id=case_json.get('data').pop('index'),
                                           name=case_json.get('data').pop('name'))
            return JsonResponse(ajax_dict)
        else:
            filter_query = set_filter_session(request)
            pro_list = get_pager_info(
                TestCaseInfo, filter_query, '/data/case_list/', id)
            manage_info = {
                'account': account,
                'case': pro_list[1],
                'page_list': pro_list[0],
                'info': filter_query,
                'sum': pro_list[2],
            }
            return render(request, 'case_list.html', manage_info)
    else:
        return HttpResponseRedirect("/login/")


def edit_case(request, id=None):
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            try:
                case_json = json.loads(request.body.decode('utf-8'))
            except ValueError:
                logger.error('用例信息解析异常: {case_info}'.format(case_info=case_json))
                return JsonResponse(get_ajax_msg('sorry', '用例信息解析异常'))
            ajax_dict = add_case_data(type=False, **case_json)
            return JsonResponse(ajax_dict)
        case_info = TestCaseInfo.objects.get(id=id)
        scripts_info = eval(case_info.case_scripts)
        project_name = case_info.belong_project
        manage_info = {
            'account': account,
            'case_info': case_info,
            'scripts_info': scripts_info['scripts'],
            'project_data': ProjectInfo.objects.all().values('project_name').order_by('-create_time'),
            'module_data': ModuleInfo.objects.filter(belong_project__project_name=project_name)
                .values('id', 'module_name').order_by('-create_time'),
        }
        return render(request, "edit_case.html", manage_info)
    else:
        return HttpResponseRedirect("/login/")


def add_env(request):
    if request.session.get('login_status'):
        if request.is_ajax():
            try:
                env_json = json.loads(request.body.decode('utf-8'))
            except ValueError:
                logger.error('环境信息解析异常: {env_json}'.format(env_json=env_json))
                return JsonResponse(get_ajax_msg('sorry', '环境信息解析异常'))
            index = env_json.get('index')
            if index == 'add':
                ajax_dict = add_env_data(**env_json)
            elif index == 'edit':
                ajax_dict = add_env_data(type=False, **env_json)
            return JsonResponse(ajax_dict)
    else:
        return HttpResponseRedirect("/login/")


def env_list(request, id):
    if request.session.get('login_status'):
        account = request.session["now_account"]
        if request.is_ajax():
            try:
                env_json = json.loads(request.body.decode('utf-8'))
            except ValueError:
                logger.error('环境信息解析异常: {env_json}'.format(env_json=env_json))
                return JsonResponse(get_ajax_msg('sorry', '环境信息解析异常'))
            # 包含mode为删除，不包含则为添加
            if env_json.get('mode') == 'add':
                ajax_dict = add_env_data(**env_json)
            elif  env_json.get('mode') == 'del':
                ajax_dict = del_case_data(id=env_json.get('id'))
            elif env_json.get('mode') == 'copy':
                ajax_dict = copy_case_data(id=env_json.get('data').pop('index'),
                                           name=env_json.get('data').pop('name'))
            return JsonResponse(ajax_dict)
        else:
            filter_query = set_filter_session(request)
            pro_list = get_pager_info(
                EnvInfo, filter_query, '/data/env_list/', id)
            manage_info = {
                'account': account,
                'env': pro_list[1],
                'page_list': pro_list[0],
                'info': filter_query,
                'sum': pro_list[2],
            }
            return render(request, 'env_list.html', manage_info)
    else:
        return HttpResponseRedirect("/login/")
