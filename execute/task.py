import unittest
from execute.runner import run_test

class TestCase(unittest.TestCase):
    def __init__(self, driver, testcase_list):
        super().__init__()
        self.driver = driver
        self.testcase_list = testcase_list


    def runTest(self):
        run_test(self.driver, self.testcase_list)


class TestSuite(unittest.TestSuite):
    def __init__(self, tests=()):
        super().__init__(tests)