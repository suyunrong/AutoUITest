from django import template
from data.models import TestCaseInfo

register = template.Library()


@register.filter(name='data_type')
def data_type(value):
    """
    返回数据类型 自建filter
    :param value:
    :return: the type of value
    """
    return str(type(value).__name__)


@register.filter(name='convert_eval')
def data_type(value):
    """
    数据eval转换 自建filter
    :param value:
    :return: the value which had been eval
    """
    return eval(value)


@register.filter(name='get_prepost_case_name')
def data_type(value):
    """
    获取前置后置用例名
    :param value:
    :return:
    """
    value = eval(value)
    if len(value) == 0:
        return '无'
    return TestCaseInfo.objects.get(id=value[0]).case_name


@register.filter(name='get_prepost_case_id')
def data_type(value):
    """
    获取前置后置用例id
    :param value:
    :return:
    """
    value = eval(value)
    if len(value) == 0:
        return '无'
    # return TestCaseInfo.objects.get(id=value[0]).id
    return value[0]