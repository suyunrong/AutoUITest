from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from data.models import TestCaseInfo, EnvInfo
from execute.task import TestCase, TestSuite
from execute.runner import run_test, get_summary
import unittest

def init_driver(base_url, explorer_name, explorer_version):

    global capabilities

    if explorer_name.lower() == 'chrome':
        capabilities = DesiredCapabilities.CHROME
        capabilities['version'] = explorer_version

    driver = webdriver.Remote(command_executor=base_url,
                              desired_capabilities=capabilities)
    driver.maximize_window()
    return driver


def quit_driver(driver):
    driver.quit()


def run_single_case(case_id, env_id):

    testcase_list = [

    ]

    tt_dict = {
        'failfast': 'False'
    }

    case_info = TestCaseInfo.objects.get(id=case_id)
    env_info = list(EnvInfo.objects.filter(id=env_id).values('base_url', 'explorer_name', 'explorer_version'))[0]
    case_scripts = eval(case_info.case_scripts).get('scripts')

    driver = init_driver(env_info.get('base_url'), env_info.get('explorer_name'), env_info.get('explorer_version'))

    testcase = TestCase(driver, case_scripts)
    suite = TestSuite((testcase,))
    result = unittest.TextTestRunner(**tt_dict).run(suite)
    summary = get_summary(result)
    quit_driver(driver)

    return summary
