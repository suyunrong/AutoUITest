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