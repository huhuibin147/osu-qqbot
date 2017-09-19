import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt 
import pymysql

conn = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='osu', charset='utf8')
osu_api_key = 'b68fc239f6b8bdcbb766320bf4579696c270b349'
def get_cursor():
    return conn.cursor()

def get_map(country='CN'):
    cur = get_cursor()
    sql = '''
        SELECT pp_raw FROM osu_user where country = %s
    '''
    cur.execute(sql, country)
    res = cur.fetchall()

    rank_map2 = {
        '0-1000pp'  : [0, 'orange'],
        '1000-2000pp' : [0, 'teal'],
        '2000-3000pp' : [0, 'slateblue'],
        '3000-4000pp' : [0, 'crimson'],
        '4000-5000pp' : [0, 'forestgreen'],
        '5000-6000pp' : [0, 'hotpink'],
        '6000-7000pp' : [0, 'indigo'],
        '7000-14000pp' : [0, 'lightpink']
    }

    for r in res:
        if 1000 > r[0] >= 0:
            rank_map2['0-1000pp'][0] += 1
        elif 2000 > r[0] >= 1000:
            rank_map2['1000-2000pp'][0] += 1
        elif 3000 > r[0] >= 2000:
            rank_map2['2000-3000pp'][0] += 1
        elif 4000 > r[0] >= 3000:
            rank_map2['3000-4000pp'][0] += 1
        elif 5000 > r[0] >= 4000:
            rank_map2['4000-5000pp'][0] += 1
        elif 6000 > r[0] >= 5000:
            rank_map2['5000-6000pp'][0] += 1
        elif 7000 > r[0] >= 6000:
            rank_map2['6000-7000pp'][0] += 1
        elif r[0] >= 7000:
            rank_map2['7000-14000pp'][0] += 1
    
    return rank_map2




# mpl.rcParams['axes.titlesize'] = 20
# mpl.rcParams['xtick.labelsize'] = 16
# mpl.rcParams['ytick.labelsize'] = 16
# mpl.rcParams['axes.labelsize'] = 16
mpl.rcParams['xtick.major.size'] = 0
mpl.rcParams['ytick.major.size'] = 0

def draw_zhu():
    rank_map = {
        'int'  : (2300, 'orange'),
        'heisiban' : (1700, 'teal'),
        'louxinye' : (4400, 'slateblue'),
        'inter' : (3400, 'crimson')
    }

    #柱状图
    fig = plt.figure('pp rank',figsize=(9,9))
    ax = fig.add_subplot(111)
    ax.set_title('pp - CN')
    xticks = np.arange(9)
    bar_width = 0.5
    users = rank_map2.keys()
    pp = [x[0] for x in rank_map2.values()]
    colors = [x[1] for x in rank_map2.values()]
    bars = ax.bar(xticks, pp, width=bar_width, edgecolor='none')
    ax.set_ylabel('nums')
    ax.set_xticks(xticks)
    # ax.set_xlim([bar_width/2-0.5, 3-bar_width/2])
    ax.set_xticklabels(users)
    # ax.set_ylim([0, 11000])
    for bar, color in zip(bars, colors):
        bar.set_color(color)

    #饼图
    fig = plt.figure('pp rank2',figsize=(7,7))
    ax = fig.add_subplot(111)
    labels = ['{}\n{} pp'.format(u, p) for u, p in zip(users, pp)]
    ax.pie(pp, labels=labels, colors=colors)



def draw_bin():
    # 饼图
    rank_map2 = get_map('US')
    pp_label = rank_map2.keys()
    pp_num = [x[0] for x in rank_map2.values()]
    colors = [x[1] for x in rank_map2.values()]
    fig = plt.figure('pp rank2',figsize=(9,9))
    ax = fig.add_subplot(111)
    labels = ['{}:{}'.format(u, p) for u, p in zip(pp_label, pp_num)]
    ax.pie(pp_num, labels=labels, colors=colors)
    plt.show()

# draw_bin()

def draw_country():
    fig = plt.figure('pp rank3',figsize=(8,8))
    # country = ['CN','TW','HK','AU','CA','FR','GB','JP','KR','PL','RU','US']
    country = ['CN','KR','PL','RU','US']
    for i,c in enumerate(country):
        map2 = get_map(c)
        pp_label = map2.keys()
        pp_num = [x[0] for x in map2.values()]
        colors = [x[1] for x in map2.values()]
        x = range(len(pp_label))
        plt.plot(x, pp_num,  label=country[i])  
    plt.xticks(x, pp_label, rotation=0)
    plt.legend()
    plt.show()
draw_country()