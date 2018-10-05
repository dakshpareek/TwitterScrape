from selenium import webdriver
import time,os
from selenium.webdriver.chrome.options import Options


def get_token():
  options = Options()
  path = 'C://chromedriver.exe'
  options.add_argument('--headless')
  options.add_argument('--hide-scrollbars')
  options.add_argument('--disable-gpu')
  options.add_argument('--log-level=3')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--disable-extensions')
  options.add_argument('--profile-directory=Default')
  options.add_argument("--disable-infobars")
  options.add_argument("--disable-plugins-discovery")
  if os.path.isfile(path):
    driver = webdriver.Chrome(options=options, executable_path=path)
  else:
    driver = webdriver.Chrome(options=options)
  glink="https://twitter.com/KingBach/status/1045211591266848768"
  driver.get(glink)
  time.sleep(5)
  cookies_list = driver.get_cookies()
  token = ""
  for cookie in cookies_list:
      if cookie['name'] == 'gt':
          token = cookie['value']
  driver.close()
  return token
f=open('tok.txt','w')
f.write(get_token())
f.close()