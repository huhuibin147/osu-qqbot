import multiprocessing
import traceback
import requests
import time
import json
import pymysql
import re
import random

osu_api_key = 'b68fc239f6b8bdcbb766320bf4579696c270b349'

page = random.randint(1, 525)
url = 'http://www.xicidaili.com/nt/%s' % page
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
res = requests.get(url, headers=headers)
value = re.compile(r'<td class="country">.*?<img.*?<td>(.*?)</td>.*?<td>(.*?)</td>',re.S)
values = value.findall(res.text)
#values = [(ip,port),(127.0.0.1,80)]
# return values

def get_ip_list():
    '''返回prox list'''
    page = random.randint(1, 525)
    url = 'http://www.xicidaili.com/nt/%s' % page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    value = re.compile(r'<td class="country">.*?<img.*?<td>(.*?)</td>.*?<td>(.*?)</td>',re.S)
    values = value.findall(res.text)
    #values = [(ip,port),(127.0.0.1,80)]
    return values

def get_random_prox():
    # if not ip_list:
    #     ip_list = get_ip_list()
    # ip_tup = random.choice(ip_list)
    ip_tup = random.choice(values)
    proxy_ip = "http://%s:%s" % (ip_tup[0],ip_tup[1])
    proxies = {'http': proxy_ip}
    # print (proxies)
    return proxies

def get_url(url, timeout=3):
    '''通用读Url'''
    try:
        proxies = get_random_prox()
        res = requests.get(url, timeout=timeout, proxies=proxies)
        return res
    except:
        print('超时..')
        # traceback.print_exc()
        return 0


conn = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu', charset='utf8')

def get_cursor():
    return conn.cursor()

def setid(info):
    '''插入'''
    try:
        cur = get_cursor()
        sql = '''
            insert into osu_user
                (user_id, username, tth, ranked_score, total_score, pp_rank, level, pp_raw, acc, country, pc) 
            values
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        tth = int(info.get('count300',0))+int(info.get('count100',0))+int(info.get('count50',0))
        args = [info.get('user_id'), info.get('username'), tth, info.get('ranked_score'), info.get('total_score'), info.get('pp_rank'), info.get('level'), info.get('pp_raw'), round(float(info.get('accuracy')),2), info.get('country'), info.get('playcount')]
        result = cur.execute(sql, args)
        conn.commit()
        print('insert '+ info.get('user_id'))
    except:
        conn.rollback()
        # traceback.print_exc()

def get_user(uid):
    '''uid+0到+10的范围抓取,用于探索Uid使用,范围id抓取'''
    for i in range(10):
        uid += i
        print ("uid:%s" % uid)
        url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osu_api_key, uid)
        res = get_url(url,3)
        while res == 0:
            res = get_url(url)
        result = json.loads(res.text)
        #插入
        if len(result)>0:
            if result.get('count300') is not None:
                setid(result[0])
        
def get_user2(uid):
    '''uid抓取,单id存在的抓取'''
    print ("uid:%s" % uid)
    url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osu_api_key, uid)
    res = get_url(url,3)
    while res == 0:
        res = get_url(url)
    result = json.loads(res.text)
    #插入
    if result:
        setid(result[0])

def main(start=0, num=1):
    '''按uid分进程爬，30个进程并发'''
    for t in range(num):
        pool = multiprocessing.Pool(processes=30)
        pre_num = t*300+start
        for i in range(30):
            pool.apply_async(get_user, (pre_num+10*i, ))
        pool.close()
        pool.join()
        
def main2(start=1,num=1):
    '''按rank页爬，10个进程并发'''
    pool = multiprocessing.Pool(processes=20)
    for i in range(num):
        pool.apply_async(getUserList, (start+i, ))
    pool.close()
    pool.join()

def getUserList(page=1,country='TW'): 
    '''取rank页资源'''
    try:
        # url = 'https://osu.ppy.sh/p/pp/?m=0&s=3&o=1&f=&page=%s' % page
        url = 'https://osu.ppy.sh/p/pp/?c=%s&m=0&s=3&o=1&f=&page=%s' % (country,page)
        res = get_url(url,3)
        while res == 0:
            res = get_url(url)
        result = res.text
        print('page:'+str(page)) 
        pattern = re.compile('onclick="document.location=&quot;/u/(.*?)&quot;"')
        result = pattern.findall(result)
        # print (result)
        if not result:
            return
        for r in result:
            get_user2(r)
    except:
        traceback.print_exc()

def getBp(uid='-interesting-'):
    '''bp抓取'''
    try:
        url = 'https://osu.ppy.sh/api/get_user_best?k=b68fc239f6b8bdcbb766320bf4579696c270b349&u=%s' % uid
        res = get_url(url,3)
        while res == 0:
            res = get_url(url)
        result = json.loads(res.text)
        print('uid:'+ str(uid))
        # print(result)
        for r in result:
            insert_bp(r)
    except:
        traceback.print_exc()

def insert_bp(info):
    '''插入'''
    try:
        cur = get_cursor()
        sql = '''
            insert into osu_bp
                (beatmap_id, score, maxcombo, countmiss, acc, mods, user_id, date, rank, pp) 
            values
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        c50 = float(info['count50'])
        c100 = float(info['count100'])
        c300 = float(info['count300'])
        cmiss = float(info['countmiss'])
        acc = round((c50*50+c100*100+c300*300)/(c50+c100+c300+cmiss)/300*100,2)
        args = [info.get('beatmap_id'), info.get('score'), info.get('maxcombo'), info.get('countmiss'), acc, info.get('enabled_mods'), info.get('user_id'), info.get('date'), info.get('rank'), info.get('pp')]
        result = cur.execute(sql, args)
        conn.commit()
        print('insert:%s,%s' % (info.get('user_id'), info.get('beatmap_id')))
    except:
        conn.rollback()
        # traceback.print_exc()

def get_uid_bycountry(cou='CN'):
    try:
        cur = get_cursor()
        sql = '''
            SELECT user_id from osu_user where country=%s LIMIT 6115,3800
        '''
        cur.execute(sql, cou)
        res = cur.fetchall()
        return res
    except:
        traceback.print_exc()

def main3(cou='CN'):
    '''按rank页爬，10个进程并发'''
    res = get_uid_bycountry(cou)
    pool = multiprocessing.Pool(processes=10)
    for r in res:
        pool.apply_async(getBp, (r[0], ))
    pool.close()
    pool.join()



if __name__ == "__main__":

    start_time = time.time()
    #x页 y*10条
    main2(1,200)
    

    #x号id y*300条
    # main(8000000, 10000)
    used_time = time.time()-start_time
    print ("结束,用时:"+ str(used_time))
