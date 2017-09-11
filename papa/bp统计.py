import urllib
import traceback
import requests
import json
import pymysql

def get_url(url, timeout=3):
    try:
        res = requests.get(url, timeout=timeout)
        return res
    except:
        print('超时..')
        traceback.print_exc()
        return 0

def get_bp_and_pp(uid):
    try:
        url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osu_api_key, uid)
        res = get_url(url)
        while not res:
            res = get_url(url)
        if res == 0:
            return 0,0
        result = json.loads(res.text)
        if not result:
            return 0,0
        pp = result[0]['pp_raw']

        url2 = 'https://osu.ppy.sh/api/get_user_best?k=%s&u=%s' % (osu_api_key, uid)
        res = get_url(url2)
        while not res:
            res = get_url(url)
        if res == 0:
            return 0,0
        result = json.loads(res.text)
        return pp,result
    except:
        traceback.print_exc()
        return 0,0


conn = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu', charset='utf8')
osu_api_key = 'b68fc239f6b8bdcbb766320bf4579696c270b349'
def get_cursor():
    return conn.cursor()

def check_user(uid):
    try:
        pp,res = get_bp_and_pp(uid)
        if not pp:
            return 0
        count_num = 0
        count_pp = 0
        maxpp = 0
        for r in res:
            maxcombo1 = int(r['maxcombo']) - 10
            maxcombo2 = int(r['maxcombo']) + 10
            c50 = float(r['count50'])
            c100 = float(r['count100'])
            c300 = float(r['count300'])
            cmiss = float(r['countmiss'])
            acc = round((c50*50+c100*100+c300*300)/(c50+c100+c300+cmiss)/300*100,2)
            acc1 = acc - 1
            acc2 = acc + 1
            args = [r['beatmap_id'], r['enabled_mods'], maxcombo1, maxcombo2, acc1, acc2]
            # print(args)
            cur = get_cursor()
            sql='''
                SELECT avg(u.pp_raw),count(1) from osu_bp b INNER JOIN osu_user u on b.user_id=u.user_id where b.beatmap_id = %s and b.mods=%s and b.maxcombo BETWEEN %s and %s and b.acc BETWEEN %s and %s
            '''
            cur.execute(sql, args)
            res = cur.fetchall()
            res = res[0]
            print(res)
            if res[0] > maxpp:
                maxpp = res[0]
            count_num += 1
            count_pp += res[0]
        print(pp)
        print(count_pp/count_num)
        print(maxpp)
    except:
        traceback.print_exc()
        return 0

# check_user('ca2e2e')




def write(f='BpRank.txt'):
    cur = get_cursor()
    sql='''
        SELECT beatmap_id,avg(acc),avg(pp),count(1) num from osu_bp WHERE beatmap_id in (SELECT beatmap_id FROM(SELECT beatmap_id from osu_bp GROUP BY beatmap_id ORDER BY count(1) desc LIMIT 10) as t) GROUP BY beatmap_id ORDER BY num desc
    '''
    cur.execute(sql)
    res = cur.fetchall()

    print ("creating log ..")
    with open(f,'a') as f:
        f.write('***********BP统计结果***********\n\n')
        for index,i in enumerate(res):
            beatmap = getBeatMap(i[0])
            while not beatmap:
                beatmap = getBeatMap(i[0])
            maxid = i[0]
            acc = round(i[1])
            pp = round(i[2])
            num = i[3]
            title = beatmap[0].get('title')
            star = beatmap[0].get('difficultyrating')
            star = round(float(star),2)#小数点精度
            artist = beatmap[0].get('artist')
            version = beatmap[0].get('version')
            line = '%s.%s - %s [%s]\nbp出现次数:%s  平均pp:%s  平均acc:%s\n\n' % (index+1,artist,title,version,num,pp,acc)
            f.write(line)

        f.write('\n***********BP统计结果***********\n\n\n')
    print ("finish!")

def getBeatMap(bid=814293):
    try:
        res = requests.get('https://osu.ppy.sh/api/get_beatmaps?k=b68fc239f6b8bdcbb766320bf4579696c270b349&b='+str(bid),timeout=2)
        print ('getting beatmap:'+str(bid))
        result = json.loads(res.text)
        
    except:
        traceback.print_exc()
        print ('error beatamp:'+str(bid))
        result=[]

    return result

# write()


