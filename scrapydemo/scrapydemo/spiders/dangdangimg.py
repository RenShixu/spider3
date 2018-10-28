# -*- coding: utf-8 -*-
import scrapy,re
from scrapydemo.items import Book


class DangdangimgSpider(scrapy.Spider):
    name = 'dangdangimg'
    allowed_domains = ['http://search.dangdang.com/']
    start_urls = ['http://search.dangdang.com/?key=python&act=input']

    def parse(self, response):
        bookitems = response.css("ul.bigimg li")
        i = 0
        for item in bookitems:
            book = Book()
            book['name'] = item.xpath("./a[1]/@title").extract_first()
            if i == 0:
                book['img'] = item.xpath("./a[1]/img/@src").extract_first()
            else:
                book['img'] = item.xpath("./a[1]/img/@data-original").extract_first()
            book['text'] = item.css("p.name a::attr(title)").extract_first()
            book['price'] = item.css("p.price span.search_now_price::text").extract_first()[1:]
            discounttext = item.css("p.price span.search_discount::text").extract_first()
            book['discount'] = re.findall("\(([\.0-9]+)折\)",discounttext)[0]
            author = item.css("p.search_book_author").xpath("./span[1]/a[1]/@title").extract_first()
            if author:
                book['author'] = author
            else:
                book['author'] = item.css("p.search_book_author").xpath("./span[1]/text()").extract_first()
            book['time'] = item.css("p.search_book_author").xpath("./span[2]/text()").extract_first()[2:]
            book['press'] = item.css("p.search_book_author").xpath("./span[3]/a[1]/@title").extract_first()
            i += 1
            yield book

        print(len(bookitems))
