from selenium import webdriver
import test.ins as ins
from time import sleep,time
import requests as req

import re
import pymysql

browser = webdriver.Firefox(executable_path="/home/wj/Downloads/gecko/geckodriver")

browser.get("https://www.instagram.com/kayf_tv/")

sleep(3)
url = browser.find_elements_by_xpath('/html/body/span/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a')

for i in url:
    print(i.get_attribute('href'))
urllist=[]
j = 0
k = 1
o = 0
c = 0
conn = pymysql.connect(host='172.18.0.3', user='root', passwd='123456', db='scrapy',charset='utf8')
cursor = conn.cursor()
try:
    while(1):
        j = j + 1
        if j==4:
            k = k+1
            j=1
        path = "/html/body/span/section/main/div/div[3]/article/div[1]/div/div[{}]/div[{}]/a".format(k,j)
        print(path)
        try:

            url = browser.find_element_by_xpath(path)
            print(url.get_attribute('href'))
        except:
            print('not found')
            print('the {} try'.format(o))
            o=o+1
            j=j-1
            if o==3:
                if k==16:
                    k=12
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                sleep(5)
                o = 0
            continue
        r = req.get(url.get_attribute('href'), headers=ins.headers)
        starlist = re.findall('<meta property="og:video" content="(.*)" />', r.text)
        print (starlist)
        try:
            i = starlist[0]
        except:
            j = j + 1
            if j == 4:
                k = k + 1
                j = 1
            continue
        sql = "SELECT * FROM ins_url WHERE videoid = '{}'".format(i[45:55])
        cursor.execute(sql)
        # 获取所有记录列表
        if cursor.execute(sql) == 0:
            print('new++++++++++++++++++++++++++++++++++++++++++++++++++++')
            insert_sql = "INSERT INTO ins_url(videoid,videorul,date,statue) VALUES('{}', '{}', now(),'0')".format(i[45:55],i)
            print(insert_sql)
            try:
                cursor.execute(insert_sql)
                conn.commit()

            except:
                print('内容错误')
        else:
            print('old---------------------------------------------------')


finally:
    conn.close()
    browser.close()




