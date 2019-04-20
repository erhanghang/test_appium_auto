# -*- encoding:utf8 -*- 
''' 
@author: PGQ
@version: 2016-12-22 
@comment: 
'''
# -*- coding: utf-8 -*-
# appium --no-reset --log-timestamp --session-override --command-timeout 300
from appium import webdriver

# 引入刚刚创建的同目录下的desired_capabilities.py
import desired_capabilities

# 我们使用python的unittest作为单元测试工具
from unittest import TestCase

# 我们使用python的unittest作为单元测试工具
import unittest

# 使用time.sleep(xx)函数进行等待
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MqcTest(TestCase):
    global uri
    global desired_caps

    def setUp(self):
        # 获取我们设定的capabilities，通知Appium Server创建相应的会话。
        self.desired_caps = desired_capabilities.get_desired_capabilities()
        # 获取server的地址。
        self.uri = desired_capabilities.get_uri()

    def test_aixuexi(self):
        # 获取用户名和密码
        user = desired_capabilities.getParam("username")
        passwd = desired_capabilities.getParam("password")

        boolFlag1=True
        boolLoginFlag1 = False
        intFlag1=0
        chromedriver = ['2.33', '2.30', '2.28', '2.24', '2.23', '2.22', '2.20', '2.18', '2.16', '2.14']

        print("登录用户%s" % user)
        while boolFlag1:
            try:
                # 创建会话，得到driver对象，driver对象封装了所有的设备操作。下面会具体讲。
                self.desired_caps['recreateChromeDriverSessions'] = True
                self.driver = webdriver.Remote(self.uri, self.desired_caps)
                self.driver.implicitly_wait(15)
                time.sleep(5)
                if not boolLoginFlag1:
                    time.sleep(8)
                    self.driver.find_element_by_id("gaosi.com.learn:id/tv_login_phone").send_keys(user)
                    #self.driver.find_element_by_id("gaosi.com.learn:id/tv_login_phone").click()
                    self.driver.find_element_by_id("gaosi.com.learn:id/tv_login_pwd").send_keys(passwd)
                    #self.driver.find_element_by_id("gaosi.com.learn:id/tv_login_pwd").click()
                    time.sleep(2)
                    self.driver.find_element_by_id("gaosi.com.learn:id/btn_login").click()
                    boolLoginFlag1=True
                time.sleep(20)
                intCount = 0
                while intCount < 10:
                    time.sleep(1)
                    intCount = intCount + 1
                    contexts = self.driver.contexts
                    print(contexts)
                    if u'WEBVIEW_gaosi.com.learn' in contexts:
                        print("adfasd")
                        break
                self.driver.switch_to.context('WEBVIEW_gaosi.com.learn')
                self.driver.switch_to.default_content()
                #self.driver.switch_to.context(contexts[1])
                print(self.driver.current_context)
                boolFlag1 = False
            except ZeroDivisionError:
                self.driver.quit()
                boolLoginFlag1=True
                print("ZeroDivision")
                self.desired_caps['chromedriverExecutable'] = '/usr/lib/node_modules/appium/node_modules/appium-chromedriver/chromedriver/linux/chromedriver_64_'+chromedriver[intFlag1]
                # self.desired_caps['chromedriverExecutable'] = 'C:\\Users\\hp\\AppData\\Roaming\\npm\\node_modules\\appium\\build\\chromedriver\\windows\\chromedriver'+chromedriver[intFlag1]+'.exe'
                if boolLoginFlag1:
                    self.desired_caps['appWaitActivity'] = '.studentapp.main.MainActivity'
                print("chromedriver版本：%s" % chromedriver[intFlag1])
                intFlag1=intFlag1+1
                if intFlag1==len(chromedriver):
                    self.assertFalse(boolFlag1, "没有找到webview!")
                    break
                continue

            #**************************************登录学生端**************************************
            # self.switchUrl(self.driver,"loginstaticHtml.html")
            # time.sleep(2)
            # print "++++++++++++++开始登录++++++++++++++++++"
            # self.waitForclick(self.driver,"//a[contains(text(),'收不到验证码？使用账号密码登录')]")
            # time.sleep(3)
            # self.waitForInputAndClick(self.driver,"(//input[@placeholder='报名时登记的手机号'])[2]",user)
            # self.waitForInputAndClick(self.driver,"//input[@placeholder='请输入密码']",passwd)
            # element=self.driver.find_element_by_xpath("//button[@class='mint-button mint-button--primary mint-button--large']")
            # self.driver.execute_script("arguments[0].removeAttribute('disabled')",element)
            # element.click()

            # **************************************登录学生端**************************************
        self.switchUrl(self.driver,"indexstaticHtml.html")
        time.sleep(2)
        print("++++++++++++++开始答题++++++++++++++++++")
        self.waitForclickpass(self.driver, "//button[text()='关闭']")
        time.sleep(3)
        self.waitForclickpass(self.driver,"//div[@class='todo-work']")
        time.sleep(6)
        self.switchUrl(self.driver,"homeworkstaticHtml.html")
        time.sleep(2)
        self.waitForclick(self.driver,"(//div[@class='modules-class-time'])[1]") #选课节
        time.sleep(3)
        self.waitForclick(self.driver,"//label[text()='开始交作业']/parent::button")
        time.sleep(5)
        self.switchUrl(self.driver,"zuoyestaticHtml.html")
        time.sleep(2)
        blankcontent = 1
        strflag=False
        while True:
            #填空题
            blanks=self.driver.find_elements_by_xpath("//input[@class='blanks-answer' and @data-node='blankAnswer']")
            if len(blanks)>0:
                for blank in blanks:
                    if blank.get_attribute('style') != "display: none;":
                        #blank.send_keys(blankcontent)
                        self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", blank,blankcontent)
                        # self.driver.execute_script("arguments[0].innerHTML=arguments[1]", element, '18700000107')
                        blank.click()
                        blankcontent=blankcontent+1
            #判断题
            selections = self.driver.find_elements_by_xpath("//div[@class='select']")
            if len(selections) > 0:
                for selection in selections:
                    if selection.find_element_by_xpath("../../../..").get_attribute('style').find('overflow: hidden;')==-1:
                        selection.find_element_by_xpath("//label[1]").click()
            #选择题
            options = self.driver.find_elements_by_xpath("//li[@class='single']")
            if len(options) > 0:
                for option in options:
                    if option.find_element_by_xpath("../../..").get_attribute('style').find(
                            'overflow: hidden;') == -1:
                        option.click()
                        break
            #主观题-拍照i
            answers = self.driver.find_elements_by_xpath("//img[@class='unanswer']")
            if len(answers) > 0:
                for answer in answers:
                    if answer.find_element_by_xpath("../../../..").get_attribute('style').find('overflow: hidden;')==-1:
                        answer.click()
                        time.sleep(1)
                        answer.find_element_by_xpath("../following-sibling::div[1]/a").click()
            time.sleep(2)
            self.waitForclick(self.driver,"//div[@class='modules-homework-pageUpDown-down']")  # 下一题目
            if strflag:
                break
            time.sleep(2)
            if self.driver.find_element_by_xpath("//div[@class='modules-homework-pageUpDown-down']/span[1]").text=="完成":
                strflag=True
        time.sleep(5)
        self.switchUrl(self.driver,"anscardstaticHtml.html")
        time.sleep(2)
        print("++++++++++++++开始提交作业++++++++++++++++++")
        self.waitForclick(self.driver,"//button[@class='mint-button score-submit mint-button--primary mint-button--large']") #提交作业
        time.sleep(6)
        contexts = self.driver.contexts
        print(contexts)
        self.driver.switch_to.context('NATIVE_APP')
        time.sleep(2)
        self.driver.find_element_by_id("android:id/button1").click()
        # time.sleep(8)
        # self.waitForclick(self.driver,"//button[@class='msgbox-btn msgbox-confirm ']")
        time.sleep(8)
        view = self.driver.find_elements_by_accessibility_id("习惯是很大的力量哦，要坚持！")
        if len(view) > 0:
            self.driver.find_element_by_accessibility_id("习惯是很大的力量哦，要坚持！").click()
        time.sleep(5)
        view = self.driver.find_elements_by_accessibility_id("每答对1题得3个金币")
        if len(view) > 0:
            self.driver.find_element_by_accessibility_id("每答对1题得3个金币").click()
        time.sleep(6)
        contexts = self.driver.contexts
        print(contexts)
        # os.system('taskkill /F /im chromedriver.exe')
        print(self.driver.current_context)
        time.sleep(15)
        self.driver.switch_to.context('WEBVIEW_gaosi.com.learn')
        time.sleep(2)
        contexts = self.driver.contexts
        print(contexts)
        print(self.driver.current_context)
        self.switchUrl(self.driver, "scorestaticHtml.html")
        time.sleep(5)
        #self.waitForclick(self.driver, "//div[@class='score-container']")
        #time.sleep(10)
        #self.waitForclick(self.driver, "//div[@class='modules-glod-img modules-bg1']")
        #time.sleep(5)
        self.waitForclick(self.driver,"//button[@class='mint-button score-submit error-question mint-button--primary mint-button--large']") #去订正
        time.sleep(5)
        print("去订正")
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(2)
        self.waitForclick(self.driver,"//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        # 第一题
        print("开始订正第1题")
        self.switchUrl(self.driver, "correctProstaticHtml.html") #订正页面
        time.sleep(2)
        self.waitForOptionsClick(self.driver, "//li[@class='single']", 1)
        self.waitForclick(self.driver,"//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        #第二题
        print("开始订正第2题")
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(2)
        self.waitForclick(self.driver,"//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        self.switchUrl(self.driver, "correctProstaticHtml.html")
        time.sleep(2)
        self.waitForOptionsClick(self.driver, "//li[@class='single']", 0)
        self.waitForOptionsClick(self.driver, "//li[@class='single']", 2)
        self.waitForclick(self.driver,"//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        # 第三题
        print("开始订正第3题")
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(2)
        self.waitForclick(self.driver,
                          "//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        self.switchUrl(self.driver, "correctProstaticHtml.html")
        time.sleep(2)
        self.waitForDoubleInputAndClick(self.driver, "//input[@class='blanks-answer' and @data-node='blankAnswer']",
                                        "40", "50")
        self.waitForclick(self.driver,
                          "//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        # 第四题
        print("开始订正第4题")
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(2)
        self.waitForclick(self.driver,
                          "//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        self.switchUrl(self.driver, "correctProstaticHtml.html")
        time.sleep(2)
        self.waitForOptionsClick(self.driver, "//label[@class='default right']", 0)
        self.waitForOptionsClick(self.driver, "//label[@class='default wrong']", 1)
        self.waitForOptionsClick(self.driver, "//label[@class='default wrong']", 1)
        self.waitForOptionsClick(self.driver, "//label[@class='default wrong']", 1)
        self.waitForOptionsClick(self.driver, "//label[@class='default wrong']", 1)
        self.waitForOptionsClick(self.driver, "//label[@class='default right']", 4)
        self.waitForclick(self.driver,"//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        # 第五题
        print("开始订正第5题")
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(2)
        self.waitForclick(self.driver,
                          "//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        self.switchUrl(self.driver, "correctProstaticHtml.html")
        time.sleep(2)
        self.waitForOptionsClick(self.driver, "//li[@class='single']", 0)
        self.waitForOptionsClick(self.driver, "//li[@class='single']", 0)
        self.waitForclick(self.driver,
                          "//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        # 第六题
        print("开始订正第6题")
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(2)
        self.waitForclick(self.driver,
                          "//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        self.switchUrl(self.driver, "correctProstaticHtml.html")
        time.sleep(2)
        self.waitForOptionsClick(self.driver, "//li[@class='single']", 0)
        self.waitForclick(self.driver,
                          "//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        # # 第七题
        # print "开始订正第7题"
        # self.switchUrl(self.driver, "correctionstaticHtml.html")
        # time.sleep(2)
        # self.waitForclick(self.driver,
        #                   "//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        # self.switchUrl(self.driver, "correctProstaticHtml.html")
        # time.sleep(2)
        # self.waitForDoubleInputAndClick(self.driver,"//input[@class='blanks-answer' and @data-node='blankAnswer']","草盛豆苗稀","带月荷锄归")
        # self.waitForclick(self.driver,
        #                   "//button[@class='mint-button score-submit mint-button--primary mint-button--large']")
        print("结束订正并返回")
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        self.waitForclick(self.driver,"//span[@class='mint-button-icon']")
        time.sleep(2)
        self.switchUrl(self.driver, "scorestaticHtml.html")
        time.sleep(2)
        self.waitForclick(self.driver, "//span[@class='mint-button-icon']")
        time.sleep(2)
        self.switchUrl(self.driver,"indexstaticHtml.html")
        time.sleep(2)
        self.waitForclickpass(self.driver,"//button[text()='关闭']")
        time.sleep(3)
        self.switchUrl(self.driver,"minestaticHtml.html")
        time.sleep(2)
        print("++++++++++++++开始退出++++++++++++++++++")
        self.waitForclick(self.driver,"//div[@class='mine-setting']")#设置
        time.sleep(2)
        self.switchUrl(self.driver,"settingstaticHtml.html")
        time.sleep(2)
        self.waitForclick(self.driver,"//button[@class='mint-button mint-button--danger mint-button--large']") #退出登录
        time.sleep(3)
        self.driver.switch_to.context('NATIVE_APP')
        time.sleep(2)
        self.driver.find_element_by_id("android:id/button1").click()

        # time.sleep(5)
        # self.waitForclick(self.driver, "//button[@class='msgbox-btn msgbox-confirm ']")
        time.sleep(2)

    def tearDown(self):
        # 测试结束，退出会话。
        self.driver.quit()

    def switchUrl(self,driver,suburl):
        intCount=0
        while  intCount<10:
            try:
                time.sleep(5)
                intCount = intCount + 1
                print("窗口%s ，第%s次切换" % (suburl, str(intCount)))
                all_handles = driver.window_handles
                for handle in all_handles:
                    driver.switch_to_window(handle)
                    if driver.current_url.find(suburl)>-1:
                        intCount=10
                        break
            except:
                continue

    def  waitFor(self,xpath,times):
        for num in range(1,times):
            try:
                time.sleep(1)
                self.driver.find_element_by_xpath(xpath)
                return True
            except:
                print("没有找到 %s" % xpath)
                return False

    def  waitForclick(self,driver,xpath):
        try:
            element = WebDriverWait(self.driver, 30, 1).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))
            element.click()
            time.sleep(2)
        except:
            self.driver.quit()

    def  waitForDisplayclick(self,driver,xpath):
        try:
            element = WebDriverWait(self.driver, 30, 1).until(EC.visibility_of_element_located(
                (By.XPATH, xpath)))
            time.sleep(2)
            element.click()
            time.sleep(2)
        except:
            self.driver.quit()

    def  waitForInputAndClick(self,driver,xpath,strcontent):
        try:
            element = WebDriverWait(self.driver, 30, 1).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, strcontent)
            time.sleep(1)
            element.click()
            time.sleep(2)
        except:
            self.driver.quit()

    def  waitForDoubleInputAndClick(self,driver,xpath,strcontent1,strcontent2):
        try:
            elements = WebDriverWait(self.driver, 30, 1).until(EC.presence_of_all_elements_located(
                (By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", elements[0], strcontent1)
            time.sleep(1)
            elements[0].click()
            time.sleep(2)
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", elements[1], strcontent2)
            time.sleep(1)
            elements[1].click()
            time.sleep(2)
        except:
            self.driver.quit()

    def  waitForOptionsClick(self,driver,xpath,i):
        try:
            elements = WebDriverWait(self.driver, 30, 1).until(EC.presence_of_all_elements_located(
                    (By.XPATH, xpath)))
            #print len(elements)
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(false)", elements[i])
                time.sleep(2)
                elements[i].click()
            except:
                self.driver.execute_script("arguments[0].scrollIntoView(true)", elements[i])
                time.sleep(2)
                elements[i].click()
            time.sleep(2)
        except:
            self.driver.quit()

    def waitForclick_old(self, driver, xpath):
        for num in range(1,20):
            elments=driver.find_elements_by_xpath(xpath)
            if len(elments)>0:
                time.sleep(3)
                driver.find_element_by_xpath(xpath).click()
                break
            print("等待第%s次" % str(num))
            if num==19:
                print("没有找到 %s" % xpath)
                driver.find_element_by_xpath(xpath).click()

    def  waitForclickpass(self,driver,xpath):
        for num in range(1,3):
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

    def tapScreen(self,x,y):
        screen_width_case_phone=1080
        screen_height_case_phone=1920
        screen_width_execute_phone = self.driver.get_window_size()['width'] #screen width
        screen_height_execute_phone = self.driver.get_window_size()['height'] #screen height
        x_click = x * screen_width_execute_phone / screen_width_case_phone # x coordinates on execute phone
        y_click = y * screen_height_execute_phone / screen_height_case_phone # y coordinates on execute phone
        self.driver.tap([(x_click, y_click), ])
        time.sleep(2)

    def swipeToDown(self):
        screen_width_execute_phone = self.driver.get_window_size()['width'] #screen width
        screen_height_execute_phone = self.driver.get_window_size()['height'] #screen height
        Startpoint = screen_height_execute_phone * 0.25
        scrollEnd = screen_height_execute_phone * 0.75
        self.driver.swipe(300, Startpoint, 300, scrollEnd, 2000)



    def scrollDownToFind(self,xpath):
        while not (self.driver.find_element_by_xpath(xpath).isDisplayed()):
            self.swipeToDown()


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass