# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,os
from urllib import request

class ScrapydemoPipeline(object):
    def process_item(self, item, spider):
        return item

class DangdangBookInfo(object):
    def __init__(self,host,database,user,password,port):
        self.host = host
        self.database = database
        self.password = password
        self.user = user
        self.port = port

    '''读取配置文件信息'''
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get("MYSQL_HOST"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            password=crawler.settings.get("MYSQL_PASS"),
            user=crawler.settings.get("MYSQL_USER"),
            port=crawler.settings.get("MYSQL_PORT"),
        )

    '''连接数据库'''
    def open_spider(self,spider):
        self.db = pymysql.connect(self.host,self.user,self.password,self.database,charset="utf8",port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        itemdict = dict(item)
        colums = ",".join(itemdict.keys())
        values = ",".join(["%s"]*len(item))
        sql = "insert into %s(%s) values (%s)"%(item.table,colums,values)
        self.cursor.execute(sql,tuple(itemdict.values()))
        self.db.commit()
        return item

    '''关闭数据连接'''
    def close_spider(self,spider):
        self.db.close()

class DangdangBookImgDeal(object):
    def __init__(self,imgpath):
        self.imgpath = imgpath

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            imgpath=crawler.settings.get("IMG_PATH")
        )

    def process_item(self,item,spider):
        if not os.path.exists(self.imgpath):
            os.mkdir(self.imgpath)
        imgname = item["img"].split("/").pop()
        request.urlretrieve(item['img'],self.imgpath + "/" + imgname)
        return item



