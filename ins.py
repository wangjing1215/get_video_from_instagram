# -*- coding: utf-8 -*-
import requests as req
import time
import os
from requests.cookies import RequestsCookieJar
import pymysql
headers = {
            'Host': 'www.instagram.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-us;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Referer': 'https://www.instagram.com/accounts/login/?source=auth_switcher',
            'X-CSRFToken':'WtYeNx61dL1QWntFJtZp1biKuv9Icpxd',
            'X-Instagram-AJAX': 'c5b336091f6'}

def parse(response):
    # print(response.body)
    conn = pymysql.connect(host='172.18.0.3', user='root', passwd='123456', db='scrapy',charset='utf8')
    cursor = conn.cursor()
    print('*********************************')
    thehtml = str(response)
    thehtml = thehtml.replace('\\', '')
    #print (thehtml)
    video_url_list = []
    flag = 0
    back = 0
    try:
        limi = thehtml.rindex('video_url')
    except:
        limi = 0
    while(flag < limi):
        pro = thehtml.index('video_url', back)
        back = thehtml.index('video_view_count', pro)
        video_url=thehtml[pro+12:back-3]
        print(video_url)
        video_url_list.append(video_url)
        flag = pro
    for  i in video_url_list:
        sql = "SELECT * FROM ins_url WHERE videoid = '{}'".format(i[45:55])
        cursor.execute(sql)
        # 获取所有记录列表
        if cursor.execute(sql) == 0:
            print('新记录+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            insert_sql = "INSERT INTO ins_url(videoid,videorul,date,statue) VALUES('{}', '{}', now(),'0')".format(i[45:55], i)
            print(insert_sql)
            try:
                cursor.execute(insert_sql)
                conn.commit()

            except:
                print('内容错误')
        else:
            print('已存在记录-------------------------------------------------')
        '''
        last = req.get(url=i,cookies=cookies)
        filename = '/home/wj/test/'+i[45:55]+'.mp4'
        if os.path.exists(filename):
            print('this ' + filename + ' have exists')
            continue
        with open(filename, 'ab+') as f:
            print('write '+filename)
            f.write(last.content)
            f.flush()
            print('write ' + filename+' end')
        '''
    conn.close()




def cookie():
    print('start')

    loginUrl = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
    s = req.session()
    postdata = { 'username': 'wangjing1215133636@gmail.com', 'password': '133636wj', 'queryParams': '{"source": "auth_switcher"}'}
    #print(postdata)
    s = s.post(url=loginUrl, data=postdata, headers=headers)
    #print(postdata)
    c = req.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
    c.set('cookie-name', 'cookie-value')
    s.cookies.update(c)
    print(s.cookies.get_dict())
    return s.cookies.get_dict()

if __name__ == "__main__":
    try:
        while(1):
            cookies = cookie()
            cookies['shbts'] = str(time.time())
            cookies['shbid'] = '*********'
            cookies['ds_user_id'] = '***********'
            cookies['sessionid'] = '************%3AMbdlmwg37gYAVb%3A28'
            cookies['urlgen'] = '{\"************\": 20473}:1gX6Kn:31_4pQKGPdcqQoCYjCJjejFe03Q}'
            ulr = 'https://www.instagram.com'
            o = req.get(ulr,  headers=headers, cookies=cookies)
            parse(o.text)
            time.sleep(120)
    except:
        pass




