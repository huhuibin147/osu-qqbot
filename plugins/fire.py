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
        self.driver = webdriver.Firefox()
        # 隐式等待时间
        self.driver.implicitly_wait(10)

    def getUrl(self, url):
        self.driver.get(url)
        

    def screenshot(self, img):
        self.driver.save_screenshot(img)

    def stop(self):
        self.driver.quit()

    def get_rank_chart(self, username):
        try:
            self.getUrl('https://osu.ppy.sh/users/%s' % username)
            p = self.driver.find_element(By.XPATH, '/html/body/div[9]/div/div/div[1]/div[2]/div[2]/div[3]')
            img = '%s_rank_chart.png' % username
            p.screenshot(img)
            return img
        except:
            traceback.print_exc()


if __name__ == "__main__":
    bi = bili()
    bi.get_rank_chart('-inter-')
    # bi.stop()


