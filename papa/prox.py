# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用

import re
import requests
import random

def get_ip_list(url, headers):
    res = requests.get(url, headers=headers)
    value = re.compile(r'<td class="country">.*?</td><td>(.*?)</td>',re.S)
    values = value.findall(res.text)
    print (values)

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

if __name__ == '__main__':
    page = random.randint(1, 525)
    url = 'http://www.xicidaili.com/nt/%s' % page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    # proxies = get_random_ip(ip_list)
    # print(proxies)