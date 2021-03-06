# -*- coding: utf-8 -*-
import re
import time
import traceback
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class bili():

    def __init__(self):
        self.start()

    def start(self):
        self.driver = webdriver.PhantomJS()
        # 隐式等待时间
        self.driver.implicitly_wait(10)

    def getUrl(self, url='https://www.bilibili.com/'):
        # 滚动加载整个页面
        self.driver.get(url)
        self.driver.execute_script("""
            (function () {
                var y = 0;
                var step = 100;
                window.scroll(0, 0);

                function f() {
                    if (y < document.body.scrollHeight) {
                        y += step;
                        window.scroll(0, y);
                        setTimeout(f, 100);
                    } else {
                        window.scroll(0, 0);
                        document.title += "scroll-done";
                    }
                }

                setTimeout(f, 1000);
            })();
        """)

        for i in range(30):
            if "scroll-done" in self.driver.title:
                break
            time.sleep(10)
        print('加载完毕!')

    def screenshot(self, img='home.png'):
        self.driver.save_screenshot(img)

    def stop(self):
        self.driver.quit()


    def get_bangumi(self):
        p = self.driver.find_element(By.CLASS_NAME, 'bangumi-timing-module')
        childs = p.find_elements(By.CLASS_NAME, 'card-timing-module')
        bangumi = []
        for c in childs:
            # 旧番过滤
            try:
                ban_l = c.text.split('\n')
                nums = ban_l[1][3:]
                num = nums.replace('话','')
                if int(num) <= 12:
                    new_ban = ban_l[0] + '--' + nums
                    bangumi.append(new_ban)
                # print(c.find_element(By.TAG_NAME,'a').get_attribute('href'))
                # print(c.text)
            except:
                print('爬取新番出现bug...') 
        return bangumi

    def get_bangumi_rank(self):
        p = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[6]/div/div[2]/section/div/ul')
        childs = p.find_elements(By.CLASS_NAME, 'ri-info-wrap')
        bangumi_rank = []
        for c in childs:
            #取集数
            ban = c.text.replace('更新至','--')
            t = c.get_attribute('title')
            hit = t.split('播放:')[1]
            hit = int(hit)
            if hit > 10000:
                hit = round(hit/10000, 1)
                hit = str(hit)+'万'
            else:
                hit = str(hit)
            bangumi = '%s 播放量:%s' % (ban, hit)
            print(bangumi)
            bangumi_rank.append(bangumi)
        return bangumi_rank

    def get_element_xy(self, element, offset):
        if not offset:
            offset = (0,0,0,0)
        left = element.location['x'] + offset[0]
        top = element.location['y'] + offset[1]
        right = element.location['x'] + element.size['width'] + offset[2]
        bottom = element.location['y'] + element.size['height'] + offset[3]
        return left,top,right,bottom

    def cut_img(self, img='home.png', newimg='t.png', **kargs):
        
        left = kargs['left']
        top = kargs['top']
        right = kargs['right']
        bottom = kargs['bottom']

        im = Image.open(img) 
        im = im.crop((left, top, right, bottom))
        im.save(newimg)

    def get_time_bangumi(self, day):
        '''1-昨天,2-今天,3-明天'''
        try:
            self.getUrl('https://bangumi.bilibili.com/anime/timeline')
            self.screenshot('time_bangumi.png')
            p = self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[2]/div[%s]'%(day))
            left,top,right,bottom = self.get_element_xy(p, (11,-60,25,10))
            kwargs = {
                'left' : left,
                'top' : top,
                'right' : right,
                'bottom' : bottom
            }
            new_img = 'cut_bangumi_%s.png'%(day)
            self.cut_img('time_bangumi.png', new_img, **kwargs)
            return new_img
        except:
            traceback.print_exc()

    def get_osu_homepage(self, username):
        '''1-昨天,2-今天,3-明天'''
        try:
            self.getUrl('https://osu.ppy.sh/users/%s' % username)
            save_img = '%s_homepage.png' % username
            self.screenshot(save_img)
            p = self.driver.find_element(By.XPATH, '/html/body/div[9]/div/div/div[1]/div[2]/div[2]/div[3]')
            left,top,right,bottom = self.get_element_xy(p, (0,0,20,0))
            kwargs = {
                'left' : left,
                'top' : top,
                'right' : right,
                'bottom' : bottom
            }
            print(kwargs)
            new_img = 'cut_%s_homepage.png' % username
            self.cut_img(save_img, new_img, **kwargs)
            return new_img
        except:
            traceback.print_exc()

def test():
    # bi.getUrl(img='time_bangumi.png', url='https://bangumi.bilibili.com/anime/timeline')
    # p = self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[2]/div[2]')
    # print(p.location['x'],p.location['y'],p.size['width'],p.size['height'])
    left = 60 #+11
    top = 802  #-60
    right = 350 #+25
    bottom = 957 #+10
    # im = Image.open('time_bangumi.png') 
    im = Image.open('-interesting-_homepage.png')
    im = im.crop((left, top, right, bottom))
    im.save('t.png')
    # bi.stop()


if __name__ == "__main__":
    bi = bili()
    # bi.get_time_bangumi(2)
    bi.get_osu_homepage('-inter-')
    # bi.getUrl()
    # # bi.get_bangumi()
    # # bi.get_bangumi_rank()
    bi.stop()


    # test()
