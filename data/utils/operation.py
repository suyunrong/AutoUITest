from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from data.models import UserInfo, ProjectInfo, ModuleInfo, TestCaseInfo, EnvInfo
from data.utils.common import get_ajax_msg, load_modules, load_cases
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
        nickname = kwargs.pop('nickname')
        password = kwargs.pop('password')
        if user_info.filter(username__exact=username).filter(status=1).count() > 0:
            logger.debug('{username} 已被其他用户注册'.format(username=username))
            return get_ajax_msg('sorry', '该用户名已被注册，请更换用户名')
        user_info.create(username=username, nickname=nickname, password=password)
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
            id = kwargs.pop('index')
            if project_name != project_info.get(id=id).project_name and \
                project_info.filter(project_name__exact=project_name).count() > 0:
                return get_ajax_msg('sorry', '项目名已经存在，请更换项目名')
            project_obj = project_info.get(id=id)
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
    '''
    删除项目逻辑
    :param id:
    :return:
    '''
    try:
        project_name = ProjectInfo.objects.get(id=id).project_name
        belong_modules = ModuleInfo.objects.filter(belong_project__project_name=project_name).values_list('module_name')
        for module_name in belong_modules:
            belong_testcase = TestCaseInfo.objects.filter(belong_module__module_name=module_name[0]).values_list(
                'case_name')
            for case_name in belong_testcase:
                TestCaseInfo.objects.filter(case_name__exact=case_name).delete()
        ModuleInfo.objects.filter(belong_project__project_name=project_name).delete()
        ProjectInfo.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        return get_ajax_msg('sorry', '项目删除异常，请重试')
    logging.info('{project_name} 项目已删除'.format(project_name=project_name))
    return get_ajax_msg('ok', '项目删除成功')


def add_module_data(type=True, **kwargs):
    '''
    添加模块逻辑
    :param type:
    :param kwargs:
    :return:
    '''
    module_info = ModuleInfo.objects
    belong_project = kwargs.pop('belong_project')
    module_name = kwargs.get('module_name')
    if type:
        try:
            if kwargs.get('module_name') is '':
                return get_ajax_msg('sorry', '模块名称不能为空')
            if kwargs.get('belong_project') is '':
                return get_ajax_msg('sorry', '所属项目不能为空')
            if kwargs.get('test_user') is '':
                return get_ajax_msg('sorry', '测试人员不能为空')

            if module_info.filter(belong_project__project_name__exact=belong_project) \
                    .filter(module_name__exact=module_name).count() < 1:
                try:
                    belong_project = ProjectInfo.objects.get(project_name__exact=belong_project)
                except ObjectDoesNotExist:
                    logging.error('项目信息读取失败：{belong_project}'.format(belong_project=belong_project))
                    return '项目信息读取失败，请重试'
                kwargs['belong_project'] = belong_project
                module_info.create(**kwargs)
                logger.info('新增模块：{module_info}'.format(module_info=module_info))
                return get_ajax_msg('ok', '模块添加成功')
            else:
                return get_ajax_msg('sorry', '模块名已经在项目中存在，请更换模块名')
        except DataError:
            return get_ajax_msg('sorry', '模块信息过长，请重新编辑')
    else:
        try:
            if module_name != module_info.get(id=kwargs.get('index')).module_name \
                    and module_info.filter(belong_project__project_name__exact=belong_project) \
                    .filter(module_name__exact=module_name).count() > 0:
                return get_ajax_msg('sorry', '模块名已经在项目中存在，请更换模块名')

            module_obj = module_info.get(id=kwargs.pop('index'))
            module_obj.module_name = kwargs.get('module_name')
            module_obj.test_leader = kwargs.get('test_leader')
            module_obj.simple_desc = kwargs.get('simple_desc')
            module_obj.other_desc = kwargs.get('other_desc')
            module_obj.save()

            logger.info('模块更新成功: {kwargs}'.format(kwargs=kwargs))
            return get_ajax_msg('ok', '模块更新成功')
        except DataError:
            return get_ajax_msg('sorry', '模块信息过长，请重新编辑')
        except Exception:
            logging.error('更新失败：{kwargs}'.format(kwargs=kwargs))
            return get_ajax_msg('sorry', '更新失败，请重试')


def del_module_data(id):
    '''
    删除模块逻辑
    :param id:
    :return:
    '''
    try:
        module_name = ModuleInfo.objects.get(id=id).module_name
        TestCaseInfo.objects.filter(belong_module__module_name=module_name).delete()
        ModuleInfo.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        return get_ajax_msg('sorry', '模块删除异常，请重试')
    logging.info('{module_name} 模块已删除'.format(module_name=module_name))
    return get_ajax_msg('ok', '模块删除成功')


def add_case_data(type=True, **kwargs):
    case_json = kwargs.get('case')
    scripts_json = kwargs.get('scripts')
    case_info = TestCaseInfo.objects
    belong_project = case_json.get('belong_project')
    belong_module = case_json.get('belong_module')
    case_name = case_json.get('case_name')

    if case_json.get('case_name') is '':
        return get_ajax_msg('sorry', '用例名称不能为空')
    if case_json.get('belong_project') is '':
        return get_ajax_msg('sorry', '所属项目不能为空')
    if case_json.get('belong_module') is '':
        return get_ajax_msg('sorry', '所属模块不能为空')
    if case_json.get('author') is '':
        return get_ajax_msg('sorry', '所有者不能为空')
    if scripts_json.get('scripts') is None:
        return get_ajax_msg('sorry', '脚本不能为空')

    if type:
        try:
            if case_info.filter(belong_module_id=belong_module) \
                    .filter(case_name__exact=case_name).count() < 1:
                try:
                    belong_module = ModuleInfo.objects.get(id=belong_module)
                except ObjectDoesNotExist:
                    logging.error('模块信息读取失败：{belong_module}'.format(belong_module=belong_module))
                    return '模块信息读取失败，请重试'
                case_json['belong_project'] = belong_project
                case_json['belong_module'] = belong_module
                case_json['case_scripts'] = scripts_json
                if 'is_execute' in case_json.keys():
                    case_json['is_execute'] = True
                case_info.create(**case_json)
                logger.info('新增用例：{case_info}'.format(case_info=case_info))
                return get_ajax_msg('ok', '用例添加成功')
            else:
                return get_ajax_msg('sorry', '用例名已经在模块中存在，请更换用例名')
        except DataError:
            return get_ajax_msg('sorry', '用例信息过长，请重新编辑')
    else:
        try:

            case_name = case_json.get('case_name')
            if case_name != case_info.get(id=case_json.get('case_index')).case_name \
                    and case_info.filter(belong_module_id=belong_module).filter(case_name__exact=case_name).count() > 0:
                return get_ajax_msg('sorry', '用例名已经在模块中存在，请更换用例名')
            try:
                belong_module = ModuleInfo.objects.get(id=belong_module)
            except ObjectDoesNotExist:
                logging.error('模块信息读取失败：{belong_module}'.format(belong_module=belong_module))
                return '模块信息读取失败，请重试'

            case_obj = case_info.get(id=case_json.pop('case_index'))
            case_obj.case_name = case_json.get('case_name')
            case_obj.belong_project = belong_project
            case_obj.belong_module = belong_module
            case_obj.author = case_json.get('author')
            case_obj.case_desc = case_json.get('case_desc')
            case_obj.case_scripts = scripts_json
            case_obj.prepos_case = case_json.get('prepos_case')
            case_obj.postpos_case = case_json.get('postpos_case')
            if 'is_execute' not in case_json.keys():
                case_obj.is_execute = False
            else:
                case_obj.is_execute = True
            case_obj.save()

            logger.info('更新用例：{case_info}'.format(case_info=case_obj))
            return get_ajax_msg('ok', '用例更新成功')

        except DataError:
            return get_ajax_msg('sorry', '用例信息过长，请重新编辑')
        except Exception:
            logging.error('更新失败：{kwargs}'.format(kwargs=kwargs))
            return get_ajax_msg('sorry', '更新失败，请重试')


def copy_case_data(id, name):
    """
    复制用例逻辑
    :param id:
    :param name:
    :return:
    """
    case_info = TestCaseInfo.objects.get(id=id)
    belong_module = case_info.belong_module
    if TestCaseInfo.objects.filter(case_name=name, belong_module=belong_module).count() > 0:
        return get_ajax_msg('sorry', '用例名称重复，请重新输入')
    case_info.id = None
    case_info.case_name = name
    case_info.save()
    return get_ajax_msg('ok', '用例复制成功')


def del_case_data(id):
    case_name = TestCaseInfo.objects.get(id=id).case_name
    TestCaseInfo.objects.get(id=id).delete()
    logging.info('{case_name} 用例已删除'.format(case_name=case_name))
    return get_ajax_msg('ok', '用例删除成功')


def choose_data(**kwargs):
    '''
    动态下拉获取模块、用例逻辑
    :param kwargs:
    :return:
    '''
    testcase = kwargs.get('testcase')
    type = testcase.pop('type')
    if type == 'module':
        return load_modules(**testcase)
    elif type == 'case':
        return load_cases(**testcase)
    # return load_modules(**testcase) if type == 'module' else load_cases(**testcase)


def add_env_data(type=True, **kwargs):
    """
    添加、修改环境逻辑
    :param type:
    :param kwargs:
    :return:
    """
    id = kwargs.pop('index')
    env_info = EnvInfo.objects
    env_name = kwargs.get('env_name')
    if type:
        try:
            if kwargs.get('env_name') is '':
                return get_ajax_msg('sorry', '环境名称不能为空')
            if kwargs.get('base_url') is '':
                return get_ajax_msg('sorry', '环境URL不能为空')
            if kwargs.get('explorer_name') is '':
                return get_ajax_msg('sorry', '浏览器名称不能为空')
            if kwargs.get('explorer_version') is '':
                return get_ajax_msg('sorry', '浏览器版本不能为空')
            if env_info.filter(env_name__exact=env_name).count() < 1:
                env_info.create(**kwargs)
                logger.info('新增环境：{env_info}'.format(env_info=env_info))
                return get_ajax_msg('ok', '环境添加成功')
            else:
                logger.debug('{env_name} 环境名已经存在'.format(env_name=env_name))
                return get_ajax_msg('sorry', '环境名已经存在，请更换环境名')
        except:
            logger.error('信息输入有误：{env_info}'.format(env_info=env_info))
            return get_ajax_msg('sorry', '环境信息过长，请重新输入')
    else:
        try:
            if env_name != env_info.get(id=id).env_name and env_info.filter(env_name__exact=env_name).count() > 0:
                return get_ajax_msg('sorry', '环境名已经存在，请更换环境名')
            env_obj = env_info.get(id=id)
            env_obj.env_name = kwargs.get('env_name')
            env_obj.base_url = kwargs.get('base_url')
            env_obj.explorer_name = kwargs.get('explorer_name')
            env_obj.explorer_version = kwargs.get('explorer_version')
            env_obj.simple_desc = kwargs.get('simple_desc')
            env_obj.save()
            logger.info('环境更新成功: {kwargs}'.format(kwargs=kwargs))
            return get_ajax_msg('ok', '环境更新成功')
        except DataError:
            return get_ajax_msg('sorry', '环境信息过长，请重新编辑')
        except Exception:
            logging.error('更新失败：{kwargs}'.format(kwargs=kwargs))
            return get_ajax_msg('sorry', '更新失败，请重试')


def del_env_data(id):
    env_name = EnvInfo.objects.get(id=id).env_name
    EnvInfo.objects.get(id=id).delete()
    logging.info('{env_name} 环境已删除'.format(env_name=env_name))
    return get_ajax_msg('ok', '环境删除成功')