from django.http import HttpResponseRedirect
from django.shortcuts import render
import logging
from .models import ProjectInfo, ModuleInfo, TestCaseInfo,EnvInfo

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
            pass
        elif request.method == 'GET':
            manage_info = {
                'account': account
            }
            return render(request, "add_project.html", manage_info)
    else:
        return HttpResponseRedirect("/login/")


def project_list(request, id):
    if request.session.get('login_status'):
        pass
    else:
        return HttpResponseRedirect("/login/")