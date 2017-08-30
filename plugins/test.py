# -*- coding: utf-8 -*-

import random
import pymysql
import traceback
import json
import requests


rbq_614892339 = set([])
rbq_list_614892339 = {}            
rbq_514661057 = set([])
rbq_list_514661057 = {}

def onQQMessage(bot, contact, member, content):
    #contact :  ctype/qq/uin/nick/mark/card/name 
    #群限制 Q号 614892339
    if contact.ctype == 'group' and contact.qq == '614892339':
        if len(rbq_614892339) > 20:
            rbq_614892339.pop()
        rbq_614892339.add(member.name)
        if content == '!dalou':
            bot.SendTo(contact, 'dalouBot登场!')
        elif content == '!help':
            bot.SendTo(contact, 'dalou只会打爆你!')
        elif content == '!daloudalou':
            msg = 'dalouBot v1.0\n1.rbq\n2.myrbq\n3.setid\n4.myinfo'
            bot.SendTo(contact, msg)
        elif content == '!rbq':
            r = random.choice(list(rbq_614892339))
            msg = '%s 获得了一个 %s 作为rbq' % (member.name, r)
            if rbq_list_614892339.get(member.qq) is None:
                rbq_list_614892339[member.qq] = set([r])
            elif len(rbq_list_614892339[member.qq]) == 5:
                rem_r = random.choice(list(rbq_list_614892339[member.qq]))
                msg = 'rbq太多了,%s 已被抛弃!' % rem_r
                rbq_list_614892339[member.qq].remove(rem_r)
            else:
                rbq_list_614892339[member.qq].add(r)                
            bot.SendTo(contact, msg)
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
            if not setid(member.qq, osuid, member.name, 614892339, osuname):
                bot.SendTo(contact, '绑定失败,dalouBot数据库被玩坏了!')
                return
            bot.SendTo(contact, '绑定成功,使用myinfo查询信息!')
        elif '!myinfo' == content:
            info = get_myinfo(member.qq)
            if not info:
                bot.SendTo(contact, '未绑定,请使用setid!')
                return
            msg = "%s\nosu:%s\nosuid:%s" % (member.name, info[5], info[3])
            bot.SendTo(contact, msg) 
        elif '!getid' in content:
            name = content.split('@')[1]
            res = get_osuinfo_byname(name)
            if not res:
                bot.SendTo(contact, 'name 未绑定osuid')
                return
            msg = "%s\nosu:%s\nosuid:%s" % (name, res[5], res[3])
            bot.SendTo(contact, msg)

    #群限制 Q号 514661057
    if contact.ctype == 'group' and contact.qq == '514661057':
        if len(rbq_514661057) > 20:
            rbq_514661057.pop()
        rbq_514661057.add(member.name)
        if content == '!dalou':
            bot.SendTo(contact, 'dalouBot登场!')
        elif content == '!help':
            bot.SendTo(contact, 'dalou只会打爆你!')
        elif content == '!daloudalou':
            msg = 'dalouBot v1.0\n1.rbq\n2.myrbq\n3.setid\n4.myinfo'
            bot.SendTo(contact, msg)
        elif content == '!rbq':
            r = random.choice(list(rbq_514661057))
            msg = '%s 获得了一个 %s 作为rbq' % (member.name, r)
            if rbq_list_514661057.get(member.qq) is None:
                rbq_list_514661057[member.qq] = set([r])
            elif len(rbq_list_514661057[member.qq]) == 5:
                rem_r = random.choice(list(rbq_list_514661057[member.qq]))
                msg = 'rbq太多了,%s 已被抛弃!' % rem_r
                rbq_list_514661057[member.qq].remove(rem_r)
            else:
                rbq_list_514661057[member.qq].add(r)                
            bot.SendTo(contact, msg)
        elif content == '!myrbq':
            if rbq_list_514661057.get(member.qq) is None or len(rbq_list_514661057.get(member.qq)) == 0:
                bot.SendTo(contact, '你没有rbq醒醒!')
                return
            msg = '%s 有%s个rbq:\n' % (member.name, len(rbq_list_514661057[member.qq]))
            r_list = list(rbq_list_514661057[member.qq])
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
            if not setid(contact.qq, osuid, member.name, 614892339, osuname):
                bot.SendTo(contact, '绑定失败,dalouBot数据库被玩坏了!')
                return
            bot.SendTo(contact, '绑定成功,使用myinfo查询信息!')
        elif '!myinfo' == content:
            info = get_myinfo(contact.qq)
            if not info:
                bot.SendTo(contact, '未绑定,请使用setid!')
                return
            msg = "%s\nosu:%s\nosuid:%s" % (member.name, info[5], info[3])
            bot.SendTo(contact, msg)

    #主号权限

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
        res = requests.get(url, timeout=1)
        if not res:
            return 0
        result = json.loads(res.text)
        uid = result[0]['user_id']
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


def get_osuinfo_byname(name):
    try:
        cur = get_cursor()
        sql = '''
            SELECT * FROM user where name = %s
        '''
        cur.execute(sql, name)
        res = cur.fetchall()
        if not res:
            return 0
        return  res[0]
    except:
        traceback.print_exc()
        return 0
