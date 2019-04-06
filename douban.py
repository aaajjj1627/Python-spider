import requests

'''
模拟登陆豆瓣
'''

class DouBanLogin(object):
    def __init__(self,account,password):
        self.url = "https://accounts.douban.com/j/mobile/login/basic"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        '''初始化数据'''
        self.data = {
            "ck": "",
            "name": account,
            "password": password,
            "remember": "true",
            "ticket": ""
        }
        self.session = requests.Session()

    def get_cookie(self):
        '''模拟登陆获取cookie'''
        html = self.session.post(
            url = self.url,
            headers = self.headers,
            data=self.data
        ).json()

        if html["status"] == "success":
            print("恭喜你登陆成功")

    def get_user_data(self):
        '''获取用户数据'''
        url = "https://www.douban.com/people/88398330/"
        #获取用户信息页面
        html = self.session.get(url).text
        print (html)

    def run(self):
        self.get_cookie()
        self.get_user_data()

if __name__ == '__main__':
    account = input("请输入你的帐号:")
    password = input("请输入你的密码:")
    login = DouBanLogin(account,password)
    login.run()