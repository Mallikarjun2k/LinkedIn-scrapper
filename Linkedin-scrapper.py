from requests.api import request
from time import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv

def main():
  driver=webdriver.Chrome()
  #LinkedIn Login
  url='https://www.linkedin.com/login'
  driver.get(url)
  sleep(1)
  email_id=driver.find_element_by_id('username')
  #Provide login credential
  email_id.send_keys('Your Email or username')
  sleep(1)
  pass_id=driver.find_element_by_name('session_password')
  pass_id.send_keys('Your password')
  sleep(1)
  log_in=driver.find_element_by_class_name('login__form_action_container ')
  log_in.click()
  sleep(4)
  #To scroll infine page
  last_height = driver.execute_script("return document.body.scrollHeight")
  while True:
          driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          sleep(4)
          new_height = driver.execute_script("return document.body.scrollHeight")
          sleep(4)
          if new_height == last_height:
              break
          last_height =new_height

  page = driver.page_source
  sleep(1)
  soup=BeautifulSoup(page,'html.parser')
  posts=[]
  post={}
  #Extracting Profile  & description
  membername=[]
  p_name=soup.find_all('span',class_="feed-shared-actor__name t-14 t-bold hoverable-link-text t-black" )
  for name in p_name:
    p_name=name.text.replace('\n','')
    membername.append(p_name)
  post['membername']=membername

  description=[]
  despn=soup.find_all('span', class_="break-words")
  for des in despn:
    despn=des.text.replace('\n',' ')
    description.append(despn)
  post['description']=description

  #Date of posting
  postdate=[]
  dates=soup.find_all('span',class_="feed-shared-actor__sub-description t-12 t-normal t-black--light")
  for date in dates:
    dates=date.text.replace('\n','')
    postdate.append(dates)
  post['postdate']=postdate
 
  posts.append(post)
  #CSV file
  with open('filename.csv', 'w', newline='', encoding="UTF-8") as f:
      c = csv.writer(f)
      for key, value in post.items():
          c.writerow([key] + value)
if __name__ == '__main__':
  main()