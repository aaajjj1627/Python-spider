import re
import requests
from lxml import etree
'''
爬取小说
'''

#定义一个爬取网络小说的函数
def getNovelContent():
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
	html =  requests.get("http://www.quanshuwang.com/book/44/44683",headers=headers).text
	html = html.encode('iso-8859-1').decode('gbk') #转换该网站的格式

	#解析html为HTML文档
	selector1 = etree.HTML(html)
	#提取出链接
	urls = selector1.xpath('//div[@class="clearfix dirconone"]/li/a/@href')
	for url in urls:
		text = requests.get(url,headers=headers).text
		text = text.encode('iso-8859-1').decode('gbk')
		selector2 = etree.HTML(text)
		chapter_title = selector2.xpath('//div[@class="bookInfo"]//strong/text()')
		title = chapter_title[0].replace("章 节目录 ","")
		chapter_content = selector2.xpath('//div[@class="bookInfo"]/div/text()')

		for content in chapter_content:
			content = content.replace("\'\r\n\xa0\xa0\xa0\xa0","")
			content = content.replace(r"'\r\n'","")
			print(content)
			f = open('{}.txt'.format(title),"w")
			f.write(content)

getNovelContent()
