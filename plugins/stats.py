# -*- coding: utf-8 -*-
import pymysql  
import time
import json
import requests
import threading
import datetime
import traceback
from qqbot import qqbotsched

group_list = ['614892339','514661057','641236878']

def onInit(bot):
    t = threading.Thread(target=sched_day_insert, args=())
    t.start()

def onQQMessage(bot, contact, member, content):
    if contact.ctype == 'group':
        if contact.qq not in group_list:
            return

        #通用线程函数
        t = threading.Thread(target=_method, args=(bot, contact, member, content))
        t.start()

        return

def _method(bot, contact, member, content):

    if content == '!s':
        msg = get_stats(member.qq)
        bot.SendTo(contact, msg)
        return
    elif content == '!status':
        update_status(bot, contact, member, content)
        return

def sched_day_insert():
    o = osu()
    try:
        o.time_insert()
    except:
        print('定时任务出错')
        traceback.print_exc()

def get_stats(qq):
    o = osu()
    res = o.get_myinfo(qq)
    if not res:
        return '未绑定,请使用setid!'
    return o.osu_stats(res[5])

def update_status(bot, contact, member, content):
    o = osu()
    uplist = o.today_updates()
    bindlist = o.get_user_list_fromDB()
    uplist_new = data_format(uplist)
    bindlist_new = data_format(bindlist)
    len_up = len(set(uplist))
    len_bind = len(set(bindlist))
    auto_flag = 0
    error_user = set(bindlist_new) - set(uplist_new)
    len_error = len(error_user)
    # print('up的数量:%s,bind的数量:%s,error的数量:%s'%(len_up,len_bind,len_error))
    if len_error == 0:
        msg = '今日更新数据无误,更新条数:%s' % len_up
    elif len_error < 0:
        msg = '今日更新数据异常,更新条数:%s大于绑定用户数:%s' % (len_up,len_bind)
    else:
        msg = '今日更新条数:%s,未更新数量:%s' % (len_up,len_error)
        if len_bind-len_up > 5:
            msg += ',开始自动更新剩余用户...'
            print('自动更新列表:%s'%error_user)
            auto_flag = 1
        else:
            msg += ',这几个用户被放弃了:%s' % list(error_user)
    bot.SendTo(contact, msg)
    if auto_flag:
        error_user = list(error_user)
        o._inerts_many(error_user)
        bot.SendTo(contact, '自动插入完成!')
        # 自动清理
        if o.del_users(error_user):
            bot.SendTo(contact, '如下列表用户被自动清理:%s'%error_user)
        else:
            bot.SendTo(contact, '自动清理异常!')

    return

def data_format(lists):
    res_list = []
    for l in lists:
        new_data = l.lower()
        new_data = new_data.replace('_',' ')
        new_data = new_data.replace('%20',' ')
        res_list.append(new_data)
    return res_list

class osu:

    def __init__(self):
        self.con = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu')
        self.headers = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, br',
            'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection' : 'keep-alive',
            'Cookie' : '__cfduid=d0f839d6873527f32fe3b9dc8426362481508213944; XSRF-TOKEN=DMTtpVyEN1VvSFglE9tFYui1BkrkcuHMxh9bB1IH; osu_session=eyJpdiI6IktyNWxtVFJVNmwwcGdoS05FK21yYVE9PSIsInZhbHVlIjoiZ0t3Z0pzYUoxbXJcL1J6Mm10UmM0WG51c1Y0RTg3R0ZrNVRtcVJCSWV0bytwZjQ2OFwvaTI1MFI5Z2x5bkx3b0RrbWlyclV4U1wvQmtxQU5EY01VN2FcL0NnPT0iLCJtYWMiOiJlZWJhZTU0NzgzNzM4MGQxMmJlYTY0NjA2NTE0NDQyYmJkNzg1MDQyNWE3YjU0OTUyMGZmOGQwOGE5ZTM5YjQ0In0%3D; _ga=GA1.2.987670012.1508213952; __utma=226001156.987670012.1508213952.1508238423.1509076921.2; __utmz=226001156.1508238423.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cf_clearance=ffcabb88813877be171e47f35a2c99cbb8c1146a-1509076917-31536000; __utmb=226001156.3.10.1509076921; _gid=GA1.2.38718716.1509076975',
            'Host'  :  'osu.ppy.sh',
            'Upgrade-Insecure-Requests' :  '1',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        }
        self.osu_api_key = 'b68fc239f6b8bdcbb766320bf4579696c270b349'

    def get_con(self):
        self.con = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu')

    def get_cursor(self):
        return self.con.cursor()

    def get_myinfo(self, qq):
        '''qq绑定信息'''
        try:
            cur = self.get_cursor()
            sql = '''
                SELECT * FROM user where qq = %s
            '''
            cur.execute(sql, qq)
            res = cur.fetchall()
            if not res:
                return 0
            return  res[0]
        except:
            traceback.print_exc()
            return 0

    def today_updates(self):
        '''今日更新数据'''
        cur = self.get_cursor()
        sql = '''
            SELECT username FROM user2 where time=%s
        '''
        today = self.get_today()
        cur.execute(sql, today)
        res = cur.fetchall()
        ret = [r[0] for r in res]
        return  ret

    def del_users(self, users):
        '''清理用户'''
        try:
            cur = self.get_cursor()
            sql = '''
                DELETE FROM user where osuname in (%s)
            '''
            in_p = ','.join(map(lambda x: '%s', users))
            sql = sql % in_p
            res = cur.execute(sql, users)
            self.con.commit()
            return res
        except:
            self.con.rollback()
            traceback.print_exc()
            return 0


    def __del__(self):
        self.con.close()

    def insert_user(self,*user):
        try:
            cur = self.get_cursor()
            sql = 'insert into user2(username,pp,acc,pc,rank,tth,time) values(%s,%s,%s,%s,%s,%s,%s)'
            result = cur.execute(sql,tuple(user))
            print('插入数据结果:'+str(result))
            self.con.commit()
        except:
            self.con.rollback()
            pass

    def get_user_fromDB(self,username,**kwargs):
        cur = self.get_cursor()
        if not kwargs:
            if self.is_today():
                time = self.get_today()
            else:
                time = self.get_yes()
            sql = 'select * from user2 where username=%s and time>=%s limit 1'
            print('查询时间:'+time)
        result = cur.execute(sql,(username,time))
        print('查询数据结果:'+str(result))
        if result:
            user_info = cur.fetchall()
            #print(user_info)
            return user_info
        else:
            return ''

    def get_user_list_fromDB(self):
        print('查询用户列表..')
        cur = self.get_cursor()
        sql = 'SELECT osuname from user GROUP BY osuname'
        result = cur.execute(sql)
        user_list = cur.fetchall()
        ret = [r[0] for r in user_list]
        return  ret
        return user_list

    def exist_user(self,uid):
        #print('查询用户是否存在')
        cur = self.get_cursor()
        sql = 'SELECT 1 from user2 where username="'+uid+'" limit 1'
        result = cur.execute(sql)
        user_list = cur.fetchall()
        return user_list

    def check_today_user(self,uid,time):
        print('%s已存在今日数据'%uid)
        cur = self.get_cursor()
        sql = '''SELECT 1 from user2 where username=%s and time = %s limit 1'''
        result = cur.execute(sql, [uid,time])
        user_list = cur.fetchall()
        return user_list

    def osu_stats(self,uid):
        try:
            print('查询用户:'+uid)
            res = requests.get('https://osu.ppy.sh/api/get_user?k=%s&u=%s'%(self.osu_api_key,str(uid)),headers=self.headers,timeout=5)

            result = json.loads(res.text)
            if not result:
                return ''
            #print(result)
            result = result[0]
            username = result['username']
            pp = result['pp_raw']
            in_pp = float(pp)
            #print(in_pp)
            rank = result['pp_rank']
            acc1 = round(float(result['accuracy']),2)
            #print(acc1)
            acc = str(acc1)
            pc =  result['playcount']
            count300 = result['count300']
            count100 = result['count100']
            count50 = result['count50']
            tth = eval(count300)+eval(count50)+eval(count100)
            tth_w = str(tth//10000)
            #与本地数据比较
            u_db_info = self.get_user_fromDB(uid)
            if u_db_info:
                info = u_db_info[0]
                add_pp = str(round(in_pp - float(info[2]),2))
                add_rank = info[5] - int(rank)
                if add_rank >= 0:
                    add_rank = '+'+str(add_rank)
                else:
                    add_rank = str(add_rank)
                add_acc =  round(acc1 - float(info[3]),2)
                if add_acc >=0.0:
                    add_acc = '+'+str(add_acc)
                else:
                    add_acc = str(add_acc)
                add_pc = str(int(pc) - int(info[4]))
                add_tth = str(tth - int(info[6]))
                d = username+'\n'+pp+'pp(+'+add_pp+')\n'+'rank: '+rank+'('+add_rank+')\n'+'acc : '+acc+'%('+add_acc+')\n'+'pc  : '+pc+'pc(+'+add_pc+')\n'+'tth  : '+tth_w+'w(+'+add_tth+')'
            else:
                d = username+'\n'+pp+'pp(+0)\n'+'rank: '+rank+'(+0)\n'+'acc : '+acc+'%(+0)\n'+'pc  : '+pc+'pc(+0)\n'+'tth  : '+tth_w+'w(+0)'
            #in_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            is_exist = self.exist_user(uid)
            if not is_exist:
                print('用户不存在,进行插入')
                #检测时间段0-9点
                if self.is_today():
                    in_time = self.get_today()
                else:
                    in_time = self.get_yes()
                self.insert_user(username,in_pp,acc1,pc,rank,tth,in_time)
            return d
        except:
            traceback.print_exc()

    def getU(self,uid):
        try:
            print('获取用户:'+uid)
            res = requests.get('https://osu.ppy.sh/api/get_user?k=%s&u=%s'%(self.osu_api_key,str(uid)),headers=self.headers,timeout=2)
        except:
            print('获取失败:'+uid)
            res = ''
        return res


    def get_today(self):
        today = datetime.date.today()
        return str(today)+' 9:00:00'


    def get_today(self):
        today = datetime.date.today()
        return str(today)+' 9:00:00'

    def get_yes(self):
        now = datetime.datetime.now()
        date = now - datetime.timedelta(days = 1)
        return date.strftime('%Y-%m-%d')+' 9:00:00'

    def is_today(self):
        #0昨天 1今天
        now_hour = time.strftime("%H%M%S")
        cmp_hour = 90000
        if int(now_hour) - cmp_hour < 0:
            return 0
        else:
            return 1

    def is_insert_today(self):
        cur = self.get_cursor()
        time = self.get_today()
        sql = 'SELECT 1 from user2 where time="'+time+'" LIMIT 1'
        result = cur.execute(sql)
        user_list = cur.fetchall()
        return user_list

    def auto_inert(self):
        self._inerts_many(self.get_user_list_fromDB())

    def _inerts_many(self, userlist):
        try:
            today = datetime.date.today()
            in_time = str(today)+' 9:00:00'
            for uid in userlist:
                res = self.getU(uid)
                get_num = 0
                while not res:
                    if get_num < 5:
                        get_num += 1
                        res = self.getU(uid)
                    else:
                        break 
                if not res:
                    continue

                result = json.loads(res.text)  
                if result:         
                    result = result[0]
                else:
                    continue
                username = result['username']
                pp = result['pp_raw']
                in_pp = float(pp)
                rank = result['pp_rank']
                acc1 = round(float(result['accuracy']),2)
                pc =  result['playcount']
                count300 = result['count300']
                count100 = result['count100']
                count50 = result['count50']
                tth = eval(count300)+eval(count50)+eval(count100)
                self.insert_user(username,in_pp,acc1,pc,rank,tth,in_time)
                print(uid+'插入成功')
        except:
            print('auto_inert错误')
            traceback.print_exc()

    def insert_forday(self):
        print('开始执行定时插入任务')
        self.auto_inert()
        print('定时插入任务结束')

    def time_insert(self):
        '''定时任务'''
        today = datetime.date.today()
        now_hour = time.strftime('%H%M%S')
        is_run = int(now_hour) - 90000
        if  is_run < 0:
            print('延时执行')
            now = datetime.datetime.now()
            stats = datetime.datetime(today.year,today.month,today.day,9,0,0)
            delay = (stats - now).seconds
            print(delay)
            s = sched.scheduler(time.time, time.sleep)
            s.enter(delay,0,self.insert_forday,())
            s.run()
        else:
            print('超过时间,立即执行定时任务')
            if not self.is_insert_today():
                print('今日数据不存在,准备抓取...')
                self.insert_forday()
            else:
                print('今日数据已存在,不需要抓取')
            #self.insert_forday()
            print('定时任务结束')

