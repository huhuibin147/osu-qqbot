# -*- coding: utf-8 -*-
import os
import time
import random
import pymysql
import traceback
import threading
import json
import requests
import redis
import html.parser
import os
import re
import datetime
import math
import multiprocessing

import mods
import Config
import post2site
import qqbot.facemap

from cbot import get_chatlog
from cbot import seg_train
from cbot import segment
from gensim.models import word2vec
from gensim import models

rbq_614892339 = set([])
rbq_list_614892339 = {}            
rbq_514661057 = set([])
rbq_list_514661057 = {}
testuser = []
msglist = set([])
speak_flag = [1]
worlds_num = [10000]
methods = {}


group_list = ['614892339','514661057','641236878']

def onStartupComplete(bot):
    # 启动完成时被调用
    t_up_speak = threading.Thread(target=speak_task,args=())
    t_up_speak.start()
    t_train = threading.Thread(target=chat_train,args=())
    t_train.start()


def onInterval(bot):
    # 每隔 5 分钟被调用
    t_up_speak = threading.Thread(target=speak_task,args=())
    t_up_speak.start()

def onQQMessage(bot, contact, member, content):
    #contact :  ctype/qq/uin/nick/mark/card/name 
    if contact.ctype == 'group':
        if contact.qq not in group_list:
            return

        #通用线程函数
        t = threading.Thread(target=_method, args=(bot, contact, member, content))
        t.start()

        return

    
def _method(bot, contact, member, content):

    # msg收集
    if content and len(content) < 30 and member.qq != '1677323371':
        if len(msglist) > worlds_num[0]:
            msglist.pop()
        msglist.add(content)

    # rbq列表收集
    if len(rbq_614892339) > 50:
        rbq_614892339.pop()
    rbq_614892339.add(member.name)

    # speak
    if speak_flag[0] and member.qq != '1677323371' and random.randint(0,100) > 99:
        msg = random.sample(msglist,1)
        print('回复speak触发!')
        bot.SendTo(contact, msg[0])

    if '@ME' in content:
        msg = random.sample(msglist,1)[0]
        bot.SendTo(contact, msg)
        return
    # if content == '!help':
    #     bot.SendTo(contact, 'dalou只会打爆你!')
    elif content == '!bq':
        bot.SendTo(contact, '/'+random.choice(qqbot.facemap.faceText))
        return
    elif content == '!cnt':
        bot.SendTo(contact, 'interBot目前的词库量:%s,上限:%s' % (len(msglist), worlds_num[0]))
        return
    elif '!setcnt' in content and member.qq == '405622418':
        if int(content[8:]) < len(msglist):
            msg = '调整失败,上限小于当前词库量'
        else:
            worlds_num[0] = int(content[8:])
            msg = 'interBot目前的词库量:%s,上限调整为:%s' % (len(msglist), worlds_num[0])
        bot.SendTo(contact, msg)
        return
    elif content == '!stopsp':
        speak_flag[0] = 0
        bot.SendTo(contact, '啊啊啊被淹了!')
        return
    elif content == '!startsp':
        speak_flag[0] = 1
        bot.SendTo(contact, 'Bot我又回来了!')
        return
    elif content == '!inter':
        msg = get_help()
        bot.SendTo(contact, msg)
        return
    elif content == '!rbq':
        # 控制频率
        # key = 'get_rbq:%s' % member.qq
        # value = redis_client.get(key)
        # if not value:
        #     redis_client.setex(key, 1, 60)
        # else:
        #     bot.SendTo(contact, '这1分钟你只能成为别人的rbq!!!')
        #     return
        # r = random.choice(list(rbq_614892339))
        # msg = '%s 获得了一个 %s 作为rbq' % (member.name, r)
        # if rbq_list_614892339.get(member.qq) is None:
        #     rbq_list_614892339[member.qq] = set([r])
        # elif len(rbq_list_614892339[member.qq]) == 5:
        #     rem_r = random.choice(list(rbq_list_614892339[member.qq]))
        #     msg = 'rbq太多了,%s 已被抛弃!' % rem_r
        #     rbq_list_614892339[member.qq].remove(rem_r)
        # else:
        #     rbq_list_614892339[member.qq].add(r)                
        # bot.SendTo(contact, msg)
        bot.SendTo(contact, '被inter偷偷关了!')
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
        return
    elif '!setid' in content:
        osuname = content.split(' ')[1]
        osuid = get_osuid(osuname)
        if not osuid:
            bot.SendTo(contact, '绑定失败,interBot不想让你绑定!')
            return
        if not setid(member.qq, osuid, member.name, contact.qq, osuname):
            bot.SendTo(contact, '绑定失败,interBot数据库被玩坏了!')
            return
        bot.SendTo(contact, '绑定成功,使用myinfo查询信息!')
        return
    elif '!myinfo' == content:
        res = get_myinfo(member.qq)
        if not res:
            bot.SendTo(contact, '未绑定,请使用setid!')
            return
        home_url = 'https://osu.ppy.sh/u/%s' % (res[3])
        msg = "%s\nosu:%s\nosuid:%s\nmoney:%s\nbagnum:%s\n%s" % (member.name, res[5], res[3], res[6], res[7], home_url)
        bot.SendTo(contact, msg) 
        return
    elif '!getid' in content:
        content = content.rstrip()
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
        return
    elif '!setjs' in content and member.qq == '405622418':
        name = content.split(' ')[1]
        if name not in testuser:
            testuser.append(name)
        bot.SendTo(contact, 'interBot奸视列表:'+str(testuser))
        return
    elif '!remjs' in content and member.qq == '405622418':
        name = content.split(' ')[1]
        if name in testuser:
            testuser.remove(name)
        bot.SendTo(contact, 'interBot奸视列表:'+str(testuser))
        return
    elif '!js' == content:
        if not testuser:
            bot.SendTo(contact, 'inter没有在奸视任何人')
        else:
            bot.SendTo(contact, 'interBot奸视列表:'+str(testuser))
        return
    elif '!check' in content:
        # bot.SendTo(contact, 'inter手动计算中...请骚等!')
        uid = content[7:]
        #取qq绑定
        if not uid:
            res = get_osuinfo_byqq(member.qq)
            if not res:
                bot.SendTo(contact, member.name+'未绑定osuid,请使用setid!')
                return
            uid = res[5]
        pp,pp2,maxpp = check_user(uid)
        if not pp:
            bot.SendTo(contact, '没有pp,下一个!')
            return
        msg = '%s\npp:%spp\ninter手算:%spp\n目前潜力:%spp' % (uid,pp,pp2,maxpp)
        bot.SendTo(contact, msg)
        return
    elif '!test' in content:
        uid = content[6:]
        #取qq绑定
        if not uid:
            res = get_osuinfo_byqq(member.qq)
            if not res:
                bot.SendTo(contact, member.name+'未绑定osuid,请使用setid!')
                return
            uid = res[5]
        msg = health_check(uid)
        bot.SendTo(contact, msg)
        return
    elif '!bbp' in content:
        uid = content[5:]
        #取qq绑定
        if not uid:
            res = get_osuinfo_byqq(member.qq)
            if not res:
                bot.SendTo(contact, member.name+'未绑定osuid,请使用setid!')
                return
            uid = res[5]
        msg = get_bp_info(uid)
        bot.SendTo(contact, msg)
        return
    elif '!sp' == content:
        msg = get_xinrenqun_replay()
        bot.SendTo(contact, msg)
        return
    elif '!skill' in content:
        uid = content[6:]
        #取qq绑定
        if not uid:
            res = get_osuinfo_byqq(member.qq)
            if not res:
                bot.SendTo(contact, member.name+'未绑定osuid,请使用setid!')
                return
            uid = res[5]
        msg = get_skill(uid)
        bot.SendTo(contact, msg)
        return
    elif '!vssk' in content:
        ulist = content[6:].split(',')
        if len(ulist) == 1:
            #取qq绑定
            res = get_osuinfo_byqq(member.qq)
            if not res:
                bot.SendTo(contact, member.name+'未绑定osuid,请使用setid!')
                return
            u1 = res[5]
            u2 = content[6:]
        elif len(ulist) == 2:
            u1 = ulist[0]
            u2 = ulist[1]
        else:
            bot.SendTo(contact, '不想理你!')
        msg = skill_vs(u1,u2)
        bot.SendTo(contact, msg)
        return
    elif '!upage' in content:
        slist = content[7:].split(',')
        if len(slist) == 1:
            page = 1
        else:
            page = int(slist[1])
        msg = get_userpage(slist[0], page)
        bot.SendTo(contact, msg)
        return
    elif '!card' in content:
        uid = content[6:]
        #取qq绑定
        if not uid:
            res = get_osuinfo_byqq(member.qq)
            if not res:
                bot.SendTo(contact, member.name+'未绑定osuid,请使用setid!')
                return
            uid = res[5]
        msg = get_card_msg(uid)
        bot.SendTo(contact, msg)
        return
    elif '!map' in content:
        uid = content[5:]
        #取qq绑定
        if not uid:
            res = get_osuinfo_byqq(member.qq)
            if not res:
                bot.SendTo(contact, member.name+'未绑定osuid,请使用setid!')
                return
            uid = res[5]
        # bot.SendTo(contact, 'inter去ppy找图了,请骚等...')
        msg = tuijian(uid)
        bot.SendTo(contact, msg)
        return
    elif '新番' == content:
        msg = get_bangumi(bot, contact, num = 3)
        bot.SendTo(contact, msg)
        return
    elif '新番排行' == content:
        msg = get_bangumi_rank(bot, contact, num = 5)
        bot.SendTo(contact, msg)
        return
    elif 'osu' == content:
        w = random.choice(list(word_list))
        msg = w + ':' + Config.osu_words[w]
        bot.SendTo(contact, msg)
        return
    elif '!pk' in content:
        osuname2 = content[4:]
        res = get_osuinfo_byqq(member.qq)
        osuname = res[5]
        if osuname == osuname2:
            bot.SendTo(contact, '你想爆了自己???')
            return
        if not res:
            bot.SendTo(contact, member.name+'未绑定osuid,请使用setid!')
            return
        else:
            res2 = get_from_osu_user(osuname2)
            if not res2:
                bot.SendTo(contact, '这个人不在池中拒绝pk')
                return
            num = random.randint(0,100)
            if num > 49:
                msg = '%s %s %s!' %(osuname, random.choice(att_type), osuname2)
                pk_count(osuname, osuname2)
            else:
                msg = '%s %s %s!' %(osuname2, random.choice(att_type), osuname)
                pk_count(osuname2, osuname)
            bot.SendTo(contact, msg)
            return
    elif '!zj' == content:
        res = get_osuinfo_byqq(member.qq)
        if not res:
            bot.SendTo(contact, member.name+'未绑定osuid,请使用setid!')
            return
        uid = res[5]
        rec = get_pk_count(uid)
        if rec == -1:
            msg = '战绩系统被玩坏了!!!'
        else:
            rate = round((rec[0]/(rec[0]+rec[1])*100),2)
            msg = "%s's 战绩\n胜:%s\n负:%s\n胜率:%s%%" % (uid, rec[0], rec[1], rate)
        bot.SendTo(contact, msg)
        return
    elif '!win' == content:
        ranklist = get_pk_rank(type=1)
        print (ranklist)
        if ranklist == -1:
            msg = '战绩系统被玩坏了!!!'
        elif len(ranklist) == 0: 
            msg = '战绩旁空空,你们快打一架!'
        else:
            msg = 'winner榜\n'
            for i,r in enumerate(ranklist):
                msg += '%s.%s  %s胜\n' % (i+1, r[0], r[1][0])
        bot.SendTo(contact, msg[:-1])
        return
    elif '!lose' == content:
        ranklist = get_pk_rank(type=2)
        print (ranklist)
        if ranklist == -1:
            msg = '战绩系统被玩坏了!!!'
        elif len(ranklist) == 0: 
            msg = '战绩旁空空,你们快打一架!'
        else:
            msg = 'loser榜\n'
            for i,r in enumerate(ranklist):
                msg += '%s.%s  %s败\n' % (i+1, r[0], r[1][1])
        bot.SendTo(contact, msg[:-1])
        return
    elif '!kw' in content:
        try:
            key = content[4:]
            segmodel = methods['segmodel']
            res = segmodel.most_similar(key,topn=5)
            msg = "%s's 相关词\n" % key
            for idx,item in enumerate(res):
                msg += '%s.%s %s\n' % (idx+1, key, item[0])
            bot.SendTo(contact, msg[:-1])
        except:
            bot.SendTo(contact, '%s不在interbot的词汇表中' % key)
        return
    elif '!trainwords' == content and member.qq == '405622418':
        try:
            bot.SendTo(contact, '啊啊啊!interbot被抓去训练了!')
            chat_train(check_rds=True)
            bot.SendTo(contact, 'interbot感觉还行,训练归来!')
        except:
            traceback.print_exc()
            bot.SendTo(contact, 'interbot感觉不对劲,训练异常!')
        return

    elif '!restart' == content and member.qq == '405622418':
        os.system('qq restart')
        bot.SendTo(contact, 'inter5秒后重启...')
        return
    elif '!stop' == content and member.qq == '405622418':
        os.system('qq stop')
        bot.SendTo(contact, 'inter被迫下班了...')
        return
    elif '!shutdownpc' == content and member.qq == '405622418':
        os.system('shutdown -s -t 60')
        bot.SendTo(contact, 'inter 60秒后关机跑路...')
        return
    elif '!load' in content and member.qq == '405622418':
        plug = content[6:]
        os.system('qq plug '+plug)
        bot.SendTo(contact, '插件热加载成功!')
        return
    elif '今日看番' == content:
        get_bangumi_timeline(bot, contact, 2)
        return
    elif '明日看番' == content:
        get_bangumi_timeline(bot, contact, 3)
        return
    elif '昨日看番' == content:
        get_bangumi_timeline(bot, contact, 1)
        return
    # elif '!qx' in content:
    #     uid = content[4:]
    #     #取qq绑定
    #     if not uid:
    #         res = get_osuinfo_byqq(member.qq)
    #         if not res:
    #             bot.SendTo(contact, member.name+'未绑定osuid,请使用setid!')
    #             return
    #         uid = res[5]
    #     get_osu_qx(bot, contact, uid)
    #     return
    elif '!path' == content:
        bot.SendTo(contact, os.getcwd())
        return


def pk_count(winer, loser):
    # 战绩统计
    try:
        key = 'pk_rec'
        pk_rec = redis_client.get(key)
        if not pk_rec:
            pk_rec = {}
        else:
            pk_rec = json.loads(pk_rec)
        winer_rec = pk_rec.get(winer)
        if winer_rec:
            winer_rec[0] += 1
        else:
            pk_rec[winer]=[1,0]

        loser_rec = pk_rec.get(loser)
        if loser_rec:
            loser_rec[1] += 1
        else:
            pk_rec[loser]=[0,1]

        # print (pk_rec)
        
        redis_client.setex(key, json.dumps(pk_rec), 3600*60)
    except:
        traceback.print_exc()

def get_pk_count(user):
    # 战绩查询
    try:
        key = 'pk_rec'
        pk_rec = redis_client.get(key)
        if not pk_rec:
            pk_rec = {}
        else:
            pk_rec = json.loads(pk_rec)
        user_rec = pk_rec.get(user, [0,0])
        return user_rec
    except:
        traceback.print_exc()
        return -1

def get_pk_rank(type=1, num=5):
    # 战绩排行查询  1-win 2-lose
    try:
        key = 'pk_rec'
        ranklist = []
        pk_rec = redis_client.get(key)
        if not pk_rec:
            pk_rec = []
        else:
            pk_rec = json.loads(pk_rec)
        if type == 1:
            sort_pk = sorted(pk_rec.items(), key=lambda d:d[1][0], reverse=True)
        elif type == 2:
            sort_pk = sorted(pk_rec.items(), key=lambda d:d[1][1], reverse=True)
        for i in range(num):
            ranklist.append(sort_pk[i])
        return ranklist
    except:
        traceback.print_exc()
        return -1

att_type = ['一脚踢爆了','单手打爆了','用脚打爆了','单戳解决了','acc碾压了','一串连打带走了','随手fc解决了','高速全屏跳带走了']


#定时任务-监视任务
from qqbot import qqbotsched
@qqbotsched(minute='0-59/1')
def mytask(bot):
    if not testuser:
        return
    gl = bot.List('group', '514661057')#614892339
    if gl is not None:
        for group in gl:
            for t in testuser:
                msg = get_recent_plays(t)
                if msg:
                    bot.SendTo(group, msg)


#定时任务-讲话任务1
from qqbot import qqbotsched
@qqbotsched(second='0-59/15')
def speaktask(bot):
    groupid = '614892339'
    gl = bot.List('group', groupid)
    if gl is not None:
        for group in gl:
            if speak_flag[0] and random.randint(0,100) > 97 and speak_level_check(groupid):
                msg = random.sample(msglist,1)
                print('speak任务触发!')
                bot.SendTo(group, msg[0])

#定时任务-讲话任务2
from qqbot import qqbotsched
@qqbotsched(second='0-59/15')
def speaktask2(bot):
    groupid = '514661057'
    gl = bot.List('group', groupid)
    if gl is not None:
        for group in gl:
            if speak_flag[0] and random.randint(0,100) > 97 and speak_level_check(groupid):
                msg = random.sample(msglist,1)
                print('speak任务触发!')
                bot.SendTo(group, msg[0])

#定时任务-定时训练
from qqbot import qqbotsched
@qqbotsched(hour='0-23/1')
def traintask(bot):
    chat_train()

def speak_level_check(groupid):
    try:
        key = 'chatlog_%s' % groupid
        chatlog = redis_client.get(key)
        chatlog = json.loads(chatlog) if chatlog else [0]
        if int(chatlog[0].get('qq',0)) == 1677323371:
            return 0
        else:
            return 1
    except:
        traceback.print_exc()


def speak_task():
    try:
        conn = get_conn()
        # cur = conn.cursor(pymysql.cursors.DictCursor)
        cur = conn.cursor()
        sql = '''
            SELECT content FROM chat_logs
        '''
        cur.execute(sql)
        res = cur.fetchall()
        if not res:
            return 0
        shuf_res = list(res)
        random.shuffle(shuf_res)
        limit_cnt = worlds_num[0]-500
        for i in range(len(msglist)):
            msglist.pop()
        for r in shuf_res:
            if len(msglist) > limit_cnt:
                break 
            if len(r[0]) < 30:
                msglist.add(r[0])
        print('词库自动更新,条数:%s' % len(msglist))
        conn.close()
    except:
        traceback.print_exc()
        conn.close()

def chat_train(check_rds=False):
    try:
        if not check_rds:
            key = 'words_train'
            try:
                if redis_client.exists(key):
                    print('跳过训练！')
                    load_seg_model()
                    return
                redis_client.setex(key, 1, 3600)
            except:
                traceback.print_exc()
        # 处理chatlog
        o = get_chatlog.osu()
        chatlist = o.get_chatlog()
        get_chatlog.chat2txt(chatlist)
        print('chatlog写入成功！')
        # 切词
        segment.run()
        print('切词完成！')
        # train
        seg_train.run()
        print('训练完成！')
        load_seg_model()
    except:
        traceback.print_exc()

def load_seg_model():
    try:
        model = models.Word2Vec.load('.qqbot-tmp\plugins\cbot\chat500.model.bin')
        methods.update({'segmodel':model})
        print('模型载入成功！')
    except:
        traceback.print_exc()


redis_client = redis.Redis(host='127.0.0.1', port=6379)
def get_recent_plays(osuname):
    try:
        osuid = get_osuid(osuname)
        url = 'https://osu.ppy.sh/pages/include/profile-history.php?u=%s&m=0' % osuid
        res = get_url(url)
        while res == 0:
            res = get_url(url)
        if not res:
            return 0
        value = re.compile(r"<time class='timeago' datetime.*?>(.*?)</time> - <a target='_top' href=.*?>(.*?)</a> (.*?)<br/>")
        values = value.search(res.text)
        print(values.group())
        if not values:
            return 0
        #redis处理判断是否更新
        key = 'osu_recent:%s' % osuid
        recent = redis_client.get(key)
        if recent and bytes.decode(recent) == values.group(1):
            return 0
        else:
            redis_client.set(key, values.group(1), 3600 * 24)
            #UTC时间转换
            utc_time = datetime.datetime.strptime(values.group(1)[0:-4],'%Y-%m-%d %H:%M:%S')
            now_time = utc_time + datetime.timedelta(hours=8)
            msg = '%s在%s偷偷打了张图:\nmap:%s\nscore:%s' % (osuname,now_time,values.group(2),values.group(3))
            return msg
    except:
        traceback.print_exc()
        return 0

headers = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection' : 'keep-alive',
    'Cookie' : '__cfduid=d0f839d6873527f32fe3b9dc8426362481508213944; XSRF-TOKEN=DMTtpVyEN1VvSFglE9tFYui1BkrkcuHMxh9bB1IH; osu_session=eyJpdiI6IktyNWxtVFJVNmwwcGdoS05FK21yYVE9PSIsInZhbHVlIjoiZ0t3Z0pzYUoxbXJcL1J6Mm10UmM0WG51c1Y0RTg3R0ZrNVRtcVJCSWV0bytwZjQ2OFwvaTI1MFI5Z2x5bkx3b0RrbWlyclV4U1wvQmtxQU5EY01VN2FcL0NnPT0iLCJtYWMiOiJlZWJhZTU0NzgzNzM4MGQxMmJlYTY0NjA2NTE0NDQyYmJkNzg1MDQyNWE3YjU0OTUyMGZmOGQwOGE5ZTM5YjQ0In0%3D; _ga=GA1.2.987670012.1508213952; __utma=226001156.987670012.1508213952.1508238423.1509076921.2; __utmz=226001156.1508238423.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cf_clearance=ffcabb88813877be171e47f35a2c99cbb8c1146a-1509076917-31536000; __utmb=226001156.3.10.1509076921; _gid=GA1.2.38718716.1509076975',
    'Host'  :  'osu.ppy.sh',
    'Upgrade-Insecure-Requests' :  '1',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
}
def get_url(url, timeout=3, stoptimes=3 ):
    key = 'times:%s' % url
    try:
        times = redis_client.get(key)
        if not times:
            redis_client.incr(key)
            redis_client.expire(key, 60)
        elif int(times) < stoptimes:
            redis_client.incr(key)
        else:
            return []

        res = requests.get(url,  headers=headers, timeout=timeout)
        return res
    except:
        traceback.print_exc()
        print('超时..')
        return 0

def get_conn():
    conn = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu', charset='utf8')
    return conn

osu_api_key = 'b68fc239f6b8bdcbb766320bf4579696c270b349'

def setid(qq, osuid, name, groupid, osuname):
    '''qq绑定osuid'''
    try:
        conn = get_conn()
        cur = conn.cursor()
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
        
        conn.close()
        return 1
    except:
        conn.rollback()
        
        conn.close()
        traceback.print_exc()
        return 0

def get_osuid(osuname):
    '''抓osuid'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osu_api_key, osuname)
        res = get_url(url)
        while res == 0:
            res = get_url(url)
        if not res:
            return 0
        result = json.loads(res.text)
        uid = result[0]['user_id']
        print(uid)
        conn.close()
        return uid
    except:
        traceback.print_exc()
        conn.close()
        return 0

def get_myinfo(qq):
    '''qq绑定信息'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        sql = '''
            SELECT * FROM user where qq = %s
        '''
        cur.execute(sql, qq)
        res = cur.fetchall()
        if not res:
            return 0
        
        conn.close()
        return  res[0]
    except:
        traceback.print_exc()
        
        conn.close()
        return 0

def tuijian(uid):
    '''低端推荐pp图'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        pp = float(get_user_pp(uid))
        sql = '''
            SELECT beatmap_id,count(beatmap_id) num FROM osu_user ta INNER JOIN osu_bp tb on ta.user_id = tb.user_id where ta.pp_raw BETWEEN %s and %s GROUP BY beatmap_id ORDER BY num desc limit 0,20; 
        '''
        cur.execute(sql, [pp, pp+20])
        res = cur.fetchall()
        
        conn.close()
        if not res:
            return 0
        ret = random.choice(res)
        msg = 'inter推荐给%s的图:https://osu.ppy.sh/b/%s  推荐指数:%s' %(uid,ret[0],ret[1])
        return  msg
    except:
        traceback.print_exc()
        
        conn.close()
        return 0

def get_osuinfo_byqq(qq):
    '''查库qq对应osuid'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        sql = '''
            SELECT * FROM user where qq = %s
        '''
        cur.execute(sql, qq)
        res = cur.fetchall()
        
        conn.close()
        print (res)
        if not res:
            return 0
        return  res[0]
    except:
        traceback.print_exc()
        
        conn.close()
        return 0

def get_user_pp(uid):
    try:
        url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osu_api_key, uid)
        res = get_url(url)
        while res == 0:
            res = get_url(url)
        if not res:
            return 0,0
        result = json.loads(res.text)
        if not result:
            return 0,0
        pp = result[0]['pp_raw']
        return pp
    except:
        traceback.print_exc()
        return 0

def get_bp_and_pp(uid):
    '''用户pp和bp'''
    try:
        url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osu_api_key, uid)
        res = get_url(url)
        while res == 0:
            res = get_url(url)
        if not res:
            return 0,0
        result = json.loads(res.text)
        if not result:
            return 0,0
        pp = result[0]['pp_raw']

        url2 = 'https://osu.ppy.sh/api/get_user_best?k=%s&u=%s' % (osu_api_key, uid)
        res = get_url(url2)
        while res == 0:
            res = get_url(url2)
        if not res:
            return 0,0
        result = json.loads(res.text)
        return pp,result
    except:
        traceback.print_exc()
        return 0,0


def check_user(uid):
    '''pp估计计算'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        pp,result = get_bp_and_pp(uid)
        if not pp:
            return 0,0,0
        count_num = 0
        count_pp = 0
        maxpp = 0
        for r in result:
            maxcombo1 = int(r['maxcombo']) - 10
            maxcombo2 = int(r['maxcombo']) + 10
            c50 = float(r['count50'])
            c100 = float(r['count100'])
            c300 = float(r['count300'])
            cmiss = float(r['countmiss'])
            acc = round((c50*50+c100*100+c300*300)/(c50+c100+c300+cmiss)/300*100,2)
            acc1 = acc - 0.2
            acc2 = acc + 0.2
            args = [r['beatmap_id'], r['enabled_mods'], acc1, acc2, maxcombo1, maxcombo2]
            # print(args)
            sql='''
                SELECT avg(u.pp_raw),count(1) from osu_bp b INNER JOIN osu_user u on b.user_id=u.user_id where b.beatmap_id = %s and b.mods=%s and b.acc BETWEEN %s and %s and b.maxcombo BETWEEN %s and %s 
            '''
            cur.execute(sql, args)
            res = cur.fetchall()
            
            res = res[0]
            if res[0] is None:
                continue
            # print(res)
            if res[0] > maxpp:
                maxpp = res[0]
            if res[1] != 1: 
                count_num += 1
                count_pp += res[0]
        if count_num == 0:
            yugu_pp = pp
        else:
            yugu_pp = round(count_pp/count_num)
        if maxpp == 0:
            maxpp = float(pp)
        conn.close()
        return pp,yugu_pp,round(maxpp)
    except:
        traceback.print_exc()
        
        conn.close()
        return 0,0,0

def get_user_and_bp(uid):
    '''用户以及Bp信息'''
    try:
        url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osu_api_key, uid)
        res = get_url(url)
        while res == 0:
            res = get_url(url)
        if not res:
            return 0,0
        result = json.loads(res.text)
        if not result:
            return 0,0
        user = result[0]

        url2 = 'https://osu.ppy.sh/api/get_user_best?k=%s&u=%s' % (osu_api_key, uid)
        res = get_url(url2)
        while res == 0:
            res = get_url(url2)
        if not res:
            return 0,0
        result = json.loads(res.text)
        return user,result
    except:
        traceback.print_exc()
        return 0,0

def dalou_test(uid):
    '''健康指数'''
    user,bp = get_user_and_bp(uid)
    if not user:
        return 0
    pc = int(user['playcount'])
    pp = float(user['pp_raw'])
    bp1 = float(bp[0]['pp'])
    bp5 = float(bp[4]['pp'])
    # value = round(pp/(5*bp1-4*bp5),2)
    value = round(pc*pp/(5*bp1-4*bp5)/10000,2)
    return value

def get_bp_info(uid):
    '''移植玩家bp5'''
    try:
        url = 'https://osu.ppy.sh/api/get_user_best?k=%s&u=%s' % (osu_api_key, uid)
        res = requests.get(url, timeout=3)
        s_msg = str(uid)+"'s bp!!\n"
        result = json.loads(res.text)
        if not result:
            return '没有Bp,下一个!!'
        for i,r in enumerate(result[0:5]):
            msg = 'bp{x},{pp}pp,{acc}%,{rank},+{mod}'
            c50 = float(r['count50'])
            c100 = float(r['count100'])
            c300 = float(r['count300'])
            cmiss = float(r['countmiss'])
            acc = round((c50*50+c100*100+c300*300)/(c50+c100+c300+cmiss)/300*100,2)
            msg = msg.format(x=i+1,pp=round(float(r['pp'])),acc=acc,rank=r['rank'],mod=','.join(mods.getMod(int(r['enabled_mods']))))
            s_msg = s_msg + msg + '\n'
        return s_msg[0:-1]
    except:
        traceback.print_exc()
        print('获取%s的bp失败'% str(uid))
        return '没有Bp,下一个!!'

def get_xinrenqun_replay():
    '''新人群视频'''
    try:
        ship = Config.replay_bilibili
        s_msg = 'osu!新人群月度精彩视频集锦\n'
        for sp in ship:
            s_msg = s_msg + sp['title'] + ' : ' + sp['url'] + '\n'
        return s_msg[0:-1]
    except:
        traceback.print_exc()

def get_skill(uid):
    '''skill'''
    try:
        res = requests.get('http://osuskills.tk/user/'+str(uid),timeout=5)
        if not res:
            return '没有数据,太弱了!!'
        s_msg = uid+"'s skill\n"
        value = re.compile(r'<output class="skillValue">(.*?)</output>')
        values = value.findall(res.text)
        if not values:
            return '那个破网站连不上!!'
        skills = ['Stamina', 'Tenacity', 'Agility', 'Accuracy', 'Precision', 'Reaction', 'Memory', 'Reading']
        #skills_list = list(map(lambda x,y:x+y ,skills,values))
        for i,s in enumerate(skills):
            val = int(values[i])
            if  1000 > val >= 100:
                snum = int(values[i][0:1])
            elif val >= 1000:
                snum = int(values[i][0:2])
            else:
                snum = 0
            star = '*' * snum
            skillkey = '%s:' % s
            valueskey = '%s ' % values[i]
            s_msg = s_msg+skillkey+valueskey+star+'\n'
        return s_msg[0:-1]
    except:
        traceback.print_exc()
        return '那个破网站连不上!!'

def skill_vs(uid,uid2):
    try:
        res = requests.get('http://osuskills.tk/user/%s/vs/%s'%(uid,uid2),timeout=5)
        if not res:
            return '实力太强p坏了,你们还是去床上解决吧!!'
        value = re.compile(r'<output class="skillValue">(.*?)</output>')
        values = value.findall(res.text)
        if not values:
            return '那个破网站连不上,你们还是去床上解决吧!!'
        skills = ['Stamina', 'Tenacity', 'Agility', 'Accuracy', 'Precision', 'Reaction', 'Memory', 'Reading']
        s_msg = '%s vs %s\n'%(uid,uid2)
        for i,s in enumerate(skills):
            v1 = int(values[i])
            v2 = int(values[i+8])
            vv = str(abs(v1-v2))
            fuhao = ' -- '
            if v1 > v2:
                s_msg = s_msg + s + ' : ' + values[i]+'(+'+vv+')' + fuhao + values[i+8] +'\n'
            elif v1 < v2:
                s_msg = s_msg + s + ' : ' + values[i] + fuhao + values[i+8] +'(+'+vv+')'+'\n'
            else:
                s_msg = s_msg + s + ' : ' + values[i] + fuhao + values[i+8] +'\n'
        return s_msg[0:-1]
    except:
        traceback.print_exc()
        return '那个破网站连不上,你们还是去床上解决吧!!'

def get_userpage(uid, page):
    try:
        if page <= 0:
            return '你是想找Bug吗??'
        res = requests.get('https://osu.ppy.sh/api/get_user?k=b68fc239f6b8bdcbb766320bf4579696c270b349&u='+str(uid),timeout=5)
        if not res:
            return 'id都错了醒醒!'
        s_msg = uid+"'s userpage   "
        result = json.loads(res.text)
        if not result:
            return 'id都错了醒醒!'
        uid = result[0]['user_id']

        url = 'https://osu.ppy.sh/pages/include/profile-userpage.php?u=%s'
        res = requests.get(url % uid,timeout=5)
        if len(res.text) < 1:
            return 'support都没有,先氪金好吧!'
        result = (res.text).replace('<br />','\n')
        repatt = re.compile(r'<.*?>')
        result = re.sub(repatt,'',result)
        result = html.parser.unescape(result)
        pagesize = 250
        total = (len(result)+pagesize)//pagesize
        if page > total:
            page = total
        s_msg = s_msg + '第%s页,共%s页\n'%(str(page),str(total))
        return s_msg + result[pagesize*(page-1):pagesize*page]
    except:
        traceback.print_exc()
        return 'ppy炸了,请骚等!!'

def health_check(uid):
    '''健康指数2'''
    user,bp = get_user_and_bp(uid)
    pp = float(user['pp_raw'])
    pc = int(user['playcount'])
    tth = int(user['count300'])+int(user['count100'])+int(user['count50'])
    bp1 = float(bp[0]['pp'])
    bp5 = float(bp[4]['pp'])
    acc_list = []
    for b in bp[0:5]:
        c50 = float(b['count50'])
        c100 = float(b['count100'])
        c300 = float(b['count300'])
        cmiss = float(b['countmiss'])
        acc = round((c50*50+c100*100+c300*300)/(c50+c100+c300+cmiss)/300,2)
        acc_list.append(acc)
    acc_list = sorted(acc_list,reverse=True)
    acc1 = acc_list[0]
    acc2 = acc_list[1]
    acc3 = acc_list[2]
    print(pp,pc,tth,bp1,bp5,acc1,acc2,acc3)
    v = pp*pc*tth*bp1*bp5*acc1*acc2*acc3
    if v == 0:
        return "%s 数据不正常" % uid
    else:
        A1 = pp/(4*bp1-3*bp5)
        A2 = math.log(tth/pc)/math.log(15.5)
        if pp < 1000:
            A31 = 1000*pc/(1.2*pp)-400
        elif pp < 7000:
            A31 = 1000*pc/(0.0008*pp*pp+0.4*pp)-400
        else:
            A31 = 1000*pc/(6*pp)-400
        if A31 > 1:
            A3 = math.log(A31)/math.log(24.5)
        else:
            A3 = 0
        A4 = math.pow((acc1+acc2+acc3)/3,5)
        total = A1*A2*A3*A4
        
        if pp < 300:
            level = "该号pp较低，不作出评价"
        elif total >= 55: 
            level = "该号成绩卓越，同分段中的王者!"
        elif total >= 44:
            level = "该号成绩优秀，标准的正常玩家!"
        elif A3 < 1 or A1 < 3:
            level = "基本断定是小号或者离线党!"
        elif A3 < 1.7: 
            if A1 < 9:
                level = "要么天赋超群，要么小号或者离线党,总之这个pp严重虚低!"
            else:
                if A4 < 0.75:
                    level = "虽然天赋超群,但是求你别糊图了!"
                elif A4 < 0.88: 
                    level = "虽然天赋超群，但是建议花些pc好好练习一下acc吧!"
                elif A2 < 1.7: 
                    level = "是一个有天赋的超级pp刷子,求求你不要re了!"
                elif A2 < 1.9: 
                    level = "是一个有天赋的高级pp刷子,建议降低re图次数!"
                else:
                    level = "是一个有天赋又认真的pp刷子,建议多打点综合图!"
            
        
        elif A3 < 1.9:
            if A1 < 9 and A4 > 0.75: 
                level = "有一定天赋，将来一定时间内还是可以飞升一波的!"
            if A1 < 11 and A4 > 0.75: 
                level = "有一定天赋，将来一定时间内还是可以小幅涨一点的!"
            else:
                if A4 < 0.75: 
                    level = "虽然有一些天赋,但是求你别糊图了!"
                elif A4 < 0.88: 
                    level = "虽然有一些天赋，但是建议花些pc好好练习一下acc吧!"
                elif A2 < 1.7: 
                    level = "是一个标准pp刷子,求求你不要re了!"
                elif A2 < 1.9: 
                    level = "是一个标准pp刷子,建议降低re图次数!"
                elif A2 < 2.1: 
                    level = "是一个标准pp刷子,建议多打点综合图!"
                else: 
                    level = "这种情况比较罕见，你应该和各种类型的人都不一样!"
            
        
        elif A3 < 2.1:
            if A1 < 9 and A4 > 0.75: 
                level = "看样子正渡过瓶颈期了，将来一定时间内还是可以飞升一波的!"
            if A1 < 11 and A4 > 0.75: 
                level = "要么即将渡过瓶颈期，要么之前飞太快即将进入瓶颈期!"
            else:
                if A4 < 0.75: 
                    level = "你啥都不错,但是求你别糊图了!"
                elif A4 < 0.88: 
                    level = "比较正常，但是建议好好练习一下acc吧!"
                elif A2 < 1.7: 
                    level = "是一个没天赋的pp刷子,求求你不要re了!"
                elif A2 < 1.9: 
                    level = "是一个没天赋的pp刷子,建议降低re图次数!"
                else:
                    level = "比较正常，但是可能某些方面有所欠缺，请参考指标!"
            
        
        elif A3 < 2.4:
            if A1 < 9 and A4 > 0.75: 
                level = "相信自己，你正在飞升!"
            if A1 < 11 and A4 > 0.75: 
                level = "也许在瓶颈期附近，但是相信你能克服它!"
            else:
                if A4 < 0.75: 
                    level = "你真的很强,但是求你别糊图了!"
                elif A4 < 0.88: 
                    level = "你真的很强，但是建议好好练习一下acc吧!"
                elif A2 < 1.7: 
                    level = "是一个没救了的pp刷子,求求你不要re了!"
                elif A2 < 1.9: 
                    level = "是一个没救了的pp刷子,建议降低re图次数!"
                else:
                    level = "这孩子瓶颈了!"
            
        else:
            if A1 < 10 and A4 > 0.75: 
                level = "打图经验充足，不飞升没理由!"
            else:
                if A2 < 1.8: 
                    level = "你这么个re图毫无用处，好好考虑下吧!"
                else:
                    level = "你不适合屙屎，删游戏吧!"
            
        
        msg = '%s\nBP指标:%.2f 参考值12.00\nTTH指标:%.2f 参考值2.00\nPC指标:%.2f 参考值2.00\nACC指标:%.4f 参考值0.9000\n综合指标:%.2f\n结论:%s' %(uid,A1,A2,A3,round(A4,4),round(total,2),level)
        return msg

def get_card(username):
    try:
        conn = get_conn()
        cur = conn.cursor()
        sql = '''
            SELECT username,pp_raw,acc,pc FROM osu_user where username = %s
        '''
        cur.execute(sql, username)
        res = cur.fetchall()
        #卡池不存在,手动去获取信息
        if not res:
            user_info = get_user_info(username)
            if not user_info:
                return 0
            insertUser(user_info)
            return -1
        else:
            user = res[0]
        #('xxx', 4329.1699, 98.79, '17268')
        if  0 <= user[1] <= 2000:
            level = 1
        elif 2000 < user[1] <= 3000:
            level = 2
        elif 3000 < user[1] <= 4000:
            level = 3
        elif 4000 < user[1] <= 6000:
            level = 4
        elif 6000 < user[1] <= 8000:
            level = 5
        elif 8000 < user[1]:
            level = 6
        card_level = level * '*'

        if 90 < user[2] <= 97:
            attack = (user[2]-90)*0.5
        elif 97 < user[2]:
            attack = (user[2]-97)*5
        else:
            attack = 0
        card_attack = 5 + level*5 + attack

        pc = int(user[3])
        if  0 <= pc <= 5000:
            defense = pc * 0.002
        elif 5000 < pc <= 10000:
            defense = pc * 0.002
        elif 10000 < pc <= 20000:
            defense = pc * 0.001
        elif 20000 < pc <= 30000:
            defense = pc * 0.001
        elif 30000 < pc <= 70000:
            defense = pc * 0.00025
        elif 7000 < pc:
            defense = pc * 0.000125
        card_defense = 5 + level*5 + defense

        max_attack = 5 + level*5 + 18.5
        max_defense = 5 + level*5 + 10

        card_hp = 200 + (max_attack - card_attack + max_defense - card_defense) * 8
        
        conn.close()
        
        return(username,card_level,round(card_attack),round(card_defense),round(card_hp))
    except:
        traceback.print_exc()
        conn.close()
        return 0

def get_card_msg(username):
    card_tup = get_card(username)
    if card_tup == -1:
        msg = '%s不在卡池中,自动录入卡池!' % username
        return msg
    elif card_tup == 0:
        msg = '肯定不是inter的bug,是你的问题!'
        return msg
    msg = '%s\n星级:%s\n攻击:%s\n防御:%s\n生命:%s' % (card_tup[0],card_tup[1],card_tup[2],card_tup[3],card_tup[4])
    return msg

def insertUser(info):
    '''插入'''
    try:
        conn = get_conn()
        cur = conn.cursor()
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
        
        conn.close()
        print('insert '+ info.get('user_id'))
    except:
        conn.rollback()
        
        conn.close()
        traceback.print_exc()

def get_user_info(uid):
    '''osu用户完整信息'''
    print ("uid:%s" % uid)
    url = 'https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osu_api_key, uid)
    res = get_url(url,3)
    while res == 0:
        res = get_url(url)
    result = json.loads(res.text)
    return result[0]

import bili
import fire

def get_bangumi_rank(bot, contact, num=''):
    key = 'get_bangumi_rank'
    res = redis_client.get(key)
    if not res:
        bot.SendTo(contact, 'inter忘记了,去B站看看,请骚等...')
        bi = bili.bili()
        # bi.start()
        bi.getUrl()
        bangumi = bi.get_bangumi_rank()
        bi.stop()
        #设置半天更新时间
        redis_client.setex(key, json.dumps(bangumi), 3600*3)
    else:
        bangumi = json.loads(res)
    if num:
        bangumi = bangumi[0:num]
    msg = '\n'.join(bangumi)
    msg = '新番排行\n' + msg
    return msg

def get_bangumi(bot, contact, num=''):
    key = 'get_bangumi'
    res = redis_client.get(key)
    if not res:
        bot.SendTo(contact, 'inter忘记了,去B站看看,请骚等...')
        bi = bili.bili()
        # bi.start()
        bi.getUrl()
        bangumi = bi.get_bangumi()
        bi.stop()
        #设置半天更新时间
        redis_client.setex(key, json.dumps(bangumi), 3600*3)
    else:
        bangumi = json.loads(res)
    if num:
        bangumi = random.sample(bangumi, num)
    msg = '\n'.join(bangumi)
    msg = 'inter推荐新番\n' + msg
    return msg

def get_bangumi_timeline(bot, contact, day):
    try:
        key = 'get_bangumi_timeline_%s'%(day)
        res = redis_client.get(key)
        if not res:
            bot.SendTo(contact, 'inter忘记了,去B站看看,请骚等...')
            bi = bili.bili()
            # bi.start()
            img = bi.get_time_bangumi(day)
            bi.stop()
            #设置半天更新时间
            redis_client.setex(key, img, 3600*1)
        else:
            bot.SendTo(contact, '召唤int...')
            img = res.decode()
        post2site.post2site(img, contact.qq)
    except:
        redis_client.delete(key)
        traceback.print_exc()

def get_osu_qx(bot, contact, username):
    try:
        #限制时间访问
        key_times = 'get_osu_qx'
        res_times = redis_client.get(key_times)
        if res_times:
            bot.SendTo(contact, 'inter单线程中,骚后再试...')
            return
        else:
            redis_client.setex(key_times,1,30)
        key = 'get_osu_qx_%s'%(username)
        res = redis_client.get(key)
        if not res:
            bot.SendTo(contact, 'please wait...')
            bi = fire.bili()
            # bi.start()
            img = bi.get_rank_chart(username)
            bi.stop()
            #设置半天更新时间
            redis_client.setex(key, img, 3600*6)
        else:
            # bot.SendTo(contact, '召唤int...')
            img = res.decode()
        bot.SendTo(contact, "%s's rankchart" % username)
        post2site.post2site(img, contact.qq)
        redis_client.delete(key_times)
    except:
        bi.stop()
        redis_client.delete(key)
        traceback.print_exc()


def get_from_osu_user(username):
    '''查库'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        sql = '''
            SELECT * FROM osu_user where username = %s
        '''
        cur.execute(sql, username)
        res = cur.fetchall()
        
        conn.close()
        print (res)
        if not res:
            return 0
        return  res[0]
    except:
        traceback.print_exc()
        conn.close()
        return 0

def get_help():
    '''帮助'''
    msg = '''interBot v1.4(话痨版本)
1.rbq(不知道为什么被关了)
2.myrbq
3.setid xxx(请绑定)
4.myinfo
5.getid@别人(获取群员osuid)
6.set,inter的奸视(需要权限)
7.check xxx(inter随机乱算的)
8.js 奸视列表
9.test 健康指数(dalou公式)
10.bbp 用来秀bp?
11.sp 新人群专属番
12.skill 
13.vssk +osuid 对比 
14.upage xx,2
15.map 低端推荐pp图
16.card 卡牌
17.新番/新番排行(暂时用不了)
18.osu 名词解释
19.s(stats的回归,绑定id限定)
20.days 2 跨天数增长
21. pk/zj/win/lose 壳子系列
22. kw word 词关联(new)'''
    return msg

# 解锁8号彩蛋 1061566571