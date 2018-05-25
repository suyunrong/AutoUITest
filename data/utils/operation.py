from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError

from data.models import UserInfo, ProjectInfo, ModuleInfo, TestCaseInfo, TestCaseScriptInfo
from data.utils.common import get_ajax_msg
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


def add_project_data(type=True, **kwargs):
    '''
    添加项目逻辑
    :param type: True:新增，Flase:更新
    :param kwargs:
    :return:
    '''
    project_info = ProjectInfo.objects
    project_name = kwargs.get('project_name')
    if type:
        try:
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
                return get_ajax_msg('ok', '项目添加成功')
            else:
                logger.debug('{project_name} 项目名已经存在'.format(project_name=project_name))
                return get_ajax_msg('sorry', '项目名已经存在，请更换项目名')
        except DataError:
            return get_ajax_msg('sorry', '项目信息过长，请重新编辑')
    else:
        try:
            project_obj = project_info.get(id=kwargs.get('index'))
            project_obj.project_name = kwargs.get('project_name')
            project_obj.dev_leader = kwargs.get('dev_leader')
            project_obj.test_leader = kwargs.get('test_leader')
            project_obj.simple_desc = kwargs.get('simple_desc')
            project_obj.other_desc = kwargs.get('other_desc')
            project_obj.save()
            logger.info('项目更新成功: {kwargs}'.format(kwargs=kwargs))
            return get_ajax_msg('ok', '项目更新成功')
        except DataError:
            return get_ajax_msg('sorry', '项目信息过长，请重新编辑')
        except Exception:
            logging.error('更新失败：{kwargs}'.format(kwargs=kwargs))
            return get_ajax_msg('sorry', '更新失败，请重试')

def del_project_data(id):
    try:
        project_name = ProjectInfo.objects.get(id=id).project_name
        belong_modules = ModuleInfo.objects.filter(belong_project__project_name=project_name).values_list()
        for case_obj in belong_modules:
            pass
        ModuleInfo.objects.filter(belong_project__project_name=project_name).delete()
        ProjectInfo.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        pass