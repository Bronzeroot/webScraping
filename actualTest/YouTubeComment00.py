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

vd_title = soup.select("h1.title.style-scope.ytd-video-primary-info-renderer")[0].text
vd_tmp_views = soup.select("span.view-count")[0].text
vd_views = int(re.sub(r'[^0-9]', '', vd_tmp_views))
vd_tmp_comments = soup.select("yt-formatted-string.count-text")[0].text
vd_comments = int(re.sub(r'[^0-9]', '', vd_tmp_comments))
vd_likes = int(soup.select("yt-formatted-string#text.style-scope.ytd-toggle-button-renderer.style-text", id='text')[0].text)
vd_channel = soup.select("yt-formatted-string#text.style-scope.ytd-channel-name")[0].text
vd_subscribers = soup.select("yt-formatted-string#owner-sub-count.style-scope.ytd-video-owner-renderer")[0].text

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
cmt_data = {'Comment': str_cmt_text, 'Likes' : int_cmt_likes}
video_data = {'Url': url, 'Title': vd_title, 'Views': vd_views, 'Comments':vd_comments, 'Likes' : vd_likes, 'Channel': vd_channel ,'Subscribers': vd_subscribers}
pd_data = {'Url': url, 'VD_Title': vd_title, 'VD_Views': vd_views, 'VD_Comments':vd_comments, 'VD_Likes' : vd_likes, 'VD_Channel': vd_channel ,'VD_Subscribers': vd_subscribers,'Cmt_text': str_cmt_text, 'Cmt_Likes' : int_cmt_likes}
#pd_data = {'Comment': str_cmt_text, 'Likes' : int_cmt_likes, 'Reply' : str_cmt_reply }
youtube_pd = pd.DataFrame(pd_data) 
#youtube_pd.to_csv('YouTubeCmt.csv',encoding = 'utf-8-sig', index = False, header = True)
