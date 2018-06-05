from selenium.common.exceptions import NoSuchElementException

def to_url(driver, **kwargs):
    """
    访问URL
    :param driver:
    :param kwargs:
    :return:
    """
    url = kwargs.get('ele_pos')
    driver.get(url)


def send_keys(driver, **kwargs):
    """
    输入文本
    :param driver:
    :param kwargs:
    :return:
    """
    try:
        ele_pos = kwargs.get('ele_pos')
        page_oper_val = kwargs.get('page_oper_val')
        ele = driver.find_element_by_xpath(ele_pos)
        ele.send_keys(page_oper_val)
    except NoSuchElementException:
        raise Exception('NoSuchElement')


def click(driver, **kwargs):
    """
    点击
    :param driver:
    :param kwargs:
    :return:
    """
    try:
        ele_pos = kwargs.get('ele_pos')
        ele = driver.find_element_by_xpath(ele_pos)
        ele.click()
    except NoSuchElementException:
        raise Exception('NoSuchElement')