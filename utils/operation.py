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
            return get_ajax_msg('sorry', '该用户名已被注册，请更换用户名')
        user_info.create(username=username, password=password)
        logger.info('新增用户：{user_info}'.format(user_info=user_info))
        return get_ajax_msg('ok', '恭喜您，账号注册成功')
    except DataError:
        logger.error('信息输入有误：{user_info}'.format(user_info=user_info))
        return get_ajax_msg('sorry', '用户名长度超长，请重新编辑')


def add_project_data(**kwargs):
    '''
    添加项目逻辑
    :param kwargs:
    :return:
    '''
    project_info = ProjectInfo.objects
    try:
        project_name = kwargs.get('project_name')

        if kwargs.get('project_name') is '':
            return get_ajax_msg('sorry', '项目名称不能为空')
        if kwargs.get('dev_leader') is '':
            return get_ajax_msg('sorry', '开发负责人不能为空')
        if kwargs.get('test_leader') is '':
            return get_ajax_msg('sorry', '测试负责人不能为空')
        if kwargs.get('simple_desc') is '':
            return get_ajax_msg('sorry', '简要描述不能为空')

        if project_info.filter(project_name__exact=project_name).count() < 1:
            project_info.create(**kwargs)
            logger.info('新增项目：{project_info}'.format(project_info=project_info))
            return get_ajax_msg('ok', '/data/project_list/1')
        else:
            logger.debug('{project_name} 项目名已经存在'.format(project_name=project_name))
            return get_ajax_msg('sorry', '项目名已经存在，请更换项目名')
    except DataError:
        return get_ajax_msg('sorry', '项目名长度超长，请重新编辑')