from data.models import ModuleInfo, TestCaseInfo

def get_ajax_msg(msg, content):
    '''
    ajax请求返回方法
    :param msg: str: ok or sorry
    :param content: str:
    :return: dict:
    '''
    return {
        'msg': msg,
        'content': content
    }


def set_filter_session(request):
    """
    查询session
    :param request:
    :return:
    """
    request.session['user'] = '' if 'user' not in request.POST.keys() else request.POST.get('user')
    request.session['name'] = '' if 'name' not in request.POST.keys() else request.POST.get('name')
    request.session['belong_project'] = '' if 'belong_project' not in request.POST.keys() else request.POST.get(
        'belong_project')
    request.session['belong_module'] = '' if 'belong_module' not in request.POST.keys() else request.POST.get(
        'belong_module')
    request.session['report_name'] = '' if 'report_name' not in request.POST.keys() else request.POST.get('report_name')

    filter_query = {
        'user': request.session['user'],
        'name': request.session['name'],
        'belong_project': request.session['belong_project'],
        'belong_module': request.session['belong_module'],
        'report_name': request.session['report_name']
    }

    return filter_query


def load_modules(**kwargs):
    """
    加载对应项目的模块信息，用户前端ajax请求返回
    :param kwargs:  dict：项目相关信息
    :return: str: module_info
    """
    belong_project = kwargs.get('name').get('belong_project')
    module_info = ModuleInfo.objects.filter(belong_project__project_name=belong_project).values_list(
        'id',
        'module_name').order_by(
        '-create_time')
    module_info = list(module_info)
    string = ''
    for value in module_info:
        string = string + str(value[0]) + '^=' + value[1] + 'replaceFlag'
    return get_ajax_msg('ok', string[:len(string) - 11])


def load_cases(**kwargs):
    """
    加载指定项目模块下的用例
    :param kwargs: dict: 项目与模块信息
    :return: str: 用例信息
    """
    belong_project = kwargs.get('name').get('belong_project')
    belong_module = kwargs.get('name').get('belong_module')
    if belong_module == '请选择':
        return get_ajax_msg('ok', '')
    case_info = TestCaseInfo.objects.filter(belong_project=belong_project, belong_module=belong_module) \
        .values_list('id', 'case_name').order_by('-create_time')
    case_info = list(case_info)
    string = ''
    for value in case_info:
        string = string + str(value[0]) + '^=' + value[1] + 'replaceFlag'
    return get_ajax_msg('ok', string[:len(string) - 11])


def load_cases_list(**kwargs):
    """
    加载指定项目模块下的用例
    :param kwargs: dict: 项目与模块信息
    :return: str: 用例信息
    """
    belong_project = kwargs.get('name').get('belong_project')
    belong_module = kwargs.get('name').get('belong_module')
    if belong_module == '请选择':
        return get_ajax_msg('ok', '')
    case_info = TestCaseInfo.objects.filter(belong_project=belong_project, belong_module__module_name=belong_module) \
        .values_list('id', 'case_name').order_by('-create_time')
    case_info = list(case_info)
    string = ''
    for value in case_info:
        string = string + str(value[0]) + '^=' + value[1] + 'replaceFlag'
    return get_ajax_msg('ok', string[:len(string) - 11])