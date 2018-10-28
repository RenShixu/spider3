# -*- coding: utf-8 -*-
import scrapy,time,json,re
from scrapy.http import FormRequest
from scrapy.http import Request

class RenrenloginSpider(scrapy.Spider):
    name = 'renrenlogin'
    allowed_domains = ['http://www.renren.com/']
    start_urls = ["http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp="]

    def start_requests(self):
        systime = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        url = self.start_urls[0] + systime

        params = {
            'email': '15988402262',
            'icode': '',
            'origURL': 'http://www.renren.com/home',
            'domain': 'renren.com',
            'key_id': '1',
            'captcha_type': 'web_login',
            'password': '971c4bd3c4afb972a7160003f3fb9a6fac54404d49b2a4790b7e66863379548f',
            'rkey': 'd6b3acc434f19c92fad1f33176e506f0',
            'f': 'http%3A%2F%2Fwww.renren.com%2F968476078'
        }

        '''POST请求发送'''
        request = FormRequest(url, formdata=params, callback=self.pase_home)
        yield request

    def pase_home(self, response):
        returndata = json.loads(response.body)
        if returndata["code"]:
            cookie = response.headers.getlist('Set-Cookie')
            print(cookie)
            cookiestr = ''.join(str(s) for s in cookie if s not in [None])
            pat = "b'id=([0-9]+); domain"
            userids = re.findall(pat,cookiestr)
            print(userids)
            homeurl = "http://www.renren.com/" + userids[0]
            headers = {
                'Cookie':'anonymid=jnoj7vh7-kfvtys; depovince=GW; _r01_=1; ln_uact=15988402262; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; JSESSIONID=abc0Gs8LZhwtjbNXFz4Aw; ick_login=01aed9f0-1351-4c92-addf-8adf1eb29e03; jebe_key=4d79cc41-10dc-4c02-9f7a-eb32675eb913%7Ca6b6e8d2ffb58d72d790df2637dc04b6%7C1540471508008%7C1%7C1540691988312; first_login_flag=1; wp_fold=0; jebecookies=9e259aa2-1043-4cb0-8511-8794dc3c459d|||||; _de=CB5CC0B86146D9F8488E4C840EF79200; p=699cf7e86c6d8fe7b7676b90b3bad64f8; t=143d4ed788705d9a3bd65f6f83177d338; societyguester=143d4ed788705d9a3bd65f6f83177d338; id=968476078; xnsid=477dc9c5; ver=7.0; loginfrom=null',
                'Referer':'http://www.renren.com/SysHome.do',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3452.0 Safari/537.36'
            }
            request = Request(url=homeurl,headers=headers,method='GET',callback=self.pase_homepage)
            yield request
    def pase_homepage(self,response):
        print("-----------------------------")
        print(response.body)

