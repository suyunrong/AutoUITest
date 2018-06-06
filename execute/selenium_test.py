import unittest
from execute import config
import time
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


# class TestCase(unittest.TestCase):
#     pass
#
#
# class TestSuite(unittest.TestSuite):
#     pass


# driver = config.driver
# config.max_browser(driver)
# driver.get('http://www.baidu.com')
# time.sleep(1)
# config.quit_browser(driver)


class TestCase(unittest.TestCase):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def runTest(self):
        self.driver.get('http://www.baidu.com')
        time.sleep(1)


class TestSuite(unittest.TestSuite):
    def __init__(self, tests=()):
        super().__init__(tests)


driver = config.driver
suite = TestSuite((TestCase(driver),))
unittest.TextTestRunner().run(suite)