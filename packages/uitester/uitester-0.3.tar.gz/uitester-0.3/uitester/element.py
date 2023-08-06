from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from .common import timethis
from allure_commons.types import AttachmentType
import allure
import time

class WebElement(object):
    """
    基于selenium的页面方法功能，添加或修改了被选中的页面元素的方法
    """
    def __init__(self,selenium_elem,selenium_driver):
        """

        """
        self.driver = selenium_driver
        self.elem = selenium_elem

        # add property
        self.location = selenium_elem.location
        self.size = selenium_elem.size
        self.screenshot = selenium_elem.screenshot

    @timethis
    def select(self,text=None,index=None,value=None):
        if text:
            print('SELECT OPTION BY TEXT : {}'.format(text),end = ' ')
            Select(self.elem).select_by_visible_text(text)

        elif index:
            print('SELECT OPTION BY INDEX : {}'.format(index),end = ' ')
            Select(self.elem).select_by_visible_text(index)

        elif value:
            print('SELECT OPTION BY VALUE : {}'.format(value),end = ' ')
            Select(self.elem).select_by_visible_text(value)

    @timethis
    def send_keys(self,text,isclear=True):
        '''
        向文本框发送文本
        ARGS:
            * ISCLEAR [bool] 发送文本前，是否清空输入框
        '''
        print("SEND KEYS : {}".format(text),end = ' ')
        self.elem.click()
        if isclear:
            self.driver.execute_script("arguments[0].value = '';", self.elem)
        self.elem.send_keys(text)

    @timethis
    def check(self,ischeck=True):
        '''
        勾选/反选 raido/checkbox 元素
        ARGS:
            * ISCHECK [bool] 勾选/反选被选中的元素
                * True  勾选被选中的元素 [default]
                * False 反选被选中的元素
        '''

        if ischeck:
            print("CHECK ELEM",end = ' ')
            if not self.elem.is_selected():
                self.elem.click()
        else:
            print("UNCHECK ELEM",end = ' ')
            if self.elem.is_selected():
                self.elem.click()

    @timethis
    def click(self):
        """
        点击一个元素
        """
        print('CLICK ELEM',end = ' ')
        for i in range(30):
            try:
                self.elem.click()
                # allure.attach(self.driver.get_screenshot_as_png(), name="点击元素", attachment_type=AttachmentType.PNG)
                return True
            except Exception as e:
                print(e)
            time.sleep(1)
        raise Exception("CAN'T CLICK")

    def scroll(self,method):
        """
        ARGS:
            *  METHOD
                * pageup 向上一页滚动
                * pagedown 向下一页滚动
        """
        scroll_elem = self.driver.run_js("get_scroll_elem(arguments[0])",self.elem,script="scroll.js")

        if method == "pageup":
            scroll_elem.send_keys(Keys.PAGE_UP)
        if method == "pagedown":
            scroll_elem.send_keys(Keys.PAGE_DOWN)
    @property
    def value(self):
        return self.elem.get_attribute("value")
        
    @property
    def src(self):
        return self.elem.get_attribute("src")