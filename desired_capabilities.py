# -*- encoding:utf8 -*- 

#!/usr/bin/env python

def get_desired_capabilities():
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '5.1.1',
        'deviceName': 'd6d9f4c6', #vivo chromedriver.exe2.26
        # 'platformVersion': '7.1.1',
        # 'deviceName': '8c966ad4',   #vivo X20A chromedriver.exe2.32
        'appPackage': '******',
        'appActivity': '*******',
        # 'app': "C:\\Users\\hp\\Documents\\student1.6.0.apk",
        'newCommandTimeout': 60,
        'automationName': 'Appium',
        #'automationName': 'Uiautomator2',
        'chromedriverExecutable': "C:\\Python27\\chromedriver.exe",
        'unicodeKeyboard': True,
        'resetKeyboard': True
    }
    return desired_caps

def get_uri():
    return "http://127.0.0.1:4723/wd/hub"

def getParam(st):
    if st == 'username':
        return '******'
    elif st == 'password':
        return '**********'
