# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging
import sys
from UserInfo.items import author_ask_Item,author_info_Item,author_reply_Item

class UserinfoPipeline(object):
    def __init__(self,settings):
        self.username=settings.get('MYSQL_USER')
        self.password=settings.get('MYSQL_PASSWORD')
        self.database=settings.get('zhihu')
        self.host=settings.get('MYSQL_HOST')
        self.port=settings.get('MYSQL_PORT')
        self.c=settings.get('CHARSET')

        self.logger=logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
                settings=crawler.settings
                )
    def open_spider(self,spider):
        try:
            self.conn=pymysql.connect(
                    user=self.username,
                    passwd=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    charset=self.c
                    )
            self.logger.info('Connecting to database successfully!')
            self.cur=self.conn.cursor()
        except self.conn.Error as e:
            sys.exit('Failed to connect database.',e)
    def close_spider(self,close_spider):
        self.cur.close()
        self.conn.close()
        self.logger.info('爬取结束，spider已经关闭')
    def process_item(self, item, spider):
        if isinstance(item,author_info_Item):
            try:
               statement=('insert into zhihu.author_info(name,following_count,shared_count,'\
                    'pins_count,employment,favorite_count,voteup_count,lite_favorite_content_count,education,'\
                    'headline,gender,favorited_count,follower_count,location,badge,following_topic_count,'\
                    'business,columns_count,following_columns_count,answer_count,question_count,articles_count,'\
                    'following_question_count,thanked_count,hosted_live_count,participated_live_count,independent_articles_count,'\
                    'following_favlists_count,identity,url_token)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'\
                    '%s,%s,%s,%s,%s,%s,%s,%s)'
                )
               data=(
                    item['name'],
                    item['following_count'],
                    item['shared_count'],
                    item['pins_count'],
                    item['employment'],
                    item['favorite_count'],
                    item['voteup_count'],
                    item['lite_favorite_content_count'],
                    item['education'],
                    item['headline'],
                    item['gender'],
                    item['favorited_count'],
                    item['follower_count'],
                    item['location'],
                    item['badge'],
                    item['following_topic_count'],
                    item['business'],
                    item['columns_count'],
                    item['following_columns_count'],
                    item['answer_count'],
                    item['question_count'],
                    item['articles_count'],
                    item['following_question_count'],
                    item['thanked_count'],
                    item['hosted_live_count'],
                    item['participated_live_count'],
                    item['independent_articles_count'],
                    item['following_favlists_count'],
                    item['identity'],
                    item['url_token']
                    )
               self.cur.execute(
                       statement,
                       data
                       )
               self.cur.connection.commit()
               self.logger.info('successfully inset into author_info!')
               url_token=item['url_token']
               try:
                   sql='update zhihu.author_seeds set is_crawled=1 where url_token="%s"'%(url_token)
                   self.cur.execute(sql)
                   self.cur.connection.commit()
                   self.logger.info('update a seed successfully!')
               except self.conn.Error as e:
                       self.logger.info('Failed update the seeds table!',e)
            except self.conn.Error as e:
               self.logger.error('Failed insert into author_info.',e)
        elif isinstance(item,author_reply_Item):
            try:
                statement=('insert into zhihu.reply_table(author_id,question_title)values(%s,%s)')
                re_data=(
                        item['author_id'],
                        item['quetion_title'])
                self.cur.execute(
                        statement,
                        re_data)
                self.cur.connection.commit()
                self.logger.info('successfully inset into author_reply!')
            except self.conn.Error as e:
                self.logger.error('Failed insert into author_reply.',e)
        elif isinstance(item,author_ask_Item):
            try:
                statement=('insert into zhihu.ask_table(author_id,ques_title)values(%s,%s)')
                re_data=(
                        item['author_id'],
                        item['ques_title'])
                self.cur.execute(
                        statement,
                        re_data)
                self.cur.connection.commit()
                self.logger.info('successfully inset into author_ask')
            except self.conn.Error as e:
                self.logger.error('Failed insert into author_ask.',e)         
               
        return item
