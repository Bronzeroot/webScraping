from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html,'html.parser')

nameList = bs.findAll('span',{'class':'green'})
#green에는 인물이, Red에는 대사가 들어있음
for name in nameList:
    print(name.get_text())
