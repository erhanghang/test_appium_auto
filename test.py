# -*- encoding:utf8 -*-
'''
@author: PGQ
@version: 2018-05-28
@comment:
'''
# appium --no-reset --log-timestamp --session-override --command-timeout 300
from appium import webdriver

# 引入刚刚创建的同目录下的desired_capabilities.py
from selenium.webdriver.common.by import By

import desired_capabilities

# 我们使用python的unittest作为单元测试工具
from unittest import TestCase

# 我们使用python的unittest作为单元测试工具
import unittest

# 使用time.sleep(xx)函数进行等待
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.switch_to import MobileCommand
from selenium.common.exceptions import NoSuchElementException

class MqcTest(TestCase):
    global uri
    global desired_caps

    def setUp(self):
        # 获取我们设定的capabilities，通知Appium Server创建相应的会话。
        self.desired_caps = desired_capabilities.get_desired_capabilities()
        # 获取server的地址。
        self.uri = desired_capabilities.get_uri()
        self.timeout = 30

    def test_aixuexi_student(self):
        '''测试学生端学生进行作业提交与作业订正'''
         # 获取用户名和密码
        user = desired_capabilities.getParam("username")
        passwd = desired_capabilities.getParam("password")


        print "登录用户%s" % user
        # 创建会话，得到driver对象，driver对象封装了所有的设备操作。下面会具体讲。
        self.desired_caps['recreateChromeDriverSessions'] = True
        self.driver = webdriver.Remote(self.uri, self.desired_caps)
        self.driver.implicitly_wait(1)
        #判断课节元素是否存在，存在则绕过登录点击课节，不存在则登录（兼容某些手机在第一次登录失败，重启app不再登录的问题）
        boolLoginFlag1 = self.isElementExist(('xpath', '//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.TextView'))
        if not boolLoginFlag1:
            print('**************************************登录学生端**************************************')
            # #登录前操作  权限允许
            # self.is_element_exist_and_click(('id', 'android:id/button1'))
            time.sleep(3)
            time.sleep(2)
            self.sendkeys_text(('id', 'gaosi.com.learn:id/edt_phone'), user)
            self.sendkeys_text(('id', 'gaosi.com.learn:id/edt_pass'), passwd)
            time.sleep(2)
            self.waitForclick(("id", "gaosi.com.learn:id/btn_login"))  #点击登录
            time.sleep(5)
            #登录成功后存在弹窗修改密码，暂不修改（随账号，只出现一次）
            self.is_element_exist_and_click(("id", "gaosi.com.learn:id/tv_cancel"))
            # #登录成功后存在弹窗作业宝箱，点击 X 关闭（随账号，只出现一次）
            self.is_element_exist_and_click(("id", "gaosi.com.learn:id/ibBack"))
            #登录后存在个人装扮功能弹窗，点击X关闭（只要不选择性别，就一直会弹窗）
            self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/ibBack2'))
            print('**************************************登录成功**************************************')
        print("++++++++++++++开始测试装扮流程++++++++++++++++++")
        time.sleep(5)
        self.tapScreen(800, 300)#点击头像
        try:
            print(u'头像坐标')
            self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/llMan'))#第一次使用选择男女
            self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/tvComfirm'))#确定
            time.sleep(5)
            self.driver.find_element_by_android_uiautomator('new UiSelector().className("android.widget.TextView").text("抽取装扮")').click()
        except:
            self.tapScreen(810, 1830)#点击我的
            print(u'我的坐标')
            self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/llMan'))#第一次使用选择男女
            self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/tvComfirm'))#确定
            time.sleep(5)
            self.waitForclick(('android uiautomator', 'new UiSelector().className("android.widget.TextView").text("抽取装扮")'))
        time.sleep(5)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print("切换成功")
        self.switchUrl(self.driver, "extractingstaticHtml.html")
        time.sleep(2)
        if self.isElementExist(('xpath', "//div[@class=\"extractChooseBtn\"][text()='免费召唤UFO']")):
            self.waitForclick(('xpath', "//div[@class=\"extractChooseBtn\"][text()='免费召唤UFO']"))
        else:
            self.waitForclick(('xpath', "//i[contains(text(),'召唤UFO')]"))
        time.sleep(10)
        self.click_element_or_coordinate(('xpath', '//button[@class="notSave"]'), 540, 1340)
        time.sleep(3)
        self.switchUrl(self.driver, "dressSelfstaticHtml.html")
        time.sleep(8)
        if self.isElementExist(('xpath', "//span[text()='new']/parent::div")):
            self.scrollToFind(('xpath', "//span[text()='new']/parent::div"))
            self.waitForclick(('xpath', "//span[text()='new']/parent::div"))#点击刚刚获取的装扮
        else:
            elements = self.findelements(('xpath', '//div[@class="dressDetail"]/div[@class="innerDress"]'))
            elements[0].click()
        time.sleep(2)
        self.waitForclick(('xpath', "//div[text()='保存装扮']"))
        # result = self.get_Toast(u'装扮保存成功')
        # self.assertTrue(result)
        print("++++++++++++++测试完成++++++++++++++++++")


    def tearDown(self):
        '''退出登录'''
        # self.driver.delete_all_cookies()
        # self.driver.quit()
        pass


    #封装方法
    def findelement(self, locator):
        '''显式等待元素，单个元素'''
        if locator[0] == 'accessibility id':
            element = WebDriverWait(self.driver, self.timeout, 1).until(lambda x: x.find_element_by_accessibility_id(locator[1]))
            return element
        elif locator[0] == 'android uiautomator':
            element = WebDriverWait(self.driver, self.timeout, 1).until(lambda x: x.find_element_by_android_uiautomator(locator[1]))
            return element
        else:
            element = WebDriverWait(self.driver, self.timeout, 1).until(EC.presence_of_element_located(locator))
            return element

    def findelements(self, locator):
        '''复数定位'''
        if locator[0] == 'accessibility id':
            elements = WebDriverWait(self.driver, self.timeout, 1).until(lambda x: x.find_elements_by_accessibility_id(locator[1]))
            return elements
        elif locator[0] == 'android uiautomator':
            elements = WebDriverWait(self.driver, self.timeout, 1).until(lambda x: x.find_elements_by_android_uiautomator(locator[1]))
            return elements
        else:
            elements = WebDriverWait(self.driver, self.timeout, 1).until(EC.presence_of_all_elements_located(locator))
            return elements

    def switchUrl(self, driver, suburl):
        '''切换handle'''
        intCount=0
        while  intCount < 10:
            try:
                time.sleep(2)
                intCount = intCount + 1
                print("窗口%s ，第%s次切换" % (suburl, str(intCount)))
                all_handles = driver.window_handles
                for handle in all_handles:
                    driver.switch_to_window(handle)
                    if driver.current_url.find(suburl)>-1:
                        intCount=10
                        break
            except:
                time.sleep(2)
                self.driver.refresh()
                continue

    def  waitForclick(self, locator):
        '''显式等待元素出现后进行点击操作，传入locator的格式（'xpath','....'）定位方式可以使用id、name、xpath、css....'''
        element = self.findelement(locator)
        element.click()

    def sendkeys_text(self, locator, text):
        '''输入框输入文本'''
        element = self.findelement(locator)
        element.send_keys(text)

    def is_element_exist_and_click(self, locator, timeout=8):
        '''判断元素是否存在，存在点击，不存在则进行下一步操作'''
        try:
            element = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
            element.click()
        except:
            pass

    def click_element_or_coordinate(self, locator, x, y):
        '''判断元素是否存在，不存在则点击其坐标'''
        if self.isElementExist(locator):
            self.waitForclick(locator)
        else:
            print(u'元素%s未找到'%locator[1])
            self.switch_native()
            time.sleep(2)
            self.tapScreen(x, y)#点击坐标
            time.sleep(5)
            self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
            print("切换成功")

    def isElementExist(self, locator):
        '''判断单个元素是否存在，返回布尔值'''
        try:
            time.sleep(5)
            if locator[0] == 'id':
                self.driver.find_element_by_id(locator[1])
            elif locator[0] == 'class name':
                self.driver.find_element_by_class_name(locator[1])
            elif locator[0] == 'css selector':
                self.driver.find_element_by_css_selector(locator[1])
            elif locator[0] == 'xpath':
                self.driver.find_element_by_xpath(locator[1])
            elif locator[0] == 'accessibility id':
                self.driver.find_element_by_accessibility_id(locator[1])
            return True
        except NoSuchElementException:
            return False

    def get_text(self, locator):
        '''获取元素的text'''
        element = self.findelement(locator)
        return element.text

    def getattribute(self, locator, attr):
        '''获取元素属性值'''
        element = self.findelement(locator)
        return element.get_attribute(attr)

    def get_Toast(self, text):  #查找toast值
        '''获取toast弹窗内容'''
        try:
           toast_loc = ("xpath", "//*[contains(@text,'%s')]" % text)
           WebDriverWait(self.driver, 5, 0.2).until(EC.presence_of_element_located(toast_loc))
           return True
        except:
            print(u'页面没有包含%s'%text)
            return False

    def find_toast(self, message):
        '''判断toast信息'''
        try:
            WebDriverWait(self.driver, 5, 0.1).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, message)))
            return True
        except:
            return False

    def andriod_key(self, num=4):
        '''安卓手机的一般操作，如拨号键，挂机键、返回键、菜单键.....
        num=4时，为返回键
        '''
        self.driver.press_keycode(num)

    def switch_h5(self, webview):
        '''切换webview页面'''
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": webview})

    def switch_native(self):
        '''切换app原生页面'''
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "NATIVE_APP"})
        time.sleep(2)

    def scrollToFind(self, locator):
        '''滑动页面到指定的元素上，出现在页面最底端'''
        target = self.findelement(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def __clean_text(self, text):
        '''清空文本框方法的封装'''
        self.driver.keyevent(123)    #123代表光标移动到末尾键
        for i in range(0, len(text)):
            self.driver.keyevent(67)       #67退格键

    def __find_ele(self, locator):
        '''获取到要删除的文本框内容'''
        find_ele =self.findelement(locator)
        find_ele.click()
        return find_ele.get_attribute('text')

    def clear(self,locator):
        '''删除文本框内容'''
        get_text = self.__find_ele(locator)
        self.__clean_text(get_text)

    def get_screen_size(self):
        '''屏幕滑动'''
        x=self.driver.get_window_size()["width"]
        y=self.driver.get_window_size()["height"]
        return (x,y)

    def swipe_up(self, t=500):
        '''向上滑动  从屏幕的下端点击一个坐标然后往上滑动，x坐标可以不变。Y的开始和结束坐标改进即可'''
        screen = self.get_screen_size()
        self.driver.swipe(screen[0]*0.5, screen[1]*0.75, screen[0]*0.5, screen[1]*0.25, t)

    def swipe_down(self, t=500):
        '''向下滑动  从屏幕的上端点击一个坐标然后往下滑动，x坐标可以不变。Y的开始和结束坐标改变即可'''
        screen = self.get_screen_size()
        self.driver.swipe(screen[0]*0.5, screen[1]*0.25, screen[0]*0.5, screen[1]*0.75, t)

    def swipe_left(self, t=500):
        '''向左滑动  从屏幕的右端点击一个坐标点往左滑动。Y坐标可以不改变。X的开始和结束坐标改变即可'''
        screen = self.get_screen_size()
        self.driver.swipe(screen[0]*0.75, screen[1]*0.5, screen[0]*0.25, screen[1]*0.5, t)

    def swipe_right(self, t=500):
        '''向右滑动  从屏幕的左端点击一个坐标点然后往后滑动.Y坐标可以不变。X的开始和结束坐标改变即可'''
        screen = self.get_screen_size()
        self.driver.swipe(screen[0]*0.25, screen[1]*0.5, screen[0]*0.75, screen[1]*0.5, t)

    # def accept_permissions(self, n=5):
    #     '''手机权限处理'''
    #     try:
    #         for i in range(n):
    #             time.sleep(2)
    #             if u'允许' or u'始终允许' or u'同意' or u'通过' in self.driver.page_source:
    #                 self.driver.switch_to.alert.accept()#接收弹窗
    #                 print("点击成功")
    #     except:
    #         pass

    def  waitForDisplayclick(self, locator):
        '''等待元素可见出现后进行点击'''
        try:
            element = WebDriverWait(self.driver, self.timeout, 1).until(EC.visibility_of_element_located((locator)))
            element.click()
        except:
            self.driver.quit()

    def  waitForInputAndClick(self, locator, strcontent):
        try:
            element = self.findelement(locator)
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, strcontent)
            time.sleep(1)
            element.click()
            time.sleep(2)
        except:
            self.driver.quit()

    def  waitForDoubleInputAndClick(self, locator, strcontent1, strcontent2):
        try:
            elements = self.findelements(locator)
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", elements[0], strcontent1)
            time.sleep(2)
            elements[0].click()
            time.sleep(2)
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", elements[1], strcontent2)
            time.sleep(1)
            elements[1].click()
            time.sleep(2)
        except:
            self.driver.quit()

    def  waitForOptionsClick(self, locator, i):
        try:
            elements = self.findelements(locator)
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(false);", elements[i])#元素出现在屏幕最上面
                time.sleep(2)
                elements[i].click()
            except:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", elements[i]) #元素出现在屏幕最下面
                time.sleep(2)
                elements[i].click()
            time.sleep(2)
        except:
            self.driver.quit()


    def  waitForclickpass(self,driver,xpath):
        for num in range(1, 3):
            try:
                elments=driver.find_elements_by_xpath(xpath)
                if len(elments)>0:
                    time.sleep(3)
                    driver.find_element_by_xpath(xpath).click()
                    break
                print("等待第%s次" % str(num))
                if num==19:
                    print("没有找到 %s" % xpath)
            except:
                continue

    def tapScreen(self, x, y):
        '''坐标定位,模拟点击坐标位置，需要先切回native'''
        screen_width_case_phone=1080
        screen_height_case_phone=1920
        screen_width_execute_phone = self.driver.get_window_size()['width'] #screen width
        screen_height_execute_phone = self.driver.get_window_size()['height'] #screen height
        x_click = x * screen_width_execute_phone / screen_width_case_phone # x coordinates on execute phone
        y_click = y * screen_height_execute_phone / screen_height_case_phone # y coordinates on execute phone
        self.driver.tap([(x_click, y_click), ])
        time.sleep(2)

    def taskKill(self,strTaskname='chromedriver.exe'):
        """结束进程"""
        command = "taskkill /F /IM "+strTaskname
        os.system(command)

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass