import requests
from requests import RequestException
import json
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
'''
获取豆瓣书
'''

#获取一页的html源码
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        # 如果状态码等于200返回html源码
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


#解析源码，拿到想要的内容
def parse_one_page(html):
	soup = bs(html,'lxml')

	doulist = soup.find_all(name='div',attrs={'class','doulist-item'})
	for book in doulist:
		#书的序号
		seq = book.find(name='span',attrs={'class':'pos'}).get_text()
		#print(seq)
		#图片url
		jpg_url = book.find(name='img').get('src')
		#print(jpg_url)
		#书名
		book_name = book.find(name='div', attrs={'class': 'title'}).get_text().replace(' ', '').replace("\n\n", "")
		book_star = book.find(name='blockquote', attrs={'class': 'comment'}).get_text().replace(' ', '').replace("\n\n", "、").replace("\n","")
		#print(book_name)
		#书作者、出版社、时间
		book_author = book.find(name='div', attrs={'class': 'abstract'}).get_text().replace(' ', '').replace("\n\n", "、").replace("\n","")
		#print(book_author)
		yield{
			"seq":seq,
			"jpg_url": jpg_url,
            "book_name": book_name,
            "book_author": book_author,
            "book_star": book_star
		}
#写入文件中
def write_to_file(content):
	#如果不加ensure_ascii=False,中文会变成ascii的编码格式
	with open('book.txt','a',encoding='utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False)+'\n')
		f.close()

def main(offset):
	#注释下面的主页，因为分析第一页也可以写成0的形式
    url = 'https://www.douban.com/doulist/1264675/?start=' + str(offset) + '&sort=seq&sub_type='
    html = get_one_page(url)
    #返回的是一个字典
    book_dict = parse_one_page(html)
    for content in book_dict:
        print(content)
        write_to_file(content)

if __name__ == '__main__':
	# 创建进程池，加快爬取速度
    pool = Pool()
    #进程池的映射方法,第一个参数传入函数,第二个传入参数,用生成器生成了一个步长为25，循环20次列表
    pool.map(main, [i * 25 for i in range(20)])
    pool.close()  # 关闭进程池，不再接受新的进程
    pool.join()  # 主进程阻塞等待子进程的退出


