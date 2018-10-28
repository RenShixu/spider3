import scrapy

class XinLang(scrapy.Spider):
    name = "xinlang"
    allowed_domains = ["http://news.sina.com.cn"]
    start_urls = ["http://news.sina.com.cn/guide/"]

    def parse(self, response):
        navlist = response.css("div.section")
        for item1 in navlist:
            print("="*5+"一级菜单"+"="*5)
            item1s = item1.css("h2.tit01::text").extract()
            print("-".join(item1s))


            item2s = item1.css("div.clearfix")
            for item2 in item2s:
                print("=" * 10 + "二级级菜单" + "=" * 10)
                print(item2.css("h3.tit02 a::text,h3.tit02::text,h3.tit02 span::text").extract_first())
                item3s = item2.css("ul.list01")
                for item3 in item3s:
                    print("=" * 20 + "三级级菜单" + "=" * 20)
                    print(item3.css("li a::text").extract())


