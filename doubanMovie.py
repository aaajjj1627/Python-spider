import requests
import json

#定义请求url
url =  "https://movie.douban.com/j/search_subjects"

#定义请求头
headers = {
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}

#循环构建请求参数并且发送请求
for page_start in range(0,100,20):
    params = {
        "type": "movie",
        "tag": "热门",
        "sort": "recommend",
        "page_limit": "20",
        "page_start": page_start
    }
    resonse = requests.get(
        url=url,
        headers=headers,
        params=params
    )
    #方法一：直接转换成json方法
    #  result = resonse.json()
    #方法二:手动转换
    #获取字符串
    content = resonse.content
    #转换成字符串
    string = content.decode('utf-8')
    #把字符串转换成python数据类型
    results = json.loads(string)
    #解析结果
    for movie in results["subjects"]:
        print(movie["title"],movie["rate"])