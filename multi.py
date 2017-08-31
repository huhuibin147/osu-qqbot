import multiprocessing
import traceback
import requests
import time
import json
import pymysql

osu_api_key = 'b68fc239f6b8bdcbb766320bf4579696c270b349'

def get_url(url, timeout=1):
    try:
        res = requests.get(url, timeout=timeout)
        return res
    except:
        print('超时..')
        return 0

conn = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu', charset='utf8')

def get_cursor():
    return conn.cursor()

def setid(info):
    try:
        cur = get_cursor()
        sql = '''
            insert into osu_user
                (user_id, username, pc, ranked_score, total_score, pp_rank, level, pp_raw, acc, country) 
            values
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        pc = int(info.get('count300',0))+int(info.get('count100',0))+int(info.get('count50',0))
        args = [info.get('user_id'), info.get('username'), pc, info.get('ranked_score'), info.get('total_score'), info.get('pp_rank'), info.get('level'), info.get('pp_raw'), round(float(info.get('accuracy')),2),info.get('country')]
        result = cur.execute(sql, args)
        conn.commit()
    except:
        conn.rollback()
        traceback.print_exc()

def get_user(uid):
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
                print('insert '+str(uid))
        


def main(start=0, num=1):
    for t in range(num):
        pool = multiprocessing.Pool(processes=30)
        pre_num = t*300+start
        for i in range(30):
            pool.apply_async(get_user, (pre_num+10*i, ))
        pool.close()
        pool.join()
        

if __name__ == "__main__":

    start_time = time.time()
    main(8000000, 10000)
    used_time = time.time()-start_time
    print ("结束,用时:"+ str(used_time))
