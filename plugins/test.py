# -*- coding: utf-8 -*-

import random
import pymysql
import traceback
import json
import requests
import redis
import html.parser
import re
import datetime
import math


import mods
import Config

rbq_614892339 = set([])
rbq_list_614892339 = {}            
rbq_514661057 = set([])
rbq_list_514661057 = {}
testuser = []

def onQQMessage(bot, contact, member, content):
    #contact :  ctype/qq/uin/nick/mark/card/name 
    #群限制 Q号 614892339
    if contact.ctype == 'group':
        if contact.qq != '614892339' and contact.qq != '514661057' and contact.qq != '598918097':
            return 
        if len(rbq_614892339) > 20:
            rbq_614892339.pop()
        rbq_614892339.add(member.name)
        
        if content == '!help':
            bot.SendTo(contact, 'dalou只会打爆你!')
        elif content == '!dalou':
            msg = get_help()
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
            #取qq绑定
            if not uid:
                res = get_osuinfo_byqq(member.qq)
                if not res:
                    bot.SendTo(contact, member.name+'未绑定osuid')
                    return
                uid = res[5]
            pp,pp2,maxpp = check_user(uid)
            if not pp:
                bot.SendTo(contact, '没有pp,下一个!')
                return
            msg = '%s\npp:%spp\ndalou手算:%spp\n目前潜力:%spp' % (uid,pp,pp2,maxpp)
            bot.SendTo(contact, msg)
        elif '!test' in content:
            uid = content[6:]
            #取qq绑定
            if not uid:
                res = get_osuinfo_byqq(member.qq)
                if not res:
                    bot.SendTo(contact, member.name+'未绑定osuid')
                    return
                uid = res[5]
            msg = health_check(uid)
            bot.SendTo(contact, msg)
        # elif '!test' in content:
        #     uid = content[6:]
        #     #取qq绑定
        #     if not uid:
        #         res = get_osuinfo_byqq(member.qq)
        #         if not res:
        #             bot.SendTo(contact, member.name+'未绑定osuid')
        #             return
        #         uid = res[5]
        #     value = dalou_test(uid)
        #     if value < 1:
        #         level = '极致不健康'
        #     elif 5 > value >= 1:
        #         level = '灰常不健康'
        #     elif 10 > value >= 5:
        #         level = '不健康'
        #     elif 15 > value >= 10:
        #         level = '介于健康与不健康'
        #     elif 25 > value >= 15:
        #         level = '健康'
        #     elif 100 > value >= 30:
        #         level = '健康过度'
        #     elif value >= 100:
        #         level = '健康溢出'
        #     msg = '%s\n健康指数:%s\nleve:%s' % (uid,value,level)
        #     # msg = html.parser.unescape(msg)
        #     bot.SendTo(contact, msg)
        elif '!bbp' in content:
            uid = content[5:]
            #取qq绑定
            if not uid:
                res = get_osuinfo_byqq(member.qq)
                if not res:
                    bot.SendTo(contact, member.name+'未绑定osuid')
                    return
                uid = res[5]
            msg = get_bp_info(uid)
            bot.SendTo(contact, msg)
        elif '!sp' == content:
            msg = get_xinrenqun_replay()
            bot.SendTo(contact, msg)
        elif '!skill' in content:
            uid = content[6:]
            #取qq绑定
            if not uid:
                res = get_osuinfo_byqq(member.qq)
                if not res:
                    bot.SendTo(contact, member.name+'未绑定osuid')
                    return
                uid = res[5]
            msg = get_skill(uid)
            bot.SendTo(contact, msg)
        elif '!vssk' in content:
            ulist = content[6:].split(',')
            if len(ulist) == 1:
                #取qq绑定
                res = get_osuinfo_byqq(member.qq)
                if not res:
                    bot.SendTo(contact, member.name+'未绑定osuid')
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
        elif '!upage' in content:
            slist = content[7:].split(',')
            if len(slist) == 1:
                page = 1
            else:
                page = int(slist[1])
            msg = get_userpage(slist[0], page)
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
    '''qq绑定osuid'''
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
    '''抓osuid'''
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
    '''qq绑定信息'''
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
    '''查库qq对应osuid'''
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
    '''用户pp和bp'''
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
    '''pp估计计算'''
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
            acc1 = acc - 0.2
            acc2 = acc + 0.2
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
        return pp,yugu_pp,round(maxpp)
    except:
        traceback.print_exc()
        return 0,0,0

def get_user_and_bp(uid):
    '''用户以及Bp信息'''
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
        user = result[0]

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
    for b in bp:
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
            A3 = math.log(A31)/math.log(25.5)
        else:
            A3 = 0
        A4 = math.pow((acc1+acc2+acc3)/3,5)
        total = A1*A2*A3*A4
         
        if total < 14:
            level = '可以踢了'
        elif total < 28:
            level = '严重可疑'
        elif total < 35:
            level = '较危险'
        elif total < 42:
            level = '亚健康'
        elif total < 56:
            level = '很健康'
        else:
            level = '无敌'
        msg = '%s\nBP指标:%.2f 参考值12.00\nTTH指标:%.2f 参考值2.00\nPC指标:%.2f 参考值2.00\nACC指标:%.4f 参考值0.9000\n综合指标:%.2f\n结论:%s' %(uid,A1,A2,A3,round(A4,2),round(total,4),level)
        return msg

def get_help():
    '''帮助'''
    msg = '''dalouBot v1.2
1.rbq(暂时关闭)
2.myrbq
3.setid xxx(请绑定,后续有用)
4.myinfo
5.getid@别人(获取群员osuid)
6.dalou的奸视(new)(需要权限)
7.check xxx(new)(使用大数据支持)
8.js 奸视列表(new)
9.test 健康指数(new)(dalou公式)
10.bbp(移植)
11.sp(移植)
12.skill(移植)
13.vssk(移植)
14.upage xx,2(移植)
15.接受功能建议'''
    return msg
