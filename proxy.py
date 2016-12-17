import urllib.request
import os
from bs4 import BeautifulSoup
from core.util import util

filepath = os.path.split(os.path.realpath(__file__))[0]
User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

url = 'http://www.xicidaili.com/nn/1'
req = urllib.request.Request(url, headers=header)
res = urllib.request.urlopen(req).read()

soup = BeautifulSoup(res)
ips = soup.findAll('tr')
f = open(filepath+util().separator()+"data"+util().separator()+"proxy.txt", "w")

for x in range(1,len(ips)):
    ip = ips[x]
    tds = ip.findAll("td")
    # print(tds[2].get_text())
    print(tds[1].get_text())
    # print(tds)
    ip_temp = tds[1].get_text()+"\t"+tds[2].get_text()+"\n"
    # print(tds[2].contents[0]+"\t"+tds[3].contents[0])
    f.write(ip_temp)
