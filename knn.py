#-*- coding:UTF-8 -*-
import nltk
import urllib,http.cookiejar,os

filepath = os.path.split(os.path.realpath(__file__))[0]
def getchk(number):
    #创建cookie对象
    cookie = http.cookiejar.LWPCookieJar()
    cookieSupport= urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookieSupport, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    #首次与教务系统链接获得cookie#
    #伪装browser
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'
    }
    req0 = urllib.request.Request(
            url ='http://mis.teach.ustc.edu.cn',
            headers = headers               #请求头
    )
    # 捕捉http错误
    try :
        result0 = urllib.request.urlopen(req0)
    except Exception as e:
        print(e.code)
    #提取cookie
    getcookie = ['',]
    for item in cookie:
        getcookie.append(item.name)
        getcookie.append("=")
        getcookie.append(item.value)
        getcookie = "".join(getcookie)

    #修改headers
    headers["Origin"] = "http://mis.teach.ustc.edu.cn"
    headers["Referer"] = "http://mis.teach.ustc.edu.cn/userinit.do"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Cookie"] = getcookie
    for i in range(number):
        req = urllib.request.Request(
            url ="http://mis.teach.ustc.edu.cn/randomImage.do?date='1469451446894'",
            headers = headers                 #请求头
        )
        response = urllib.request.urlopen(req)
        status = response.getcode()
        picData = response.read()
        if status == 200:
            localPic = open(filepath+"/data/source/"+str(i)+".jpg", "wb")
            localPic.write(picData)
            localPic.close()
        else:
            print("failed to get Check Code ")
def sentence():

    pass

if __name__ == '__main__':
    getchk(500)
