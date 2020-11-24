from selenium import webdriver as wd
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
# https://github.com/SOMJANG/Youtube_Comment_Crawler을 메인으로, 기타 커뮤니티를 참고하였습니다.
driver = wd.Chrome("C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
url = 'http://www.youtube.com/watch?v=I0RVlki14gI'
driver.get(url)

last_page_height = driver.execute_script('return document.documentElement.scrollHeight')

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(3.0)
    new_page_height = driver.execute_script('return document.documentElement.scrollHeight')

    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height

html_source = driver.page_source

driver.close()

soup = BeautifulSoup(html_source, 'lxml')

youtube_user_IDs = soup.select('div#header-author > a > span')

youtube_comments = soup.select('yt-formatted-string#content-text')

str_youtube_userIDs = []
str_youtube_comments = []

for i in range(len(youtube_user_IDs)):
    str_tmp = str(youtube_user_IDs[i].text)
#    print(str_tmp)
    str_tmp = str_tmp.replace('\n','')
    str_tmp = str_tmp.replace('\t','')
    str_tmp = str_tmp.replace('           ', '')
    str_youtube_userIDs.append(str_tmp)

    str_tmp = str(youtube_comments[i].text)
    str_tmp = str_tmp.replace('\n','')
    str_tmp = str_tmp.replace('\t','')
    str_tmp = str_tmp.replace('           ', '')
    str_youtube_comments.append(str_tmp)


pd_data = {'ID':str_youtube_userIDs, 'Comment':str_youtube_comments}

youtube_pd = pd.DataFrame(pd_data)
youtube_pd.to_csv(r'C:/Users/Administrator/export_dataframe.csv', index = False, header = True)
