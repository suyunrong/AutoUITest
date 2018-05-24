from django.db import DataError

from data.models import UserInfo, ProjectInfo
from utils.common import get_ajax_msg
import logging

logger = logging.getLogger('AutoUITest')

def add_register_data(**kwargs):
    '''
    用户注册逻辑
    :param kwargs: dict: kwargs
    :return:
    '''
    user_info = UserInfo.objects
    try:
        username = kwargs.pop('account')
        password = kwargs.pop('password')
        if user_info.filter(username__exact=username).filter(status=1).count() > 0:
            logger.debug('{username} 已被其他用户注册'.format(username=username))
            return '该用户名已被注册，请更换用户名'
        user_info.create(username=username, password=password)
        logger.info('新增用户：{user_info}'.format(user_info=user_info))
        return get_ajax_msg('ok', '恭喜您，账号注册成功')
    except DataError:
        logger.error('信息输入有误：{user_info}'.format(user_info=user_info))
        return get_ajax_msg('sorry', '字段长度超长，请重新编辑')


def add_project_data(**kwargs):
    project_info = ProjectInfo.objects
    try:
        project_name = kwargs.pop('project_name')
        dev_leader = kwargs.pop('dev_leader')
        test_leader = kwargs.pop('test_leader')
        simple_desc = kwargs.pop('simple_desc')
        other_desc = kwargs.pop('other_desc')
    except DataError:
        pass