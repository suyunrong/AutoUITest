from selenium.common.exceptions import NoSuchElementException


def alert(driver, **kwargs):
    """
    获取alert弹窗信息
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def back(driver, **kwargs):
    """
    浏览器后退
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def checkbox(driver, **kwargs):
    """
    多选框
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def clear(driver, **kwargs):
    """
    清除文本
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def enter(driver, **kwargs):
    """
    Enter键
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def execute_script(driver, **kwargs):
    """
    执行javascript语句
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def forward(driver, **kwargs):
    """
    浏览器前进
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def get_text(driver, **kwargs):
    """
    获取各标签文本内容
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def get_title(driver, **kwargs):
    """
    获取页面title
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def get_url(driver, **kwargs):
    """
    获取页面URL
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def is_element_exist(driver, **kwargs):
    """
    判断单个元素是否存在
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def is_elements_exist(driver, **kwargs):
    """
    判断一组元素是否存在
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def mouse_click(driver, **kwargs):
    """
    鼠标单击
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


def mouse_context_click(driver, **kwargs):
    """
    鼠标右键单击
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def mouse_double_click(driver, **kwargs):
    """
    鼠标双击
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def mouse_drag_and_drop(driver, **kwargs):
    """
    鼠标拖动
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def mouse_move_to_element(driver, **kwargs):
    """
    鼠标悬停
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def radio(driver, **kwargs):
    """
    单选框
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def refresh(driver, **kwargs):
    """
    刷新页面
    :param driver:
    :param kwargs:
    :return:
    """
    pass


def select(driver, **kwargs):
    """
    选中下拉文本
    :param driver:
    :param kwargs:
    :return:
    """
    pass


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


def to_url(driver, **kwargs):
    """
    访问URL
    :param driver:
    :param kwargs:
    :return:
    """
    url = kwargs.get('ele_pos')
    driver.get(url)