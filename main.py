# -*- encoding:utf8 -*-
'''
@author: PGQ
@version: 2018-05-28
@comment:           更新登录后切换chromedriver的方式，提高查找到合适的chromedriver效率 学生端自动化结构优化，用例间耦合性降低
'''
# appium --no-reset --log-timestamp --session-override --command-timeout 300
from appium import webdriver
from selenium.webdriver.common.by import By
# 引入刚刚创建的同目录下的desired_capabilities.py
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
import shutil


class MqcTest(TestCase):
    global uri
    global desired_caps

    def setUp(self):
        # 获取我们设定的capabilities，通知Appium Server创建相应的会话。
        self.desired_caps = desired_capabilities.get_desired_capabilities()
        # 获取server的地址。
        self.uri = desired_capabilities.get_uri()
        self.timeout = 10
         # 获取用户名和密码
        self.user = desired_capabilities.getParam("username")
        self.passwd = desired_capabilities.getParam("password")
        print "登录用户%s" % self.user
        self.driver = webdriver.Remote(self.uri, self.desired_caps)
        self.driver.implicitly_wait(5)
        boolLoginFlag1 = self.isElementExist(('android uiautomator', 'new UiSelector().resourceId("gaosi.com.learn:id/edt_phone")'))
        if boolLoginFlag1:
            print('**************************************登录学生端************************************')
            self.sendkeys_text(('id', 'gaosi.com.learn:id/edt_phone'), self.user)
            self.sendkeys_text(('id', 'gaosi.com.learn:id/edt_pass'), self.passwd)
            time.sleep(2)
            self.waitForclick(("id", "gaosi.com.learn:id/btn_login"))  #点击登录
            time.sleep(2)
            for i in range(0, 3):
                print("第%s次点击引导页"%(i+1))
                time.sleep(2)
                self.tapScreen(540, 1000)
            time.sleep(2)
            # 登录后新账号会提示修改密码，暂不修改
            self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/tv_cancel'))
            print('************************************登录学生端完成**********************************')

    #@unittest.skip('aaaa')
    def test01(self):
        '''测试学生端数学学科学生进行作业提交与作业订正'''
        self.waitForclick(('id','gaosi.com.learn:id/cvFirst'))#点击讲次1
        time.sleep(2)
        self.waitForclick(('id','gaosi.com.learn:id/tvHomeworkStatus')) #点击去提交
        time.sleep(2)
        self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/tvCancel'))#不再提示
        time.sleep(2)
        self.waitForclick(('id','gaosi.com.learn:id/ivTitleRight')) #点击客服反馈
        time.sleep(2)
        self.andriod_key()#安卓返回键
        print('********************************学生端数学班级开始测试******************************')
        time.sleep(3)
        #执行云测请打开这一步，本地执行可注释
        #self.switch_chromedriver_update() #选择合适的chromedriver版本

        H5_page_num = 0
        all_newzuoye_handles = []   #定义提交作业时所有的handle列表
        while H5_page_num <= 3:
            #执行云测请打开这一步，本地执行可注释
            # if H5_page_num != 0:
            #     time.sleep(5)
            self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
            print(u"webview切换成功")

            time.sleep(2)
            self.switchUrl_test(self.driver, 'newZuoye.html', 1)
            time.sleep(5)
            #选择题
            options = self.driver.find_elements_by_xpath("//div[@class='selectQuestion']")
            if len(options) > 0:
                self.waitForclick(('xpath', '//div[@id="select"]/div[1]/div/p'))

            #先获取作业页面的四个handle
            if H5_page_num==3:
                all_newzuoye_handles = self.driver.window_handles

            H5_page_num += 1
            time.sleep(2)
            self.switch_native()#切换原生
            time.sleep(2)
            if self.get_text(('xpath', '//android.widget.LinearLayout/android.widget.Button[2]')) == u"下一题":
                self.waitForclick(('xpath', "//android.widget.LinearLayout/android.widget.Button[2]"))
            else:
                self.waitForclick(('xpath', "//android.widget.LinearLayout/android.widget.Button[2]")) #完成

        time.sleep(2)
        print("++++++++++++++开始提交作业++++++++++++++++++")
        self.waitForclick(('id','gaosi.com.learn:id/btnConfirm'))#提交作业
        time.sleep(2)
        self.waitForclick(('id','gaosi.com.learn:id/tvCancel')) #直接交
        print(u'作业提交成功')
        time.sleep(10)
        self.tapScreen(540, 1000) #点击弹窗
        contexts = self.driver.contexts
        print(contexts)
        time.sleep(5)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print(u"webview切换成功")
        time.sleep(3)
        self.switchUrl(self.driver, "scorestaticHtml.html")
        time.sleep(3)
        print(u'开始订正作业')
        self.waitForclick(('xpath', "//button[@class='mint-button error-question mint-button--primary mint-button--large']")) #去订正
        time.sleep(3)
        self.onlinetest_math_environment(all_newzuoye_handles)#线上测试环境订正题目并提交
        #self.pro_math_environment()#生产环境订正题目并提交

        # 积分榜依赖作业提交，拆分不能降低耦合性，无意义
        # print("++++++++++++++积分榜点赞查看++++++++++++++++++")
        # self.scrollToFind(('xpath', "//div[@class=\"score-hw-rank\"]"))
        # self.waitForclick(('xpath', "//div[@class=\"score-hw-rank\"]"))
        # time.sleep(3)
        # self.switchUrl(self.driver, "homeworkRankstaticHtml.html")
        # time.sleep(8)
        # src1 = self.getattribute(('css selector', '.myRanking>.myInfo-pic>.myInfo-pic-show>img'), 'src')#获取自己头像src属性值
        # time.sleep(2)
        # self.waitForclick(('css selector', '.myRanking>.myInfo-pic>.myInfo-pic-show>img'))#点击自己头像
        # time.sleep(2)
        # self.switchUrl(self.driver, 'publicPopupstaticHtml.html')
        # time.sleep(5)
        # src2 = self.getattribute(('css selector', '.containers-level>.level-wrap>.containers-pic>img'), 'src')#获取点击头像弹窗中头像的src属性
        # self.assertEqual(src1, src2)
        # time.sleep(1)
        # self.waitForclick(('css selector', '.poupe-containers>.closePosition'))#点击关闭按钮
        # time.sleep(2)
        # self.switchUrl(self.driver, "homeworkRankstaticHtml.html")
        # time.sleep(2)
        # praiseNum = self.get_text(('css selector', '.myRanking>.myRanking-num>.likesMen>p'))#获取自己点赞数量
        # print(u'被点赞的数量为:%s'%praiseNum)
        # self.waitForclick(('css selector', '.myRanking>.myRanking-num>.likesMen>img'))
        # time.sleep(2)
        # self.switchUrl(self.driver, "thinkgoodMenstaticHtml.html")
        # time.sleep(2)
        # if int(praiseNum) == 0:
        #     text = self.get_text(('css selector', '.mine-main>.mine-none>span'))
        #     self.assertIn(text, u'还没有人赞过你～')
        # else:
        #     elements = self.findelements(('xpath', '//a[@class="mint-cell img-padding"]'))
        #     self.assertEqual(len(elements), int(praiseNum))
        # print(u'积分榜测试完成')

    @unittest.skip(u'英语作业提交与作业订正，此版本跳过测试')
    def test02(self):
        '''测试学生端英语学科学生进行课后作业提交与作业订正'''
        time.sleep(5)
        self.waitForclick(('id', 'gaosi.com.learn:id/iv_head_icon'))
        self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/llMan'))#第一次使用选择男女
        self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/tvComfirm'))#确定
        self.swipe_up()
        time.sleep(2)
        self.waitForclick(('android uiautomator', 'new UiSelector().className("android.widget.TextView").text("全部班级")'))
        self.switch_chromedriver() #选择合适的chromedriver版本
        time.sleep(5)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print("Webview切换成功")
        time.sleep(5)
        self.switchUrl(self.driver, 'myclassListstaticHtml.html')
        time.sleep(3)
        self.scrollToFind(('xpath', '//span[text()="thy学生端测试思高英语初一中考培优(暑)"]'))
        time.sleep(2)
        self.waitForclick(('xpath', '//span[text()="thy学生端测试思高英语初一中考培优(暑)"]'))
        time.sleep(2)
        self.switch_native()
        time.sleep(2)
        self.waitForclick(('xpath', '//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.TextView')) #点击第一节课后作业
        time.sleep(5)
        print('**************************************学生端英语班级课后作业开始测试**************************************')
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print("Webview切换成功")
        time.sleep(3)
        self.switchUrl(self.driver, 'publicPopupstaticHtml.html')
        time.sleep(2)
        self.click_element_or_coordinate(('css selector', '.button-wrap>.mint-button.green-button'), 540, 1320)#点击开始提交
        time.sleep(5)
        self.switchUrl(self.driver, 'zuoyestaticHtml.html')
        time.sleep(2)
        while True:
            #选择题
            options = self.findelements(('xpath', "//li[@class='single']"))
            if len(options) > 0:
                for option in options:
                    if option.find_element_by_xpath("../../..").get_attribute('style').find('overflow: hidden;') == -1:
                        option.click()
                        break
            #主观题-拍照i
            answers = self.findelements(('xpath', "//img[@class='unanswer']"))
            if len(answers) > 0:
                for answer in answers:
                    if answer.find_element_by_xpath("../../../..").get_attribute('style').find('overflow: hidden;') == -1:
                        # answer.click()
                        # time.sleep(1)
                        # answer.find_element_by_xpath("../following-sibling::div[1]/a").click()
                        pass

            time.sleep(2)
            if self.get_text(('xpath', '//div[@class=\'modules-homework-pageUpDown-down\']/span[1]')) == u"下一题":
                self.waitForclick(('xpath', "//div[@class='modules-homework-pageUpDown-down']/span[1]"))
                continue
            elif self.get_text(('xpath', '//div[@class=\'modules-homework-pageUpDown-down\']/span[1]')) == u"完成":
                self.waitForclick(('xpath', "//div[@class='modules-homework-pageUpDown-down']/span[1]"))
                break
        time.sleep(2)
        print("++++++++++++++开始提交作业++++++++++++++++++")
        time.sleep(4)
        self.switchUrl(self.driver, "anscardstaticHtml.html")
        time.sleep(3)
        self.click_element_or_coordinate(('xpath', "//button[@class='mint-button score-submit mint-button--primary mint-button--large']"), 550, 1840)#提交作业
        time.sleep(3)
        self.switch_native()
        time.sleep(3)
        self.waitForclick(('id', 'android:id/button1'))#提交
        print(u'作业提交成功')
        time.sleep(10)
        self.tapScreen(540, 1000) #点击弹窗
        time.sleep(5)
        self.tapScreen(540, 1000) #点击弹窗
        contexts = self.driver.contexts
        print(contexts)
        time.sleep(5)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print(u"webview切换成功")
        time.sleep(3)
        self.switchUrl(self.driver, "scorestaticHtml.html")
        time.sleep(4)
        print(u'开始订正作业')
        time.sleep(2)
        self.waitForclick(('xpath', "//button[@class='mint-button score-submit error-question mint-button--primary mint-button--large']"))
        time.sleep(3)
        self.onlinetest_english_environment() #线上测试环境英语订正题目并提交

    @unittest.skip(u'英语口语作业提交与作业订正，此版本跳过测试')
    def test03(self):
        '''测试学生端英语学科学生进行英语口语作业提交与作业订正'''
        time.sleep(5)
        self.waitForclick(('id', 'gaosi.com.learn:id/iv_head_icon'))
        self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/llMan'))#第一次使用选择男女
        self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/tvComfirm'))#确定
        self.swipe_up()
        time.sleep(2)
        self.waitForclick(('android uiautomator', 'new UiSelector().className("android.widget.TextView").text("全部班级")'))
        self.switch_chromedriver() #选择合适的chromedriver版本
        time.sleep(5)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print("Webview切换成功")
        time.sleep(5)
        self.switchUrl(self.driver, 'myclassListstaticHtml.html')
        time.sleep(3)
        self.scrollToFind(('xpath', '//span[text()="thy学生端测试思高英语初一中考培优(暑)"]'))
        time.sleep(2)
        self.waitForclick(('xpath', '//span[text()="thy学生端测试思高英语初一中考培优(暑)"]'))
        time.sleep(2)
        self.switch_native()
        time.sleep(2)
        self.waitForclick(('xpath', '//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.RelativeLayout[2]/android.widget.LinearLayout[1]/android.widget.TextView')) #点击第一节英语口语作业
        time.sleep(5)
        print('**************************************学生端英语班级口语开始测试**************************************')
        elements = self.findelements(('android uiautomator', 'new UiSelector().className("android.support.v7.app.ActionBar$Tab")')) #获取英语口语题目总数
        print('题目总数为：%s'%len(elements))
        i = 1
        while i < int(len(elements)):
            print('第{}题'.format(i))
            self.waitForclick(('xpath', '//android.widget.RelativeLayout/android.widget.LinearLayout[2]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView'))#点击录音
            time.sleep(2)
            self.waitForclick(('xpath', '//android.widget.RelativeLayout/android.widget.LinearLayout[2]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView'))#点击停止录音
            time.sleep(4)
            i += 1
            if i == int(len(elements)):
                break
            else:
                self.waitForclick(('android uiautomator', 'new UiSelector().className("android.widget.TextView").text("第{}题")'.format(i)))
                time.sleep(2)
        self.waitForclick(('android uiautomator', 'new UiSelector().className("android.widget.TextView").text("第5题")'))
        time.sleep(1)
        self.swipe_up()#手机屏幕上滑处理   处理某些手机完成按钮在页面不能完全展示的问题
        time.sleep(2)
        self.waitForclick(('android uiautomator', 'new UiSelector().className("android.widget.TextView").text("完成")'))
        print("++++++++++++++开始提交英语口语作业++++++++++++++++++")
        time.sleep(5)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print("Webview切换成功")
        time.sleep(3)
        self.switchUrl(self.driver, "oralListstaticHtml.html")
        time.sleep(3)
        self.click_element_or_coordinate(('css selector', "div.submitButton"), 550, 1840)#提交作业
        time.sleep(3)
        self.waitForclick(('css selector', "div.bottomButton>button.submit"))#提交按钮
        time.sleep(5)
        print(u'作业提交成功')
        self.switch_native()
        time.sleep(10)
        self.tapScreen(540, 1000) #点击弹窗
        time.sleep(5)
        self.tapScreen(540, 1000) #点击弹窗
        contexts = self.driver.contexts
        print(contexts)
        time.sleep(2)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print(u"webview切换成功")
        time.sleep(5)
        self.switchUrl(self.driver, "oralScorestaticHtml.html")
        time.sleep(3)
        print(u'开始订正作业')
        self.waitForclick(('xpath', "//button[@class='mint-button score-submit error-question mint-button--primary mint-button--large']"))
        time.sleep(3)
        self.switch_native()
        time.sleep(3)
        self.onlinetest_english_spoken_environment() #线上测试环境英语口语作业订正题目并提交


    @unittest.skip(u'个人装扮流程已经上线，此版本跳过测试')
    def test04(self):
        '''测试装扮流程'''
        print("++++++++++++++开始测试装扮流程++++++++++++++++++")
        time.sleep(5)
        self.tapScreen(540, 300)#点击头像
        try:
            self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/llMan'))#第一次使用选择男女
            self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/tvComfirm'))#确定
            time.sleep(5)
            self.driver.find_element_by_android_uiautomator('new UiSelector().className("android.widget.TextView").text("抽取装扮")').click()
        except:
            self.tapScreen(810, 1830)#点击我的
            print(u'点击我的坐标')
            self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/llMan'))#第一次使用选择男女
            self.is_element_exist_and_click(('id', 'gaosi.com.learn:id/tvComfirm'))#确定
            time.sleep(5)
            self.waitForclick(('android uiautomator', 'new UiSelector().className("android.widget.TextView").text("抽取装扮")'))
        time.sleep(5)
        self.switch_chromedriver()  #选择合适的chromedriver版本
        time.sleep(5)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print("Webview切换成功")
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


    def tearDown(self):
        '''退出app'''
        self.driver.close_app()
        print(u'app关闭成功')

    #业务内容封装
    def onlinetest_math_environment(self, all_newzuoye_handles):
        '''测试环境学生端数学自动化作业订正'''
        print("去订正")
        # 第一题
        print("开始订正第1题")
        self.switch_native()
        time.sleep(2)
        self.waitForclick(('id', 'gaosi.com.learn:id/btnConfirm'))#点击做相似题
        time.sleep(2)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print(u"webview切换成功")
        self.switchUrl_profect_handle(self.driver, "newZuoye.html", all_newzuoye_handles) #切换第1题的H5 handle
        time.sleep(2)
        self.scrollToFind(('xpath', '//div[@id="select"]/div[4]/div/p'))#滑动到最底部
        time.sleep(2)
        self.waitForclick(('xpath', '//div[@id="select"]/div[4]/div/p'))
        self.switch_native()
        time.sleep(2)
        self.waitForclick(('id', 'gaosi.com.learn:id/btnConfirm'))#提交
        #第二题
        print("开始订正第2题")
        time.sleep(4)
        self.waitForclick(('id', 'gaosi.com.learn:id/btnConfirm'))#点击做相似题
        time.sleep(2)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print(u"webview切换成功")
        self.switchUrl_profect_handle(self.driver, "newZuoye.html", all_newzuoye_handles) #切换第2题的H5 handle
        time.sleep(2)
        self.sendkeys_text(('xpath', '//div[@id="blank"]/p/input'), u"24．")
        time.sleep(1)
        self.waitForclick(('xpath', '//p[@class="newTitle"]')) #点击填空题 去除输入框内的光标
        time.sleep(2)
        self.switch_native()
        self.waitForclick(('id', 'gaosi.com.learn:id/btnConfirm'))#提交
        # 第三题
        print("开始订正第3题")
        time.sleep(4)
        self.waitForclick(('id', 'gaosi.com.learn:id/btnConfirm'))#点击做相似题
        time.sleep(2)
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print(u"webview切换成功")
        self.switchUrl_profect_handle(self.driver, "newZuoye.html", all_newzuoye_handles) #切换第3题的H5 handle
        time.sleep(2)
        self.waitForclick(('xpath',  '//div[@id="judge"]/div[1]/p[2]/span[2]'))
        self.waitForclick(('xpath',  '//div[@id="judge"]/div[2]/p[2]/span[1]'))
        self.waitForclick(('xpath',  '//div[@id="judge"]/div[3]/p[2]/span[2]'))
        self.scrollToFind(('xpath', "//span[contains(text(),'6')]"))#滑动到最底部
        time.sleep(1)
        self.waitForclick(('xpath',  '//div[@id="judge"]/div[4]/p[2]/span[2]'))
        self.waitForclick(('xpath',  '//div[@id="judge"]/div[5]/p[2]/span[1]'))
        self.waitForclick(('xpath',  '//div[@id="judge"]/div[6]/p[2]/span[2]'))
        time.sleep(2)
        self.switch_native()
        self.waitForclick(('id', 'gaosi.com.learn:id/btnConfirm'))#提交
        time.sleep(3)
        self.waitForclick(('id', 'gaosi.com.learn:id/ivTitleLeft'))#返回
        time.sleep(1)
        self.waitForclick(('id', 'gaosi.com.learn:id/tvCancel'))#以后再说
        self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
        print(u"webview切换成功")
        time.sleep(4)
        self.switchUrl(self.driver, "scorestaticHtml.html")
        time.sleep(5)
        elements = self.findelements(('xpath', '//p[text()=\'已订正\']'))#获取订正结果
        self.assertEqual(len(elements), 3)
        print(u'断言成功，作业提交订正完成')
        print("结束订正")

    def pro_math_environment(self):
        '''生产环境学生端数学自动化作业订正'''
        print("去订正")
        # 第一题
        print("开始订正第1题")
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(4)
        self.click_element_or_coordinate(('xpath', "//button[@class='mint-button score-submit mint-button--primary mint-button--large']"), 550, 1840)
        time.sleep(2)
        self.switchUrl(self.driver, "correctProstaticHtml.html") #订正页面
        time.sleep(4)
        self.waitForOptionsClick(('xpath',  "//li[@class='single']"), 2)
        self.click_element_or_coordinate(('xpath', "//button[@class='mint-button score-submit mint-button--primary mint-button--large']"), 550, 1840)
        #第二题
        print("开始订正第2题")
        time.sleep(2)
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(4)
        self.click_element_or_coordinate(('xpath', "//button[@class='mint-button score-submit mint-button--primary mint-button--large']"), 550, 1840)
        time.sleep(2)
        self.switchUrl(self.driver, "correctProstaticHtml.html")
        time.sleep(4)
        self.sendkeys_text(('xpath', '//div[@class="modules-do-work-items"]/div[1]/input'), u"答案为45°")
        #self.waitForclick(('xpath', "//button[@class='mint-button score-submit mint-button--primary mint-button--large']"))
        self.click_element_or_coordinate(('xpath', "//button[@class='mint-button score-submit mint-button--primary mint-button--large']"), 550, 1840)
        # 第三题
        print("开始订正第3题")
        time.sleep(2)
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(2)
        self.click_element_or_coordinate(('xpath', "//button[@class='mint-button score-submit mint-button--primary mint-button--large']"), 550, 1840)
        time.sleep(2)
        self.switchUrl(self.driver, "correctProstaticHtml.html")
        time.sleep(4)
        self.waitForclick(('xpath',  '//ul[@class="modules-do-work-items"]/li[1]/div[2]/label[1]'))
        self.waitForclick(('xpath',  '//ul[@class="modules-do-work-items"]/li[2]/div[2]/label[2]'))
        self.waitForclick(('xpath',  '//ul[@class="modules-do-work-items"]/li[3]/div[2]/label[1]'))
        self.waitForclick(('xpath',  '//ul[@class="modules-do-work-items"]/li[4]/div[2]/label[1]'))
        time.sleep(4)
        self.click_element_or_coordinate(('xpath', "//button[@class='mint-button score-submit mint-button--primary mint-button--large']"), 550, 1840)
        time.sleep(4)
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        self.waitForclick(('css selector', '.mint-button--normal.mint-button--default'))#点击返回
        time.sleep(4)
        self.switchUrl(self.driver, "scorestaticHtml.html")
        time.sleep(5)
        elements = self.findelements(('xpath', '//p[text()=\'已订正\']'))#获取订正结果
        self.assertEqual(len(elements), 3)
        print(u'断言成功，作业提交订正完成')
        print("结束订正")

    def onlinetest_english_environment(self):
        '''测试环境学生端英语课后自动化作业订正'''
        print("去订正")
        # 第一题
        print("开始订正第1题")
        time.sleep(2)
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(2)
        self.click_element_or_coordinate(('css selector', ".mint-button.score-submit.mint-button--primary.mint-button--large"), 550, 1840)
        time.sleep(2)
        self.switchUrl(self.driver, "correctProstaticHtml.html") #订正页面
        time.sleep(3)
        self.waitForOptionsClick(('xpath',  "//li[@class='single']"), 1)
        self.click_element_or_coordinate(('css selector', ".mint-button.score-submit.mint-button--primary.mint-button--large"), 550, 1840)
        #第二题
        print("开始订正第2题")
        time.sleep(2)
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        time.sleep(2)
        self.click_element_or_coordinate(('css selector', ".mint-button.score-submit.mint-button--primary.mint-button--large"), 550, 1840)
        time.sleep(2)
        self.switchUrl(self.driver, "correctProstaticHtml.html")
        time.sleep(3)
        self.waitForOptionsClick(('xpath',  "//li[@class='single']"), 1)
        self.click_element_or_coordinate(('css selector', ".mint-button.score-submit.mint-button--primary.mint-button--large"), 550, 1840)
        time.sleep(4)
        self.switchUrl(self.driver, "correctionstaticHtml.html")
        self.waitForclick(('css selector', '.mint-button--normal.mint-button--default'))#点击返回
        time.sleep(4)
        self.switchUrl(self.driver, "scorestaticHtml.html")
        time.sleep(5)
        elements = self.findelements(('xpath', '//p[text()=\'已订正\']'))#获取订正结果
        self.assertEqual(len(elements), 2)
        print(u'断言成功，课后作业提交订正完成')
        print("课后作业结束订正")

    def onlinetest_english_spoken_environment(self):
        '''测试环境学生端英语口语自动化作业订正'''
        print("去订正")
        elements = self.findelements(('android uiautomator', 'new UiSelector().className("android.support.v7.app.ActionBar$Tab")')) #获取英语口语题目总数
        print('题目总数为：%s'%len(elements))
        i = 1
        while i <= int(len(elements)):
            print('第{}题'.format(i))
            self.waitForclick(('xpath', '//android.widget.RelativeLayout/android.widget.LinearLayout[2]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView'))#点击录音
            time.sleep(2)
            self.waitForclick(('xpath', '//android.widget.RelativeLayout/android.widget.LinearLayout[2]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView'))#点击停止录音
            time.sleep(4)
            i += 1
            if i == int(len(elements))+1:
                break
            else:
                self.waitForclick(('android uiautomator', 'new UiSelector().className("android.widget.TextView").text("第{}题")'.format(i)))
                time.sleep(2)
        print("英语口语作业结束订正")


    def switch_chromedriver(self):
        '''在chromedriver版本列表中，查找符合该手机chrome版本的驱动'''
        global chromedriver_version
        intFlag=0
        chromedriver = ['2.24', '2.23', '2.20', '2.22', '2.34', '2.26', '2.33', '2.32', '2.31', '2.30', '2.29', '2.28', '2.27', '2.25', '2.21', '2.18', '2.16', '2.14']#按照常用的排序
        defaultPath = "/tmp/chromedriver"
        while True:
          try:
            time.sleep(2)
            contexts = self.driver.contexts
            print contexts
            time.sleep(5)
            self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
            print self.driver.current_context
            if intFlag > 0:
                print(u'切换成功,匹配的chromedriver为%s版本'%chromedriver[intFlag-1])
                chromedriver_version = chromedriver[intFlag-1]
            break
          except Exception, e:
            print Exception, ":", e
            chromedriverPath = '/appium/appium-chromedriver/chromedriver/linux/chromedriver_64_'+chromedriver[intFlag]
            self.copyChromedriver(chromedriverPath, defaultPath)
            print(u'chromedriver版本为%s'%chromedriver[intFlag])
            intFlag = intFlag+1
            if intFlag == len(chromedriver):
                chromedriver_version = None
                print(u'没有找到webview!')
                break

    def switch_chromedriver_update(self):
        '''在chromedriver版本列表中，查找符合该手机chrome版本的驱动，不使用默认chromedriver'''
        global chromedriver_version
        intFlag=0
        chromedriver = ['2.24', '2.23', '2.20', '2.22', '2.34', '2.26', '2.33', '2.32', '2.31', '2.30', '2.29', '2.28', '2.27', '2.25', '2.21', '2.18', '2.16', '2.14']#按照常用的排序
        defaultPath = "/tmp/chromedriver"
        while True:
            try:
                chromedriverPath = '/appium/appium-chromedriver/chromedriver/linux/chromedriver_64_'+chromedriver[intFlag]
                self.copyChromedriver(chromedriverPath, defaultPath)
                print(u'chromedriver版本为%s'%chromedriver[intFlag])
                time.sleep(3)
                contexts = self.driver.contexts
                print contexts
                time.sleep(5)
                self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
                print self.driver.current_context
                if self.driver.current_context == u'WEBVIEW_gaosi.com.learn':
                    print(u'切换成功,匹配的chromedriver为%s版本'%chromedriver[intFlag])
                break
            except Exception, e:
                print Exception, ":", e
                intFlag = intFlag+1
                if intFlag == len(chromedriver):
                    chromedriver_version = None
                    print(u'没有找到webview!')
                    break

    #底层封装方法
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

    #调试专用
    def sUrl(self, driver, suburl):
        '''切换handle，打印所有包含suburl的handle'''
        time.sleep(2)
        all_handles = driver.window_handles
        for handle in all_handles:
            driver.switch_to_window(handle)
            print(driver.current_url.find(suburl))

    def __sUrl_test(self, driver, suburl):
        '''切换handle，获取订正时所有handle'''
        time.sleep(2)
        dingzheng_handel_newzuoye=[]
        all_handles = driver.window_handles
        for handle in all_handles:
            driver.switch_to_window(handle)
            #print(driver.current_url.find(suburl))
            if driver.current_url.find(suburl)>-1:
                dingzheng_handel_newzuoye.append(handle)
        #print("dingzheng_handel_newzuoye:%s"%dingzheng_handel_newzuoye)
        return dingzheng_handel_newzuoye

    def __switch_handle(self, list1, list2):
        '''list1 为订正作业时取到的handles，list2为提交作业时取到的handles
        '''
        for i in range(0, len(list1)):
            if list1[i] not in list2:
                return list1[i]

    def get_profect_handle(self, driver, suburl, list2):
        '''通过对比提交作业和订正作业的包含suburl的handels，获取指定的handle'''
        list1 = self.__sUrl_test(driver, suburl)
        profect_handle = self.__switch_handle(list1, list2)
        print("profect_handle:%s"%profect_handle)
        return profect_handle

    def switchUrl_profect_handle(self, driver, suburl, list2):
        '''切换handle，切换指定的handle'''
        intCount = 0
        while intCount < 10:
            try:
                time.sleep(2)
                intCount = intCount + 1
                print("窗口%s ，第%s次切换" % (suburl, str(intCount)))
                handle = self.get_profect_handle(driver, suburl, list2)
                driver.switch_to_window(handle)
                if driver.current_url.find(suburl)>-1:
                    intCount=10
                    break
            except:
                continue

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
                continue

    def switchUrl_test(self, driver, suburl, i):
        '''切换handle,指定handel列表的下标，切换html'''
        intCount = 0
        while intCount < 10:
            try:
                time.sleep(2)
                intCount = intCount + 1
                print("窗口%s ，第%s次切换" % (suburl, str(intCount)))
                all_handles = driver.window_handles
                print(all_handles)
                driver.switch_to_window(all_handles[i])
                if driver.current_url.find(suburl)>-1:
                    intCount= 10
                    break
            except:
                continue

    def  waitForclick(self, locator):
        '''显式等待元素出现后进行点击操作，传入locator的格式（'xpath','....'）定位方式可以使用id、name、xpath、css....'''
        element = self.findelement(locator)
        element.click()

    def sendkeys_text(self, locator, text):
        '''输入框输入文本'''
        element = self.findelement(locator)
        element.send_keys(text)

    def is_element_exist_and_click(self, locator, timeout=4):
        '''判断元素是否存在，存在点击，不存在则进行下一步操作'''
        try:
            element = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
            element.click()
        except:
            pass

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
           WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_element_located(toast_loc))
           return True
        except:
            print(u'页面没有包含%s'%text)
            return False

    def click_element_or_coordinate(self, locator, x, y):
        '''判断元素是否存在，不存在则点击其坐标'''
        result = self.isElementExist(locator)
        if result:
            self.waitForclick(locator)
        else:
            print(u'元素%s未找到'%locator[1])
            self.switch_native()
            time.sleep(2)
            self.tapScreen(x, y)#点击坐标
            time.sleep(5)
            self.driver.switch_to.context(u'WEBVIEW_gaosi.com.learn')
            print("切换成功")

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
        time.sleep(1)

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
        self.driver.swipe(screen[0]*0.85, screen[1]*0.5, screen[0]*0.15, screen[1]*0.5, t)

    def swipe_right(self, t=500):
        '''向右滑动  从屏幕的左端点击一个坐标点然后往后滑动.Y坐标可以不变。X的开始和结束坐标改变即可'''
        screen = self.get_screen_size()
        self.driver.swipe(screen[0]*0.25, screen[1]*0.5, screen[0]*0.75, screen[1]*0.5, t)

    # def drag(self, locator, x, y):
    #     '''拖拽一个元素到指定的坐标'''
    #     element = self.findelement(locator)
    #     action = ActionChains(self.driver)
    #     action.drag_and_drop_by_offset(element, x, y).perform()

    def copyChromedriver(self, srcFilePath, dstFilePath):
        '''复制文件到新路径下'''
        shutil.copy(srcFilePath, dstFilePath)

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
        screen_width_case_phone = 1080
        screen_height_case_phone =1920
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