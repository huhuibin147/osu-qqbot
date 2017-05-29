# -*- coding:utf-8 -*-
import requests
import time
import json
import logging
import traceback
import pymysql
import datetime

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
        self.con=''


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
            self.send('int100被你们roll坏了',group_uin)
            return

        if msg and '!r' in msg:
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
            

    def get_con(self):
        self.con = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu')

    def get_cursor(self):
        self.get_con()
        cur = self.con.cursor()
        return cur

    def insert_user(self,*user):
        cur = self.get_cursor()
        sql = 'insert into user(username,pp,acc,pc,rank,tth,time) values(%s,%s,%s,%s,%s,%s,%s)'
        result = cur.execute(sql,tuple(user))
        logging.info('插入数据结果:'+str(result))
        self.con.commit()

    def get_user_fromDB(self,username,**kwargs):
        cur = self.get_cursor()
        if not kwargs:
            now = datetime.datetime.now()
            yday = now - datetime.timedelta(days=1)
            yday = yday.strftime('%Y-%m-%d %H:%M:%S')
            sql = 'select * from user where username=%s and time>=%s limit 1'
            logging.info('查询时间:'+yday)
        result = cur.execute(sql,(username,yday))
        logging.info('查询数据结果:'+str(result))
        if result:
            user_info = cur.fetchall()
            #print(user_info)
            return user_info
        else:
            return ''

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
                if add_rank > 0:
                    add_rank = '+'+str(add_rank)
                else:
                    add_rank = str(add_rank)
                add_acc =  round(acc1 - float(info[3]),2)
                if add_acc >0.0:
                    add_acc = '+'+str(add_acc)
                else:
                    add_acc = str(add_acc)
                add_pc = str(int(pc) - info[4])
                add_tth = str(tth - info[6])
                d = username+'\n'+pp+'pp(+'+add_pp+')\n'+'rank: '+rank+'('+add_rank+')\n'+'acc : '+acc+'%('+add_acc+')\n'+'pc  : '+pc+'pc(+'+add_pc+')\n'+'tth  : '+tth_w+'w(+'+add_tth+')'
            else:
                d = username+'\n'+pp+'pp(+0)\n'+'rank: '+rank+'(+0)\n'+'acc : '+acc+'%(+0)\n'+'pc  : '+pc+'pc(+0)\n'+'tth  : '+tth_w+'w(+0)'
            in_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            self.insert_user(username,in_pp,acc1,pc,rank,tth,in_time)
            self.con.close()
            return d
        except:
            traceback.print_exc()


if __name__ == '__main__':
    l = Login()
    try:
        l.before_login()
        l.getMsg()
        #logging.info('自动登录成功!')
    except:
        traceback.print_exc() 
        logging.info('登录信息过期!')
        info = l.run()
    while True: 
        try:   
            msg,group_uin,user_uin = l.getMsg()
            l.check_msg(msg,group_uin,user_uin)
        except:
            traceback.print_exc() 

