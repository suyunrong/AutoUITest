from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import ProjectInfo, ModuleInfo, TestCaseInfo,EnvInfo

# Create your views here.

def index(request):
    """
    首页
    :param request:
    :return:
    """
    if request.session.get('login_status'):
        project_length = ProjectInfo.objects.count()
        module_length = ModuleInfo.objects.count()
        testcase_length = TestCaseInfo.objects.count()
        env_length = EnvInfo.objects.filter().count()
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