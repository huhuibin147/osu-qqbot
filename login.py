# -*- coding:utf-8 -*-
import requests
import time
import datetime
import json
import logging
import traceback
import pymysql
import datetime
import random
import sched
import threading
import mods
import re
import Config
import html.parser

class Login(object):
    def __init__(self):
        #level=logging.DEBUG   level=logging.INFO
        logging.basicConfig(level=logging.INFO,
                             format='[%(asctime)s][%(levelname)s] %(message)s',
                             datefmt='%H:%M:%S')
        self.login_get_cookies_url = "https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001"
        self.get_ptqrshow = "https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.9142399367333609"
        self.getvfwebqq = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq={ptwebqq}&clientid=53999199&psessionid=&t=1488053293431"
        self.login2 = "http://d1.web2.qq.com/channel/login2"
        self.online = "http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq={vfwebqq}&clientid=53999199&psessionid={psessionid}&t=1488268527333"
        
        self.user3_cookies = ''
        self.psessionid = ''
        self.vfwebqq = ''
        self.ptwebqq = ''
        self.con = ''
        self.roll_list = ['int100被你们roll坏了']
        self.wzq_qipan = []
        self.wzq_color = 0 #黑
        self.size = 10


    def run(self):
        base = requests.session()
        result = base.get(self.login_get_cookies_url)
        base_cookies = result.cookies
        result = base.get(self.get_ptqrshow)
        ptqr_cookies = result.cookies
        with open('qrcode.png','wb') as f:
            f.write(result.content)
        cookies = dict(base_cookies.items() + ptqr_cookies.items())
        #进行ptqrtoken计算
        qrsig = cookies['qrsig']
        e = 0
        n = len(qrsig)
        for i in range(0, n):
            e = e + (e << 5) + ord(qrsig[i])
        ptqrtoken = 2147483647 & e
        while True:
            result = requests.get("https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=" + str(
                    ptqrtoken) + "&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-32750&mibao_css=m_webqq&t=undefined&g=1&js_type=0&js_ver=10197&login_sig=&pt_randsalt=0",
                                      cookies=cookies)
            #print(result.text)
            if '二维码未失效' in result.text:
                logging.info('请扫描二维码')
            if '已失效' in result.text:
                return {'result': '-1', 'reason': '二维码已经失效'}
            if '认证中' in result.text:
                logging.info('认证中')
            if '登录成功' in result.text:
                checksig_url = result.text.split("','")[2]
                user_cookies = result.cookies
                logging.info('登录成功')
                break
            time.sleep(1)
        self.ptwebqq = user_cookies['ptwebqq']
        result = requests.get(checksig_url, cookies=user_cookies, allow_redirects=False)
        user2_cookies = result.cookies
        self.user3_cookies = dict(user_cookies.items()+user2_cookies.items())
        headers = {
                "Referer":"http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"
        }
        vfwebqq = requests.get(self.getvfwebqq.replace('{ptwebqq}', self.ptwebqq), cookies=self.user3_cookies, headers=headers).text
        self.vfwebqq = json.loads(vfwebqq)['result']['vfwebqq']
        #二次登陆，真正的登录
        data = {
            'r': '{"ptwebqq":"'+self.ptwebqq+'","clientid":53999199,"psessionid":"","status":"online"}'
        }
        headers = {
            'Host': 'd1.web2.qq.com',
            'Referer': 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
            'Origin':'http://d1.web2.qq.com'
        }
        result = requests.post(self.login2, data=data, cookies=self.user3_cookies, headers=headers)
        jresult = json.loads(result.text)
        if jresult['retcode'] == 0:
            logging.info('登录成功')
            uin = jresult["result"]["uin"]
            headers = {
                    'Host':'d1.web2.qq.com',
                    'Referer':'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2'''
            }
            self.psessionid = jresult['result']['psessionid']
            requests.get(self.online.replace('{vfwebqq}', self.vfwebqq).replace('{psessionid}', self.psessionid), cookies=self.user3_cookies, headers=headers)
            #保存登录信息
            data_info = {
                'user3_cookies':self.user3_cookies,
                'psessionid':self.psessionid,
                'vfwebqq':self.vfwebqq,
                'ptwebqq':self.ptwebqq
            }
            with open('login.txt','w') as f:
                f.write(str(data_info))
            return {'result': '0', 'reason': '登录成功', 'cookies':self.user3_cookies, 'psessionid': self.psessionid, 'vfwebqq': self.vfwebqq, 'uin':uin,'ptwebqq': self.ptwebqq}
        else:
            logging.info('登录失败')
            return {'result': '-2', 'reason': '登录失败'}

    def getMsg(self):
        headers = {
            'Host': 'd1.web2.qq.com',
            'Referer': 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
            'Origin':'http://d1.web2.qq.com'
        }
        
        
        data = {
            'r' : '{"ptwebqq":"'+self.ptwebqq+'","clientid":53999199,"psessionid":"'+self.psessionid+'","key":""}'
        }
        url = 'http://d1.web2.qq.com/channel/poll2'
        result = requests.post(url, data=data, cookies=self.user3_cookies, headers=headers)
        #print(result.text)
        jresult = json.loads(result.text)
        if not jresult['result']:
            return None
        group_uin = jresult['result'][0]['value']['from_uin']
        user_uin = jresult['result'][0]['value']['send_uin']
        msg = ''
        if len(jresult['result'][0]['value']['content']) > 1:
            msg = jresult['result'][0]['value']['content'][1]
        msg2 = '['+str(group_uin)+']'+msg
        logging.info(msg2)
        return msg,group_uin,user_uin
        #uin = jresult['result'][0]['value']['send_uin']
        #print('uin:'+str(uin))
    
    def getUser(self,uin):
        headers2 = {
            'Referer': 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2'
        }
        url2 = 'http://s.web2.qq.com/api/get_friend_uin2?tuid='+str(uin)+'&type=1&vfwebqq='+self.vfwebqq+'&t=0.1'
        result2 = requests.get(url2,cookies=self.user3_cookies, headers=headers2)
        print(result2.text)

    

    def send(self,send_msg,group_uin):
        headers2 = {
            'Referer': 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2'
        }
        url = 'http://d1.web2.qq.com/channel/send_qun_msg2'       
        data = {
                'r': json.dumps({
                    'group_uin': int(group_uin),
                    'content': json.dumps(
                        [send_msg] +
                        [['font', {'name': '宋体', 'size': 10,
                                  'style': [0,0,0], 'color': '000000'}]]
                    ),
                    'face': 522,
                    'clientid': 53999199,
                    'msg_id': 99010001,
                    'psessionid': self.psessionid
                })
            }

        result = requests.post(url, data=data, cookies=self.user3_cookies, headers=headers2)
        logging.info(result.text)
        
    
    def before_login(self):
        #读取登录信息
        logging.info('尝试读取登录信息')
        with open('login.txt','r') as f: 
            t=f.read()
        if t:
            login_info = eval(t)
            self.user3_cookies = login_info.get('user3_cookies')
            self.psessionid = login_info.get('psessionid')
            self.vfwebqq = login_info.get('vfwebqq')
            self.ptwebqq = login_info.get('ptwebqq')


    def check_msg(self,msg,group_uin,user_uin):

        if msg and '!stats' in msg:
            #self.send('没有pp,下一个!!',group_uin)
            s_msg = self.osu_stats(msg[7:])
            if s_msg:
                self.send(str(s_msg),group_uin)
            else:
                self.send('没有pp,下一个!!',group_uin)
            return

        if msg and '!roll' in msg:
            send_msg = self.getRoll()
            self.send(send_msg,group_uin)
            return

        if msg and '!setroll' in msg:
            msg_l = msg.split(' ')
            self.roll_list.append(msg_l[1])
            return

        if msg and '!resetroll' in msg:
            self.roll_list = ['int100被你们roll坏了']
            return

        if msg and '!help' in msg:
            self.send('我并不打算help了你!!',group_uin)
            return
            
        if msg and '!ri' in msg:
            #self.getUser(user_uin)
            self.send('你想被日吗??',group_uin)
            return

        if msg and '!get' in msg:
            s_msg = self.get_user_fromDB(msg[5:])
            if s_msg:
                self.send(str(s_msg),group_uin)
            else:
                self.send('不认识你走开,下一个!!',group_uin)
            return
        


    def getRoll(self):
        index =random.randint(0,len(self.roll_list)-1)
        return self.roll_list[index]

    def get_con(self):
        self.con = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu')

    def get_cursor(self):
        self.get_con()
        cur = self.con.cursor()
        return cur

    def insert_user(self,*user):
        cur = self.get_cursor()
        sql = 'insert into user2(username,pp,acc,pc,rank,tth,time) values(%s,%s,%s,%s,%s,%s,%s)'
        result = cur.execute(sql,tuple(user))
        logging.info('插入数据结果:'+str(result))
        self.con.commit()

    def get_user_fromDB(self,username,**kwargs):
        cur = self.get_cursor()
        if not kwargs:
            if self.is_today():
                time = self.get_today()
            else:
                time = self.get_yes()
            sql = 'select * from user2 where username=%s and time>=%s limit 1'
            logging.info('查询时间:'+time)
        result = cur.execute(sql,(username,time))
        logging.info('查询数据结果:'+str(result))
        if result:
            user_info = cur.fetchall()
            #print(user_info)
            return user_info
        else:
            return ''

    def get_user_list_fromDB(self):
        logging.info('查询用户列表..')
        cur = self.get_cursor()
        sql = 'SELECT username from user2 GROUP BY username'
        result = cur.execute(sql)
        user_list = cur.fetchall()
        return user_list

    def exist_user(self,uid):
        #logging.info('查询用户是否存在')
        cur = self.get_cursor()
        sql = 'SELECT 1 from user2 where username="'+uid+'" limit 1'
        result = cur.execute(sql)
        user_list = cur.fetchall()
        return user_list

    def osu_stats(self,uid):
        try:
            logging.info('查询用户:'+uid)
            res = requests.get('https://osu.ppy.sh/api/get_user?k=b68fc239f6b8bdcbb766320bf4579696c270b349&u='+str(uid),timeout=5)

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
                add_pc = str(int(pc) - info[4])
                add_tth = str(tth - info[6])
                d = username+'\n'+pp+'pp(+'+add_pp+')\n'+'rank: '+rank+'('+add_rank+')\n'+'acc : '+acc+'%('+add_acc+')\n'+'pc  : '+pc+'pc(+'+add_pc+')\n'+'tth  : '+tth_w+'w(+'+add_tth+')'
            else:
                d = username+'\n'+pp+'pp(+0)\n'+'rank: '+rank+'(+0)\n'+'acc : '+acc+'%(+0)\n'+'pc  : '+pc+'pc(+0)\n'+'tth  : '+tth_w+'w(+0)'
            #in_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            is_exist = self.exist_user(uid)
            if not is_exist:
                logging.info('用户不存在,进行插入')
                #检测时间段0-9点
                if self.is_today():
                    in_time = self.get_today()
                else:
                    in_time = self.get_yes()
                self.insert_user(username,in_pp,acc1,pc,rank,tth,in_time)
            self.con.close()
            return d
        except:
            traceback.print_exc()

    def getU(self,uid):
        try:
            logging.info('获取用户:'+uid)
            res = requests.get('https://osu.ppy.sh/api/get_user?k=b68fc239f6b8bdcbb766320bf4579696c270b349&u='+str(uid),timeout=2)
        except:
            logging.info('获取失败:'+uid)
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
        try:
            u_tuple = self.get_user_list_fromDB()
            u_list = list(u_tuple)#[('xxx',),('xxx,')]
            today = datetime.date.today()
            in_time = str(today)+' 9:00:00'
            for uid in u_list:
                uid = uid[0]
                res = self.getU(uid)
                while not res:
                    res = self.getU(uid)

                result = json.loads(res.text)            
                result = result[0]
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
                logging.info(uid+'插入成功')
            self.con.close()
        except:
            logging.info('auto_inert错误')
            self.con.close()

    def insert_forday(self):
        logging.info('开始执行定时插入任务')
        self.auto_inert()
        logging.info('定时插入任务结束')

    def time_insert(self):
        '''定时任务'''
        today = datetime.date.today()
        now_hour = time.strftime('%H%M%S')
        is_run = int(now_hour) - 90000
        if  is_run < 0:
            logging.info('延时执行')
            now = datetime.datetime.now()
            stats = datetime.datetime(today.year,today.month,today.day,9,0,0)
            delay = (stats - now).seconds
            print(delay)
            s = sched.scheduler(time.time, time.sleep)
            s.enter(delay,0,self.insert_forday,())
            s.run()
        else:
            logging.info('超过时间,立即执行定时任务')
            if not self.is_insert_today():
                logging.info('今日数据不存在,准备抓取...')
                self.insert_forday()
            else:
                logging.info('今日数据已存在,不需要抓取')
            #self.insert_forday()
            logging.info('定时任务结束')
    
    def get_bp(self, uid):
        try:
            res = requests.get('https://osu.ppy.sh/api/get_user_best?k=b68fc239f6b8bdcbb766320bf4579696c270b349&u='+str(uid),timeout=3)
            s_msg = '请开始你的表演!!\n'
            if not res:
                return '没有Bp,下一个!!'
            beatmap_pre = 'https://osu.ppy.sh/b/%s'
            result = json.loads(res.text)
            for r in result[0:5]:
                beatmap = beatmap_pre % r['beatmap_id']
                s_msg = s_msg + beatmap +'\n'
            return s_msg[0:-1]
        except:
            logging.info('获取%s的bp失败'% str(uid))
            return '没有Bp,下一个!!'
    
    def get_bp_info(self, uid):
        try:
            res = requests.get('https://osu.ppy.sh/api/get_user_best?k=b68fc239f6b8bdcbb766320bf4579696c270b349&u='+str(uid),timeout=3)
            if not res:
                return '没有Bp,下一个!!'
            s_msg = str(uid)+"'s bp!!\n"
            result = json.loads(res.text)
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
            logging.info('获取%s的bp失败'% str(uid))
            return '没有Bp,下一个!!'

    def check_user(self, uid):
        msg_list = ['%s这么恐怖，肯定是小号!!','%s是inter认定的非小号!!']
        s_msg = (random.choice(msg_list)) % str(uid)
        return s_msg

    def get_skill(self, uid):
        try:
            res = requests.get('http://osuskills.tk/user/'+str(uid),timeout=5)
            if not res:
                return '没有数据,太弱了!!'
            s_msg = uid+"'s skill\n"
            value = re.compile(r'<output class="skillValue">(.*?)</output>')
            values = value.findall(res.text)
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
            logging.info(traceback.print_exc())
            logging.info('获取%s的skills失败'% str(uid))
            return '没有数据,太弱了!!'

    def skill_vs(self,uid,uid2):
        try:
            res = requests.get('http://osuskills.tk/user/%s/vs/%s'%(uid,uid2),timeout=5)
            if not res:
                return '实力太强p坏了,你们还是去床上解决吧!!'
            value = re.compile(r'<output class="skillValue">(.*?)</output>')
            values = value.findall(res.text)
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
            logging.info(traceback.print_exc())
            return 'inter网速太辣鸡了,你们还是去床上解决吧!!'

    def get_recent_plays(self, uid):
        try:
            res = requests.get('https://osu.ppy.sh/api/get_user?k=b68fc239f6b8bdcbb766320bf4579696c270b349&u='+str(uid),timeout=3)
            if not res:
                return '你一天没打图了,醒醒!!'
            result = json.loads(res.text)
            s_msg = uid+"'s Recent Plays\n"
            uid = result[0]['user_id']
            url = 'https://osu.ppy.sh/pages/include/profile-history.php?u=%s&m=0'
            res = requests.get(url % uid,timeout=5)
            if not res:
                return 'ppy炸了,请骚等!!'
            value = re.compile(r"<time class='timeago'.*?</time> - <a target='_top' href=.*?>(.*?)</a> (.*?)<br/>")
            values = value.findall(res.text)
            for i,r in enumerate(values):
                rplay = ' '.join(r)
                s_msg = s_msg + str(i+1) + '-' + rplay + '\n'
            return s_msg[0:-1]
        except:
            logging.info(traceback.print_exc())
            return 'ppy炸了,请骚等!!'

    def get_xinrenqun_replay(self):
        try:
            ship = Config.replay_bilibili
            s_msg = 'osu!新人群月度精彩视频集锦\n'
            for sp in ship:
                s_msg = s_msg + sp['title'] + ' : ' + sp['url'] + '\n'
            return s_msg[0:-1]
        except:
            logging.info(traceback.print_exc())
            return 'inter炸了,请骚等!!'

    def get_help(self):
        s_msg = "inter登场了!\n"
        s_msg = s_msg + '1-roll inter摇摇乐!!\n'
        s_msg = s_msg + '2-setroll 自定义inter的摇摇乐!!\n'
        s_msg = s_msg + '3-bbp   装逼用的!!\n'
        s_msg = s_msg + '4-baobp 爆bp专用!!\n'
        s_msg = s_msg + '5-skill 屙屎熟练度!!\n'
        s_msg = s_msg + '6-vssk  试一下pk进化的dalou吧!!\n'
        s_msg = s_msg + '7-recent 最近偷偷刷什么呢!!\n'
        s_msg = s_msg + '8-check inter智能测小号!!\n'
        s_msg = s_msg + '9-sp 新(大)人(佬)群集锦!!\n'
        s_msg = s_msg + '10-ri ???\n'
        return s_msg[0:-1]

    def get_userpage(self, uid, page):
        try:
            if page <= 0:
                return '你是想找Bug吗??'
            res = requests.get('https://osu.ppy.sh/api/get_user?k=b68fc239f6b8bdcbb766320bf4579696c270b349&u='+str(uid),timeout=5)
            if not res:
                return 'id都错了醒醒!'
            s_msg = uid+"'s userpage   "
            result = json.loads(res.text)
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
            logging.info(traceback.print_exc())
            return 'ppy炸了,请骚等!!'

    def check_msg(self,msg,group_uin,user_uin):

        # if msg and '!stats' in msg:
        #     #self.send('没有pp,下一个!!',group_uin)
        #     s_msg = self.osu_stats(msg[7:])
        #     if s_msg:
        #         self.send(str(s_msg),group_uin)
        #     else:
        #         self.send('没有pp,下一个!!',group_uin)
        #     return

        if msg and '!roll' in msg:
            send_msg = self.getRoll()
            self.send(send_msg,group_uin)
            return

        if msg and '!setroll' in msg:
            msg_l = msg.split(' ')
            self.roll_list.append(msg_l[1])
            return

        if msg and '!bbp' in msg:
            s_msg = self.get_bp_info(msg[5:])
            self.send(s_msg, group_uin)
            return

        if msg and '!baobp' in msg:
            s_msg = self.get_bp(msg[7:])
            self.send(s_msg, group_uin)
            return

        if msg and '!skill' in msg:
            s_msg = self.get_skill(msg[7:])
            self.send(s_msg, group_uin)
            return

        if msg and '!vssk' in msg:
            ulist = msg[6:].split(',')
            s_msg = self.skill_vs(ulist[0],ulist[1])
            self.send(s_msg, group_uin)
            return

        if msg and '!upage' in msg:
            s = msg[7:].split(',')
            if len(s) == 1:
                page = 1
            else:
                page = int(s[1])
            s_msg = self.get_userpage(s[0],page)
            self.send(s_msg, group_uin)
            return
            

        # if msg and '!recent' in msg:
        #     s_msg = self.get_recent_plays(msg[8:])
        #     self.send(s_msg, group_uin)
        #     return

        if msg and '!' in msg and 'louxinye' in msg:
            msg_list = ['dalou太强了!!','dalou我偶像!!']
            self.send(random.choice(msg_list),group_uin)
            return

        if msg and '!check' in msg:
            s_msg = self.check_user(msg[7:])
            self.send(s_msg, group_uin)
            return

        if msg and '!resetroll' in msg:
            self.roll_list = ['int100被你们roll坏了']
            return

        if msg and '!help' in msg:
            self.send("inter's help need interinter!!",group_uin)
            return
            
        if msg and '!ri' in msg:
            #self.getUser(user_uin)
            self.send('你想被日吗??',group_uin)
            return

        if msg and '!sp' in msg:
            s_msg = self.get_xinrenqun_replay()
            self.send(s_msg,group_uin)
            return 

        if msg and msg == '!interinter':
            s_msg = self.get_help()
            self.send(s_msg,group_uin)
            return 

        # if msg and msg in '!test':
        #     s_msg = '┌─┬─┬─┬─┐\n│   │   │   │   │\n├─┼─┼─┼─┤\n│   │   │   │   │\n├─┼─┼─┼─┤\n│   │   │   │   │\n├─┼─┼─┼─┤\n│   │   │   │   │\n└─┴─┴─┴─┘'
        #     self.send(s_msg,group_uin)
        #     return
             
        if msg and msg == '!test':
            s_msg = '●●●●●●●●●●●●●●●\n○○○○○○○○○○○○○○○\n●●●●●●●●●●●●●●●\n'
            self.send(s_msg,group_uin)
            return

        if msg and '!initwzq2' in msg:
            s_msg = self.init_wzq2(msg[10:])
            self.send(s_msg,group_uin)
            s_msg2 = ''.join(self.wzq_qipan)
            self.send(s_msg2[0:-1],group_uin)
            return

        if msg and '!x' in msg:
            xy = msg[3:].split(',')
            s_msg = self.wzq_xiaqi2(self.size,int(xy[0]),int(xy[1]))
            self.send(s_msg[0:-1],group_uin)
            return

        if msg and '!xtest' in msg:
            xy = msg[3:].split(',')
            self.wzq_xiaqi(int(xy[0]),int(xy[1]))
            s_msg = ''.join(self.wzq_qipan)
            self.send(s_msg[0:-1],group_uin)
            return

        if msg and msg == '!inittestwzq':
            self.init_wzq_qipan()
            self.send('初始化棋盘成功!',group_uin)
            s_msg = ''.join(self.wzq_qipan)
            self.send(s_msg[0:-1],group_uin)
            return

        # if msg and '!get' in msg:
        #     s_msg = self.get_user_fromDB(msg[5:])
        #     if s_msg:
        #         self.send(str(s_msg),group_uin)
        #     else:
        #         self.send('不认识你走开,下一个!!',group_uin)
        #     return  

    def wzq_xiaqi2(self, size, x, y):
        try:
            black = '●'
            white = '◎'
            if 1<=x<=size and 1<=y<=size:
                i = (size+1)*(x-1)+(y-1)
                if self.wzq_qipan[i] != '□':
                    return '五子棋你还想吃了它不成!'
                if self.wzq_color == 0:
                    self.wzq_qipan[i] = black
                    self.wzq_color = 1
                else:
                    self.wzq_qipan[i] = white
                    self.wzq_color = 0
                return ''.join(self.wzq_qipan)
                logging.info('下子结束')
            else:
                return '醒醒你下偏了,x,y范围在'+str(size)
        except:
            logging.info(traceback.print_exc())

    def init_wzq2(self, size):
        try:
            size = int(size)
            if size <=0 or size >50:
                self.size = 10 
                s_msg = '参数出错,使用默认size:10*10,初始化棋盘成功!'
            else:
                self.size = size 
                s_msg = '初始化棋盘成功!size:'+str(self.size)+'*'+str(self.size)
            line = '□'*self.size+'\n'
            self.wzq_qipan = (list(line))*self.size
            self.wzq_color = 0 #黑
            return s_msg
        except:
            logging.info(traceback.print_exc())
            return '初始化棋盘失败!'

    def wzq_xiaqi(self, x, y):
        try:
            black = '●'
            white = '○'
            i = 28*int(x)+2*int(y)-30
            if self.wzq_color == 0:
                self.wzq_qipan[i] = black
                self.wzq_color = 1
            else:
                self.wzq_qipan[i] = white
                self.wzq_color = 0
            logging.info('下子结束')
        except:
            logging.info(traceback.print_exc())

    def init_wzq_qipan(self):
        try:
            top     = '┌─┬─┬─┬─┐\n'
            top_mid = '│   │   │   │   │\n'
            mid     = '├─┼─┼─┼─┤\n'
            bottom  = '└─┴─┴─┴─┘\n'
            self.wzq_qipan = list(top+top_mid+mid+top_mid+mid+top_mid+mid+top_mid+bottom)
            self.wzq_color = 0 #黑
            logging.info('初始化棋盘成功!')
        except:
            logging.info(traceback.print_exc())

def qqbot_main():
    l = Login()
    try:
        l.before_login()
        l.getMsg()
        #logging.info('自动登录成功!')
    except:
        logging.info(traceback.print_exc())
        logging.info('登录信息过期!')
        info = l.run()
    while True: 
        try:   
            msg,group_uin,user_uin = l.getMsg()
            l.check_msg(msg,group_uin,user_uin)
        except:
            logging.info(traceback.print_exc())

def sched_day_insert():
    l = Login()
    try:
        l.time_insert()
    except:
        logging.info('定时任务出错')
        logging.info(traceback.print_exc())

if __name__ == '__main__':
    try:
        # sched_t = threading.Thread(target=sched_day_insert)
        main_t = threading.Thread(target=qqbot_main)
        # sched_t.start()
        main_t.start()
    except:
        logging.info(traceback.print_exc())

