#ref : https://dailyeundongee.tistory.com/30를 기반으로 

import pandas as pd
from pandas import DataFrame
from pandas import ExcelWriter
import requests as req
from bs4 import BeautifulSoup

def get_fnguide_table(code):
    
    try: 
 
        ''' 경로 탐색'''
        url = req.get('http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A%s'%(code))
        url = url.content
 
        html = BeautifulSoup(url,'html.parser')
        body = html.find('body')
 
        fn_body = body.find('div',{'class':'fng_body asp_body'})
        ur_table = fn_body.find('div',{'id':'div15'})
        table = ur_table.find('div',{'id':'highlight_D_Y'})
 
        tbody = table.find('tbody')
        tr = tbody.find_all('tr')
        Table = DataFrame()
 
        for i in tr:
 
            ''' 항목 가져오기'''
            category = i.find('span',{'class':'txt_acd'})
 
            if category == None:
                category = i.find('th')   
 
            category = category.text.strip()
 
 
            '''값 가져오기'''
            value_list =[]
 
            j = i.find_all('td',{'class':'r'})
 
            for value in j:
                temp = value.text.replace(',','').strip()
 
                try:
                    temp = float(temp)
                    value_list.append(temp)
                except:
                    value_list.append(0)
 
            Table['%s'%(category)] = value_list
 
            ''' 기간 가져오기 '''    
 
            thead = table.find('thead')
            tr_2 = thead.find('tr',{'class':'td_gapcolor2'}).find_all('th')
            year_list = []
 
            for i in tr_2:
                try:
                    temp_year = i.find('span',{'class':'txt_acd'}).text
                except:
                    temp_year = i.text
                year_list.append(temp_year)
            Table.index = year_list
 
        #Table = Table.T
        Table.reset_index(level=0, inplace=True)
        Table = Table.rename(columns={'index': 'year'}) 
        Table['code'] = code
        
            #Table = Table.append(Table)
        Table = Table.loc[Table.year.isin(['2014/12', '2015/12', '2016/12', '2017/12', '2018/12', '2019/12'])]
        return Table
    
    except: 
        print('error detection!')

get_fnguide_table('023910')

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
 
code_df.종목코드 = code_df.종목코드.map("{:06d}".format)
code_df = code_df[['종목코드', '회사명', '업종', '주요제품']]
code_df = code_df.rename(columns={'종목코드': 'code', '회사명':'name', '업종' : 'industry', '주요제품' : 'main_product'})

code_df.head() #확인

code_list = code_df['code'].values.tolist()
df = pd.DataFrame(columns = [])
for i in code_list[0:5]:  #test로 5개만 해봄
    df = df.append(get_fnguide_table(i))

