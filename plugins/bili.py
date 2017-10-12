# -*- coding: utf-8 -*-
import re
import time
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



# def test():
    # e = driver.find_element_by_xpath('/html/body/div[3]/div[6]/div/div[2]/section')
    # e.screenshot('a.png')
    # actions = webdriver.ActionChains(driver)
    # actions.move_to_element(e)
    # actions.perform()

    # e.location #{'x':720,'y':1663}
    # e.size #{'height':445,'width':260}

    # e = driver.find_element_by_xpath('//*[@id="bili_bangumi"]/div')

if __name__ == "__main__":
    bi = bili()
    bi.getUrl()
    # bi.get_bangumi()
    bi.get_bangumi_rank()
    bi.stop()
