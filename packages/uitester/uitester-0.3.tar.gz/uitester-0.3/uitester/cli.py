import os
import fire
import time


class UiTester(object):

    def start(self,filename = None):
        os.system("pytest --alluredir=report/result " + filename)
        # os.system("allure generate report/xml -o report/html --clean")
        os.system("allure serve report/result")

    def server(self,order):
        if order == "start":
            os.system("selenium-standalone start")
        if order == "install":
            install_standalone = "sudo npm install selenium-standalone@latest -g --registry=https://registry.npm.taobao.org"
            install_dirver = "sudo selenium-standalone install --drivers.firefox.baseURL=http://npm.taobao.org/mirrors/geckodriver --baseURL=http://npm.taobao.org/mirrors/selenium --drivers.chrome.baseURL=http://npm.taobao.org/mirrors/chromedriver --drivers.ie.baseURL=http://npm.taobao.org/mirrors/selenium"
            os.system(install_standalone + " && " + install_dirver)

def cli():
    fire.Fire(UiTester)