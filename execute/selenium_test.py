from . import selenium_oper
import unittest

data = {
        'scripts':[
            {
                'step_desc': '访问首页',
                'ele_pos': 'xxx',
                'page_oper': 'to_url',
                'page_oper_val': 'xxx',
                'page_exp': 'xxx',
                'slepp_time': '1'
            },
            {
                'step_desc': '输入文本',
                'ele_pos': 'xxx',
                'page_oper': 'send_keys',
                'page_oper_val': 'selenium',
                'page_exp': 'xxx',
                'slepp_time': '1'
            },
            {
                'step_desc': '点击搜索',
                'ele_pos': 'xxx',
                'page_oper': 'click',
                'page_oper_val': 'xxx',
                'page_exp': 'xxx',
                'slepp_time': '1'
            }
        ],
        'name': 'name'
    }


class TestCase(unittest.TestCase):
    pass


class TestSuite(unittest.TestSuite):
    pass