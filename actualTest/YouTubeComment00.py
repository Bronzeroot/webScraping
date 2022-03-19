from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup
import re

#Target URL 
driver = webdriver.Chrome()
url = "https://www.youtube.com/watch?v=k8S7XnVxusg"
driver.get(url)

#Scroll down to the bottom 
last_page_height = driver.execute_script('return document.documentElement.scrollHeight')

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2.0)
    new_page_height = driver.execute_script('return document.documentElement.scrollHeight')

    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height

    
#Parsing    
html_source = driver.page_source
driver.close()
soup = BeautifulSoup(html_source, 'lxml')

#Scrapping
cmt_text = soup.select("yt-formatted-string#content-text")
cmt_likes = soup.select("span#vote-count-middle")
#cmt_comments = soup.select()


str_cmt_text = []
int_cmt_likes = []
#str_cmt_reply = []


for i in range(len(cmt_text)):
    str_tmp = str(cmt_text[i].text)
    str_tmp = str_tmp.replace('\n','')
    str_tmp = str_tmp.replace('\t','')
    str_tmp = str_tmp.replace('           ', '')
    str_cmt_text.append(str_tmp)

for i in range(len(cmt_likes)):
    int_tmp = str(cmt_likes[i].text)
    int_tmp = int_tmp.replace('\n','')
    int_tmp = int_tmp.replace('\t','')
    int_tmp = int_tmp.replace('           ', '')
    int_tmp = int(int_tmp)
    int_cmt_likes.append(int_tmp)
    
#    str_tmp = str(cmt_reply[i].text)
#    str_tmp = str_tmp.replace('\n','')
#    str_tmp = str_tmp.replace('\t','')
#    str_tmp = str_tmp.replace('           ', '')
#    str_cmt_reply.append(str_tmp)

#Pandas to CSV
pd_data = {'Comment': str_cmt_text, 'Likes' : int_cmt_likes}
#pd_data = {'Comment': str_cmt_text, 'Likes' : int_cmt_likes, 'Reply' : str_cmt_reply }
youtube_pd = pd.DataFrame(pd_data) 
#youtube_pd.to_csv(r'', index = False, header = True)
