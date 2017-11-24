# -*- coding: utf-8 -*-
import pymysql  
import datetime


def onQQMessage(bot, contact, member, content):
    # 当收到 QQ 消息时被调用
    # bot     : QQBot 对象，提供 List/SendTo/GroupXXX/Stop/Restart 等接口，详见文档第五节
    # contact : QContact 对象，消息的发送者
    # member  : QContact 对象，仅当本消息为 群或讨论组 消息时有效，代表实际发消息的成员
    # content : str 对象，消息内容
    if contact.ctype == 'group' and len(content)>0:
        insertChatContent(bot,contact,member,content)


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
        print('insert success', cursor.rowcount, ' record')
    except:
        print('insert fail')
        connect.rollback()