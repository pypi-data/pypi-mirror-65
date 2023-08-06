from nltk.tokenize import sent_tokenize
import os
import itertools
import time

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


from multiprocessing.pool import ThreadPool, Pool
import threading

class translate:


    def __init__(self,data,tolang,fromlang='en',thread=1,filename=None):
        self.data=data
        self.fromlang=fromlang
        self.tolang=tolang
        self.thread=thread
        self.threadLocal = threading.local()
        self.filename=filename
        self.cdriver=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver')
    
    def driver_create(self):
        driver = getattr(self.threadLocal, 'driver', None) 
        if driver is None: # check if thread has it's driver
            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu") # efficient web driver initization
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(self.cdriver,options=chrome_options)
            driver.get(f"https://translate.google.com/#view=home&op=translate&sl={self.fromlang}&tl={self.tolang}") 
            setattr(self.threadLocal, 'driver', driver)
        return driver

    def translate(self):

        def trans_get(text):
            driver=self.driver_create()
            wait = WebDriverWait(driver, 10)
            input=wait.until(lambda driver: driver.find_element_by_xpath('//textarea[@id="source"]')) # get input textarea if it exists
            input.send_keys(text)
            time.sleep(0.7)
            output=wait.until(lambda driver: driver.find_element_by_xpath('//span[@class="tlid-translation translation"]')) # get output if it exists
            c=output.text
            time.sleep(0.7) # wait to avoiding repetated copy
            input.clear()
            if self.filename != None:
                if type(self.filename) == str:
                    with open(self.filename,'a') as f:
                        f.write(c)
                else:
                    filename=str(self.filename)
                    with open(self.filename,'a') as f:
                        f.write(c)
            else:
                return c
        
        if type(self.data) is list:
            return ThreadPool(self.thread).map(trans_get,self.data)
        elif type(self.data) is str:
            return ThreadPool(self.thread).map(trans_get,[self.data])
        else:
            try:
                return ThreadPool(self.thread).map(trans_get,self.text)
            except:
               pass
                