import pymysql
import test.ins as ins
import time
import requests as req
import  os

try:
    while(1):
        conn = pymysql.connect(host='172.18.0.3', user='root', passwd='123456', db='scrapy', charset='utf8')
        cursor = conn.cursor()
        sql = "SELECT * FROM ins_url where statue='0' order by date desc "
        cursor.execute(sql)
        if cursor.execute(sql)==0:
            print('no url '+str(time.ctime()))

        else:
            print('have url '+str(time.ctime()))
            results = cursor.fetchall()
            for row in results:
                cookies = ins.cookie()
                cookies['shbts'] = str(time.time())
                cookies['shbid'] = '*******'
                cookies['ds_user_id'] = '***********'
                cookies['sessionid'] = '***********%3AMbdlmwg37gYAVb%3A28'
                cookies['urlgen'] = '{\"****************\": 20473}:1gX6Kn:31_4pQKGPdcqQoCYjCJjejFe03Q}'
                i = row[2]
                last = req.get(url=i, cookies=cookies)
                filename = '/home/wj/test/' + i[45:55] + '.mp4'
                with open(filename, 'ab+') as f:
                    update_sql = "UPDATE ins_url SET statue = '1' where videoid = '{}'".format(i[45:55])
                    try:
                        cursor.execute(update_sql)
                        conn.commit()

                    except:
                        print('内容错误')
                    print('write ' + filename)
                    f.write(last.content)
                    f.flush()
                    print('write ' + filename + ' end')
        time.sleep(10)
        conn.close()

finally:
    pass
