# -*- coding: utf-8 -*-

import random
import pymysql
import traceback
import json
import requests
import redis
import re
import datetime

rbq_614892339 = set([])
rbq_list_614892339 = {}            
rbq_514661057 = set([])
rbq_list_514661057 = {}
testuser = []

def onQQMessage(bot, contact, member, content):
    #contact :  ctype/qq/uin/nick/mark/card/name 
    #群限制 Q号 614892339
    if contact.ctype == 'group':
        if contact.qq != '614892339' and contact.qq != '514661057':
            return 
        if len(rbq_614892339) > 20:
            rbq_614892339.pop()
        rbq_614892339.add(member.name)
        
        if content == '!help':
            bot.SendTo(contact, 'dalou只会打爆你!')
        elif content == '!dalou':
            msg = 'dalouBot v1.1\n1.rbq(暂时关闭)\n2.myrbq\n3.setid xxx\n4.myinfo\n5.dalou的奸视(new)\n6.check xxx(new)\n7.js 奸视列表\n8.接受功能建议'
            bot.SendTo(contact, msg)
        # elif content == '!rbq':
        #     r = random.choice(list(rbq_614892339))
        #     msg = '%s 获得了一个 %s 作为rbq' % (member.name, r)
        #     if rbq_list_614892339.get(member.qq) is None:
        #         rbq_list_614892339[member.qq] = set([r])
        #     elif len(rbq_list_614892339[member.qq]) == 5:
        #         rem_r = random.choice(list(rbq_list_614892339[member.qq]))
        #         msg = 'rbq太多了,%s 已被抛弃!' % rem_r
        #         rbq_list_614892339[member.qq].remove(rem_r)
        #     else:
        #         rbq_list_614892339[member.qq].add(r)                
        #     bot.SendTo(contact, msg)
        elif content == '!myrbq':
            if rbq_list_614892339.get(member.qq) is None or len(rbq_list_614892339.get(member.qq)) == 0:
                bot.SendTo(contact, '你没有rbq醒醒!')
                return
            msg = '%s 有%s个rbq:\n' % (member.name, len(rbq_list_614892339[member.qq]))
            r_list = list(rbq_list_614892339[member.qq])
            for i,r in enumerate(r_list):
                msg2 = '%s.%s\n' % (str(i+1), r)
                msg += msg2
            msg = msg[0:-1]
            bot.SendTo(contact, msg)
        elif '!setid' in content:
            osuname = content.split(' ')[1]
            osuid = get_osuid(osuname)
            if not osuid:
                bot.SendTo(contact, '绑定失败,dalouBot不想让你绑定!')
                return
            if not setid(member.qq, osuid, member.name, contact.qq, osuname):
                bot.SendTo(contact, '绑定失败,dalouBot数据库被玩坏了!')
                return
            bot.SendTo(contact, '绑定成功,使用myinfo查询信息!')
        elif '!myinfo' == content:
            res = get_myinfo(member.qq)
            if not res:
                bot.SendTo(contact, '未绑定,请使用setid!')
                return
            home_url = 'https://osu.ppy.sh/u/%s' % (res[3])
            msg = "%s\nosu:%s\nosuid:%s\nmoney:%s\nbagnum:%s\n%s" % (member.name, res[5], res[3], res[6], res[7], home_url)
            bot.SendTo(contact, msg) 
        elif '!getid' in content:
            name = content.split('@')[1]
            g = bot.List('group', str(contact.qq))[0]
            name_str = 'card=%s' % name
            qq = bot.List(g, name_str)[0].qq
            res = get_osuinfo_byqq(qq)
            if not res:
                bot.SendTo(contact, name+'未绑定osuid')
                return
            home_url = 'https://osu.ppy.sh/u/%s' % (res[3])
            msg = "%s\nosu:%s\nosuid:%s\n%s" % (name, res[5], res[3], home_url)
            bot.SendTo(contact, msg)
        elif '!set' in content and member.qq == '405622418':
            name = content.split(' ')[1]
            if name not in testuser:
                testuser.append(name)
            bot.SendTo(contact, 'dalouBot奸视列表:'+str(testuser))
        elif '!rem' in content and member.qq == '405622418':
            name = content.split(' ')[1]
            if name in testuser:
                testuser.remove(name)
            bot.SendTo(contact, 'dalouBot奸视列表:'+str(testuser))
        elif '!js' == content:
            if not testuser:
                bot.SendTo(contact, 'dalou没有在奸视任何人')
            else:
                bot.SendTo(contact, 'dalouBot奸视列表:'+str(testuser))
        elif '!check' in content:
            bot.SendTo(contact, 'dalou手动计算中...请骚等!')
            uid = content[7:]
            pp,pp2,maxpp = check_user(uid)
            if not pp:
                bot.SendTo(contact, '没有pp,下一个!')
                return
            msg = '%s\npp:%spp\n预估:%spp\n最大可能:%spp' % (uid,pp,pp2,maxpp)
            bot.SendTo(contact, msg)

    

    #测试
    if contact.ctype == 'buddy' and contact.qq == '405622418':
        if '!setid' in content:
            osuname = content.split(' ')[1]
            osuid = get_osuid(osuname)
            if not osuid:
                bot.SendTo(contact, '绑定失败,dalouBot不想让你绑定!')
                return
            if not setid(contact.qq, osuid, contact.name, 13547, osuname):
                bot.SendTo(contact, '绑定失败,dalouBot数据库被玩坏了!')
                return
            bot.SendTo(contact, '绑定成功,使用myinfo查询信息!')
        elif '!myinfo' == content:
            info = get_myinfo(contact.qq)
            if not info:
                bot.SendTo(contact, '未绑定,请使用setid!')
                return
            msg = "%s\nosu:%s\nosuid:%s" % (contact.name, info[5], info[3])
            bot.SendTo(contact, msg)
        elif '!test' == content:
            get_recent_plays('heisiban')
        elif '!set' in content:
            testuser.append(content.split(' ')[1])
            bot.SendTo(contact, '用户切换:'+testuser)


#定时任务
from qqbot import qqbotsched
@qqbotsched(minute='0-59/1')
def mytask(bot):
    if not testuser:
        return
    gl = bot.List('group', '614892339')
    if gl is not None:
        for group in gl:
            for t in testuser:
                msg = get_recent_plays(t)
                if msg:
                    bot.SendTo(group, msg)

r = redis.Redis(host='127.0.0.1', port=6379)
def get_recent_plays(osuname):
    try:
        osuid = get_osuid(osuname)
        url = 'https://osu.ppy.sh/pages/include/profile-history.php?u=%s&m=0' % osuid
        res = get_url(url)
        while not res:
            res = get_url(url)

        value = re.compile(r"<time class='timeago' datetime.*?>(.*?)</time> - <a target='_top' href=.*?>(.*?)</a> (.*?)<br/>")
        values = value.search(res.text)
        print(values.group())
        if not values:
            return 0
        #redis处理判断是否更新
        key = 'osu_recent:%s' % osuid
        recent = r.get(key)
        if recent and bytes.decode(recent) == values.group(1):
            return 0
        else:
            r.set(key, values.group(1), 3600 * 24)
            #UTC时间转换
            utc_time = datetime.datetime.strptime(values.group(1)[0:-4],'%Y-%m-%d %H:%M:%S')
            now_time = utc_time + datetime.timedelta(hours=8)
            msg = '%s在%s偷偷打了张图:\nmap:%s\nscore:%s' % (osuname,now_time,values.group(2),values.group(3))
            return msg
    except:
        traceback.print_exc()
        return 0

def get_url(url, timeout=1):
    try:
        res = requests.get(url, timeout=timeout)
        return res
    except:
        print('超时..')
        return 0

conn = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu', charset='utf8')
osu_api_key = 'b68fc239f6b8bdcbb766320bf4579696c270b349'
def get_cursor():
    return conn.cursor()

def setid(qq, osuid, name, groupid, osuname):
    try:
        cur = get_cursor()
        sql = '''
            insert into user
                (qq, osuid, name, groupid, osuname) 
            values
                (%s,%s,%s,%s,%s)
            on duplicate key update
                osuid = %s, osuname = %s, name = %s
        '''
        args = [qq, osuid, name, groupid, osuname, osuid, osuname, name]
        result = cur.execute(sql, args)
        conn.commit()
        return 1
    except:
        conn.rollback()
        traceback.print_exc()
        return 0

def get_osuid(osuname):
    try:
        url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osu_api_key, osuname)
        res = get_url(url)
        c = 0
        while res == 0:
            if c > 5:
                return 0
            else:
                res = get_url(url)
                c += 1
        if not res:
            return 0
        result = json.loads(res.text)
        uid = result[0]['user_id']
        print(uid)
        return uid
    except:
        traceback.print_exc()
        return 0

def get_myinfo(qq):
    try:
        cur = get_cursor()
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


def get_osuinfo_byqq(qq):
    try:
        cur = get_cursor()
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

def get_bp_and_pp(uid):
    try:
        url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osu_api_key, uid)
        res = get_url(url)
        c = 0
        while res == 0:
            if c > 5:
                return 0,0
            else:
                c += 1
                res = get_url(url)
        if res == 0:
            return 0,0
        result = json.loads(res.text)
        if not result:
            return 0,0
        pp = result[0]['pp_raw']

        url2 = 'https://osu.ppy.sh/api/get_user_best?k=%s&u=%s' % (osu_api_key, uid)
        res = get_url(url2)
        c = 0
        while res == 0:
            if c > 5:
                return 0,0
            else:
                c += 1
                res = get_url(url2)
        if res == 0:
            return 0,0
        result = json.loads(res.text)
        return pp,result
    except:
        traceback.print_exc()
        return 0,0


def check_user(uid):
    try:
        pp,res = get_bp_and_pp(uid)
        if not pp:
            return 0,0,0
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
            if res[0] is None:
                continue
            # print(res)
            if res[0] >= maxpp:
                maxpp = res[0]
            if res[1] != 1: 
                count_num += 1
                count_pp += res[0]
        if count_num == 0:
            yugu_pp = pp
        else:
            yugu_pp = round(count_pp/count_num)
        return pp,yugu_pp,round(maxpp)
    except:
        traceback.print_exc()
        return 0,0,0
