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