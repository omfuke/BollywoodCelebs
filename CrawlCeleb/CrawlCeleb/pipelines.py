# -*- coding: utf-8 -*-
import sqlite3
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlcelebPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('celeb1.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS celeb_triats""")
        self.curr.execute("""create table celeb_triats(
                            name TEXT,
                            producer INT,
                            director INT,
                            music INT,
                            DOB DATETIME,
                            credits INT,
                            social TEXT,
                            image TEXT
                            )
                            """)



    def process_item(self, item, spider):
        self.store_db(item)
        return item


    def store_db(self,item):
        self.curr.execute("""INSERT INTO celeb_triats values(?,?,?,?,?,?,?,?)""",(
            item['name'],
            item['producer'],
            item['director'],
            item['music'],
            item['DOB'],
            item['credits'],
            item['social'],
            item['image']

        ))
        self.conn.commit()