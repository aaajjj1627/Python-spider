#encoding:utf8
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
'''
获取吉他五线谱
'''

def getpage():
    starturls = "http://www.yuesir.com/ipu/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    response = requests.get(url=starturls,headers=headers)
    html = response.text
    selector = etree.HTML(html)
    #获取所有链接
    urls = selector.xpath('//div[@class="page-index-main-recommend-post-item"]//a/@href')
    for url in urls:
         newurl = 'http://www.yuesir.com/ipu/'+ url
         prasepage(newurl)

def prasepage(newurl):
    url = newurl
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    response = requests.get(url=newurl,headers=headers)
    html = response.text
    html = html.encode('iso-8859-1').decode('utf8')
    soup = bs(html,'lxml')
    #获取标题
    title = soup.find("h2").string.split(' ')[0]+'.gif'
    #获取url
    url = soup.find('img',attrs={'class':'page-post-main-content-list-item-img'}).get('src')
    image = requests.get(url=url,headers=headers).content
    #下载图片并保存
    filename = title
    with open(filename, "wb") as f:
        f.write(image)
    print "已经成功下载 "+ filename


getpage()

