import time
import glob
import json
import os
import random
from time import sleep
from io import open
from .exceptions import RetryException
from .browser import Browser

dir_path = os.path.dirname(os.path.realpath(__file__))

def randmized_sleep(average=1):
    _min, _max = average * 1 / 2, average * 3 / 2
    sleep(random.uniform(_min, _max))


class Logging(object):
  PREFIX = "facebook-crawler"

  def __init__(self):
    try:
      timestamp = int(time.time())
      self.cleanup(timestamp, dir_path)
      self.logger = open("%s/tmp/%s-%s.log" % (dir_path, Logging.PREFIX, timestamp), "w")
      self.log_disable = False
    except Exception:
      raise (Exception)
      self.log_disable = True

  def cleanup(self, timestamp, dir_path):
    days = 86400 * 7
    days_ago_log = "%s/tmp/%s-%s.log" % (dir_path, Logging.PREFIX, timestamp - days)
    for log in glob.glob("%s/tmp/facebook-crawler-*.log" % (dir_path)):
      if log < days_ago_log:
        os.remove(log)
  
  def log(self, msg):
    print(msg)
    if self.log_disable:
      return

    self.logger.write(msg + "\n")
    self.logger.flush()
  
  def __del__(self):
    if self.log_disable:
      return
    self.logger.close()

class FBCrawler(Logging):
  URL = "https://www.facebook.com"
  RETRY_LIMIT = 10

  def __init__(self, has_screen=True):
    super(FBCrawler, self).__init__()
    self.browser = Browser(has_screen)
    self.page_height = 0
  
  def login(self, username, password, filepath):
    browser = self.browser
    url = FBCrawler.URL
    browser.get(url)
    u_input = browser.find_one('input[name="email"]')
    u_input.send_keys(username)
    p_input = browser.find_one('input[name="pass"]')
    p_input.send_keys(password)
    login_btn = browser.find_by_id('u_0_b', waittime=5)
    browser.click(elem=login_btn, waittime=3)
    
  def create_group(self, username, password, filepath):
    
    #Login
    self.login(username, password, filepath)
    browser = self.browser
    index = 0

    #Click Messager
    msg = browser.find_by_id('navItem_217974574879787', waittime=5)
    if msg:
      self.log("%s login successfully" % (username))
    else:
      self.log("%s login failed" % (username))
      raise RetryException()
    browser.click(elem=msg, waittime=3)

    #Filter group
    conversation_list = browser.find_one('ul[aria-label="Conversation List"]')
    conversation = browser.find_by_tag(tag_selector='li', elem=conversation_list, waittime=1)

    for i in range(len(conversation)):
      browser.click(elem=conversation[i], waittime=3)
      titles = browser.find_all('h4[class="_1lj0 _6ybm"]', waittime=1)
      for title in titles:
        print(title.text)
        if title.text == "PEOPLE":
          index = i+1
          break 
      if index:
        self.log("Filter group success")
        break
    
    #Add to group
    users_to_add = []
    with open('%s/tmp/users.json' % (dir_path)) as f:
      users_to_add = json.load(f)
    for user in users_to_add:
      add_btn = browser.find_one('div[class="_4rpj"]')
      if add_btn.text == "Add People":
        browser.click(elem=add_btn, waittime=3)
      add_to_group = browser.find_one('input[placeholder="Add to group:"]', waittime=1)
      add_to_group.send_keys(user['username'])
      randmized_sleep(3)
      pick_user = browser.find_all('li[class="_3h3c _5l37"]')[1]
      pick_user.click()
      group_btn = browser.find_one('button[class="_3quh _30yy _2t_ _5ixy"]', waittime=1)
      browser.click(elem=group_btn, waittime=3)
      self.log("%s added tp group" % (user['username']))
    
    return users_to_add
