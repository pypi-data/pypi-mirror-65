import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.keys import Keys
from .common import Logger,data,Singleton,timethis
from .element import WebElement
from browsermobproxy import Server

class WebDriver():

    def __init__(self,proxy_ip=None,headless=None,debug=None,mobile=None,imagesless=None,user_data=None,cache=True,remote_server="127.0.0.1:4444"):

        self.logger = Logger("pywebdriver")

        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36')
        # self.start_server()
        if proxy_ip:
            options.add_argument('--proxy-server={0}'.format(proxy_ip))
        if headless:
            options.add_argument("--headless")
        if debug:
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        else:
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
        if mobile:
            # "Nexus 5"
            # 'iPhone 6'
            options.add_experimental_option("mobileEmulation", {'deviceName':mobile })
        if user_data:
            print("ok")
            user_data = "/Users/liyunpeng/Library/Application Support/Google/Chrome/Profile 10"
            options.add_argument('--user-data-dir="{}"'.format(user_data))
        if cache:
            cache = "~/Library/Application\ Support/Google/Chrome/Default/Application\ Cache"
            options.add_argument('--disk-cache-dir="{}"'.format(user_data))
        if imagesless:
            prefs = {
                'profile.default_content_setting_values': {
                    'images': 2
                }
            }
            options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Remote(command_executor='http://{}/wd/hub'.format(remote_server),
            desired_capabilities=DesiredCapabilities.CHROME,
            options=options)
        self.driver.run_js = self.run_js
        # add method
        self.get_screenshot_as_png = self.driver.get_screenshot_as_png
        self.save_screenshot = self.driver.save_screenshot
        self.refresh = self.driver.refresh
    def run_js(self,func,*args,script="query.js"):
        """
        调用avascript文件内的函数
        ARGS:
            * func: 需要调用的函数（含参数）
            * args: 要传入js的参数
            * scrip: 脚本文件名称

        USAGE:
            * self.run_js("query_by_locator('text','left')")
            * self.run_js("get_scroll_elem(arguments[0])",elem,script="scroll.js")
        """
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"javascript",script)

        with open(script_path,'r',encoding='UTF-8') as f:
            js = f.read() + '\n\n\n' + 'return ' + func

        return self.driver.execute_script(js,*args)

    @timethis
    def query(self,innerText=None,locator=None,locator_text=None,css=None,parts=None,timeout=30,index=0,exit=True,**kwargs):
        '''
        返回选中的元素，并保存选中的元素到self.elem
        ARGS:
            * INNERTEXT 要定位的元素的文字
            * EXIT 没有找到元素后是否退出
                * True: 退出并报错
                * False: 不退出并return False
        '''
        def query_elem(innerText,css):
            if locator:
                if parts:
                    elem_list = self.run_js("query_by_part_of_locator('{}','{}')".format(innerText,locator))
                else:
                    if locator_text == None:
                        elem_list = self.run_js("query_by_locator('{}','{}')".format(innerText,locator))
                    else:
                        elem_list = self.run_js("query_by_locator('{}','{}','{}')".format(innerText,locator,locator_text))
            elif parts:
                elem_list = self.run_js("query_by_parts_of_innerText('{0}')".format(innerText))
            elif innerText:
                elem_list = self.run_js("query_by_innerText('{0}')".format(innerText))
            elif css:
                elem_list = self.run_js("query_by_css('{0}')".format(css))
            # 属性选择器
            else:
                key = [*kwargs][0]
                elem_list = self.run_js("query_by_css('[{} = {}]')".format(key,kwargs[key]))
                self.prop_msg = '{} = {}'.format(key,kwargs[key])
            return elem_list

        start_time = time.time()
        end_time = time.time()

        while (end_time - start_time) < timeout:
            elem_list = []
            elem_list += query_elem(innerText,css)
            if elem_list:
                print('FOUND ELEM ' + (innerText or css or self.prop_msg),end = "   ")
                self.logger.debug('FOUND ELEM ' + (innerText or css or self.prop_msg))
                return WebElement(elem_list[index],self.driver)
            end_time = time.time()
            time.sleep(1)
        if exit:
            self.driver.save_screenshot('ERROR.png')
            error_msg = 'can not find Element {} in {} s'.format(innerText or css or parts,timeout)
            self.logger.error('ERROR: ' + error_msg)
            raise Exception(error_msg)
        else:
            return False


    def query_not(self,*args,**kwargs):
        try:
            self.query(*args,timeout = 1,**kwargs)
        except Exception as e:
            self.logger.info("ELEM NOT FOUND : PASS")
            return True
        else:
            raise Exception("ELEM FOUND ERROR")

    @timethis
    def query_part(self,innerText = None,locator = None,timeout = 60,index = 0):
        '''
        select elems by part of innertText
        '''
        return self.query(innerText = innerText,locator = locator,parts = True,timeout = timeout,index = index)


    def diff(self,data = None):
        # 获取页面是否发生了变化，返回 None 或者 一个字典
        if not data:
            result = self.run_js("getElementStyleMD5()")
        else:
            result = self.run_js("getDiffElement('{}')".format(data))

        if not result:
            return None
        else:
            return json.loads(result)

    def get(self,url):
        self.logger.info("GET URL: " + url)
        self.driver.get(url)

    def quit(self):
        self.logger.info("BROWSER CLOSE")
        data.is_quit = True
        # self.server.stop()
        # ps -ef|grep browsermob|grep -v grep|awk '{print $2}'|xargs kill -9
        self.driver.quit()

    def sleep(self,sleep_time):
        self.logger.info("BROWSER SLEEP: " + str(sleep_time))
        time.sleep(sleep_time)

    def open(self,url):
        self.logger.info("OPEN NEW TAP: " + url)
        script = 'window.open("{}")'.format(url)
        self.driver.execute_script(script)
        #移动句柄，对新打开页面进行操作
        # self.driver.switch_to_window(driver.window_handles[1])
        # #具体操作
        # driver.find_element_by_xpath("")
        # #关闭该新打开的页面
        # driver.close()
        # #不关闭，要移动到上一个页面，我们要移动句柄
        # driver.switch_to_window(driver.window_handles[0])
    def switch(self,index):
        self.driver.switch_to_window(self.driver.window_handles[index])

    def delete_all_cookies(self):
        self.logger.info("CLEAR ALL COOKIES")
        self.driver.delete_all_cookies()

    def start_server(self):
        basedir = os.path.dirname(os.path.abspath(__file__))
        server_path = os.path.join(basedir,"bin","browsermob-proxy-2.1.4","bin","browsermob-proxy")
        self.server = Server(server_path)
        self.server.start()
        self.proxy = self.server.create_proxy()
        self.proxy.new_har('req',options={'captureHeaders': True, 'captureContent': True, 'captureBinaryContent': True})
        self.logger.info("PROXY START :" + self.proxy.proxy)

    def get_response(self):
        self.proxy.wait_for_traffic_to_stop(1, 60)
        result = self.proxy.har
        return result['log']['entries']
        # for entry in result['log']['entries']:
        #     url = entry['request']['url']
        #     if "thor" in url:
        #         response = entry['response']
        #         print(url)
        #         print(response)
    def accept(self):
        alert = self.driver.switch_to_alert()
        alert.accept()





