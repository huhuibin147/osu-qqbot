# -*- coding: utf-8 -*-
import pymysql  
import traceback

class osu():
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu',charset='utf8')

    def conn_db(self):
        self.conn = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu',charset='utf8')

    def get_cursor(self):
        if not self.conn:
            self.conn_db()
        return self.conn.cursor(pymysql.cursors.DictCursor)
        # return self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_chatlog(self):
        try:
            cur = self.get_cursor()
            sql = '''
                SELECT * FROM chat_logs
            '''
            cur.execute(sql)
            res = cur.fetchall()
            if not res:
                return []
            return res
        except:
            traceback.print_exc()

def chat2txt(chatlist):
    with open('.qqbot-tmp\plugins\cbot\chat.txt','w',encoding='utf8') as fc:
        for r in chatlist:
            if check_content(r['content']):
                fc.write(r['content']+'\n')

def check_content(content):
    filters = ['!', '！', '~', '～', '个人信息', 'BP指标', '目前潜力', 'Beatmap by', '[@M', 'inter去ppy', 'inter忘',\
        'inter推荐给', '目前的词库量', 's 战绩', '星级:', 'winner榜' , 'loser榜', 'Stamina :', '[视频]', '今日更新的bp',\
        '更新了bp', 'rank:' ,'s skill', '相关词']
    for f in filters:
        if f in content:
            return False
    return True

# if __name__ == '__main__':
#     o = osu()
#     chatlist = o.get_chatlog()
#     chat2txt(chatlist)

