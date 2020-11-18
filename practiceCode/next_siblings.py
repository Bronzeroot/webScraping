from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html,'html.parser')

for sibling in bs.find('table',{'id': 'giftList'}).tr.next_siblings:
    print(sibling)
#첫번째 타이틀 행을 제외한 모든 제품 행을 가져온다
#객체는 자기 자신의 Sibling이 되지 않아서, 객체 자체는 그 목록에서 제외된다. (Title을 선택하고 next_siblings 호출하면 타이틀을 제외한 모든 행을 선택한다)
