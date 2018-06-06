from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


capabilities = DesiredCapabilities.CHROME
capabilities['version'] = '66.0.3359.117'


driver = webdriver.Remote(command_executor='http://10.10.12.223:4444/wd/hub',
                          desired_capabilities=capabilities)

def max_browser(driver):
    driver.maximize_window()


def quit_browser(driver):
    driver.quit()