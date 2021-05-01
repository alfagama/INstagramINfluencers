import re
import os
import errno
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from credentials import *
import mongo


class scraper():
    """
    Scraper Class
    """

    def get_comments(self, urls, driver, name, num_comment=None):
        """
        Writes all comments of every post in csv / mongoDB
        :param urls: urls of posts (list)
        :param driver: ChromeDriverManager
        :param name: influencer name (string)
        :param num_comment: total num of comments to use as limit (int)
        :return: -
        """
        # set def wait 15 secs
        self.wait = WebDriverWait(driver, 15)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Fifk5')))
        # wait 10 to load -> increase if you have slow internet connection (Εγώ είμαι με 50Mbps για αναλογία!)
        time.sleep(10)
        # set empty lists (users, comments and likes)
        self.users = []
        self.texts = []
        self.likes = []
        self.num_comment = num_comment
        # loop through all URLs to get the comments
        for url in urls:
            print('Get post, URL: ', url)
            driver.get(url)
            self.loop = True
            self.no = 1
            self.a = 0
            while self.loop:
                try:
                    # (+))
                    self.more_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'dCJp8')))
                    # click for more comments (+)
                    self.more_btn.click()
                    # counter for how many times (+) button was pressed
                    # print('Click load more:', self.no)
                    self.no += 1
                    # comments name
                    self.b = len(driver.find_elements_by_class_name('Mr508'))
                    try:
                        # next line changed for num of comments -> now takes all -> better
                        if self.b > self.num_comment:  # only take num_comment (eg. only take 50 comments)
                            print('Number of comment > {}'.format(self.num_comment))
                            self.loop = False
                    except TypeError:
                        pass
                    if self.a == self.b:
                        print('No more comment!')
                        self.loop = False
                    else:
                        self.a = self.b
                except TimeoutException:
                    print('No "Load More" comment button. (+)')
                    self.loop = False
                except StaleElementReferenceException:
                    print('Some element is missing, anyway keep going! :D')
                    continue

            print('Load comments')
            self.comments = driver.find_elements_by_class_name('Mr508')
            for i in self.comments[:self.num_comment]:
                # i.text.replace('Verified', '')
                if i.text.split('\n')[1] == 'Verified':
                    self.user = i.text.split('\n')[0]
                    self.text = i.text.split('\n')[2]
                    self.like = i.text.split('\n')[3]
                else:
                    self.user = i.text.split('\n')[0]
                    self.text = i.text.split('\n')[1]
                    self.like = i.text.split('\n')[2]
                # get number of likes -> maybe we will need for importance of comment!?
                try:
                    self.like = re.findall(r'\d+', self.like)[1]
                except Exception:
                    self.like = '0'
                self.like = int(self.like)

                self.users.append(self.user)
                self.texts.append(self.text)
                self.likes.append(self.like)
                print("User: ", self.user, "Text: ", self.text, " Like: ", self.like)
            print('Get {} comments'.format(len(self.comments[:self.num_comment])))
            # create DF -> new every time
            df = pd.DataFrame()
            # create cols and pass users / texts / likes
            df['user'] = scraper.users
            df['comment'] = scraper.texts
            df['like'] = scraper.likes
            # print('export csv')
            # write to .csv -> name is content URL -> any better ideas? :P
            url_lastname = url[28:-1]
            df.to_csv(f'data/scrape_comments/{name}/{url_lastname}.csv', index=False)
            # update MongoDB with comments of all posts
            mongo.update_comments(df, name, url)
            # clear everything for next URL
            df = df.drop(df.index, inplace=True)
            self.users = []
            self.texts = []
            self.likes = []


def initialize_scraper(name, urls_list):
    """
    Method to initialize scraper and call 'get_comments' for all user's posts.
    :param name: influencer name (string)
    :param urls: post URLs (list)
    :return: -
    """
    # create directory for user = name
    try:
        os.makedirs(f'data/scrape_comments/{name}')
        print("Created new directory for user: ", name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    # manual ChromeDriverManager()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # set website URL
    url = "https://www.instagram.com"
    driver.get(url)
    time.sleep(4)
    # find username element
    username_el = driver.find_element_by_name("username")
    # pass USERNAME
    username_el.send_keys(USERNAME)
    # find password element
    password_el = driver.find_element_by_name("password")
    # pass PASSWORD
    password_el.send_keys(PASSWORD)
    # find submit!
    submit_btn_el = driver.find_element_by_css_selector("button[type='submit']")
    # we are in!.. let's wait a little! :D
    time.sleep(1)
    # click submit!!
    submit_btn_el.click()
    # call get_comments method
    scraper.get_comments(scraper, urls_list, driver, name, 500)  # getting only the 100 first comments!
