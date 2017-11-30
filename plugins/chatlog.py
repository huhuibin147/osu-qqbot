# -*- coding: utf-8 -*-
import json
import redis
import pymysql  
import datetime
import traceback

def onQQMessage(bot, contact, member, content):
    # 当收到 QQ 消息时被调用
    # bot     : QQBot 对象，提供 List/SendTo/GroupXXX/Stop/Restart 等接口，详见文档第五节
    # contact : QContact 对象，消息的发送者
    # member  : QContact 对象，仅当本消息为 群或讨论组 消息时有效，代表实际发消息的成员
    # content : str 对象，消息内容
    if contact.ctype == 'group' and len(content)>0:
        insertChatContent(bot,contact,member,content)
        insertRedis(bot,contact,member,content)


def insertChatContent(bot,contact,member,content):
    # 连接数据库  
    try:
        connect = pymysql.Connect(  
            host='localhost',  
            port=3306,  
            user='root',  
            passwd='123456',  
            db='osu',  
            charset='utf8'  
        )  

        # 获取游标  
        cursor = connect.cursor()  
        now = datetime.datetime.now()
        createtime=now.strftime('%Y-%m-%d %H:%M:%S')  
        # 插入数据  
        sql = '''
            INSERT INTO chat_logs (group_number,qq,content,create_time) 
            VALUES ( %s, %s, %s, now())
        ''' 
        args = [contact.qq, member.qq, content]
        cursor.execute(sql, args)  
        connect.commit()  
        # print('insert success', cursor.rowcount, ' record')
    except:
        print('insert fail')
        connect.rollback()

def insertRedis(bot,contact,member,content):
    try:
        rds = redis.Redis(host='127.0.0.1', port=6379)
        key = 'chatlog_%s' % contact.qq
        chatlog = rds.get(key)
        chatlog = json.loads(chatlog) if chatlog else []
        chat_msg = {'qq':member.qq, 'content':content, 'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        chatlog.insert(0, chat_msg)
        if len(chatlog) > 50:
            chatlog.pop()
        rds.set(key, json.dumps(chatlog))
    except:
        traceback.print_exc()

