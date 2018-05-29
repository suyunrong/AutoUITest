from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from data.models import UserInfo, ProjectInfo, ModuleInfo, TestCaseInfo, TestCaseScriptInfo
from data.utils.common import get_ajax_msg, load_modules, load_cases, load_cases_list
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
            project_obj = project_info.get(id=kwargs.pop('index'))
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
                TestCaseScriptInfo.objects.filter(belong_testcase__case_name=case_name[0]).delete()
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
        belong_testcase = TestCaseInfo.objects.filter(belong_module__module_name=module_name).values_list('case_name')
        for case_name in belong_testcase:
            TestCaseScriptInfo.objects.filter(belong_testcase__case_name=case_name).delete()
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
    if type:
        try:
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
                case_info.create(**case_json)
                logger.info('新增用例：{case_info}'.format(case_info=case_info))
                return get_ajax_msg('ok', '用例添加成功')
            else:
                return get_ajax_msg('sorry', '用例名已经在模块中存在，请更换用例名')
        except DataError:
            return get_ajax_msg('sorry', '用例信息过长，请重新编辑')
    else:
        try:
            if case_name != case_info.get(id=kwargs.get('index')).case_name \
                    and case_info.filter(belong_project__exact=belong_project) \
                    .filter(belong_module__module_name=belong_module).count() > 0:
                return get_ajax_msg('sorry', '用例名已经在项目中存在，请更换用例名')
            try:
                belong_module = ModuleInfo.objects.get(module_name__exact=belong_module);
            except ObjectDoesNotExist:
                logging.error('模块信息读取失败：{belong_module}'.format(belong_module=belong_module))
                return '模块信息读取失败，请重试'
            kwargs['belong_module'] = belong_module
            case_obj = case_info.get(id=kwargs.pop('index'))
            case_obj.case_name = kwargs.get('case_name')
            case_obj.belong_module = kwargs.get('belong_module')
            case_obj.author = kwargs.get('author')
            case_obj.case_desc = kwargs.get('case_desc')
            case_obj.prepos_case = kwargs.get('prepos_case')
            case_obj.postpos_case = kwargs.get('postpos_case')
            case_obj.save()

            logger.info('用例更新成功: {kwargs}'.format(kwargs=kwargs))
            return get_ajax_msg('ok', '用例更新成功')
        except DataError:
            return get_ajax_msg('sorry', '用例信息过长，请重新编辑')
        except Exception:
            logging.error('更新失败：{kwargs}'.format(kwargs=kwargs))
            return get_ajax_msg('sorry', '更新失败，请重试')


def copy_case_data(id, name):
    case_info = TestCaseInfo.objects.get(id=id)
    belong_module = case_info.belong_module
    if TestCaseInfo.objects.filter(name=name, belong_module=belong_module).count() > 0:
        return get_ajax_msg('sorry', '用例名称重复，请重新输入')
    case_info.id = None
    case_info.name = name
    case_info.save()
    return get_ajax_msg('ok', '用例复制成功')



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
    elif type == 'case_list':
        return load_cases_list(**testcase)
    # return load_modules(**testcase) if type == 'module' else load_cases(**testcase)
