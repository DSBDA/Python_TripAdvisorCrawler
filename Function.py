import os
from selenium import webdriver
import pypyodbc
from datetime import datetime, timedelta


def DatabaseConnectionBuilder():
    IPAddress = '140.123.174.167'
    UserName = 'kakaci123'
    PassWord = 'zaza5201314'
    DataBase = 'TripAdvisor_ChenWei'

    connection = pypyodbc.connect('Driver={SQL Server};'
                                  'Server=' + IPAddress + ';'
                                                          'Database=' + DataBase + ';'
                                                                                   'uid=' + UserName + ';pwd=' + PassWord + '')
    return connection.cursor()


def BrowserSetting():
    cwd = os.getcwd() + '/'
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=en')
    driver = webdriver.Chrome(executable_path=cwd + 'chromedriver',
                              chrome_options=options)
    return driver


def BrowserSetting2():
    cwd = os.getcwd() + '/'
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'en'
    driver = webdriver.PhantomJS(cwd + 'phantomjs')
    return driver


def GetTimeStamp():
    return str(datetime.now()).split(' ')[0]


def GetYesterdayTimeStamp():
    return str(datetime.now() + timedelta(days=-1)).split(' ')[0]
