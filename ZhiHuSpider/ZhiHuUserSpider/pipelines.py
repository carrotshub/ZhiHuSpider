# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging
import sys
from .items import Question_Item,answer_Item, answer_comment_Item,author_seeds_Item
                    
            
        
class ZhihuuserspiderPipeline(object):
    def __init__(self,settings):
        """
        :summary: 类初始化方法,在这里初始化数据库
        """
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
            self.logger.info('Connectig to database successfully!')
            self.cur=self.conn.cursor()
        except self.conn.Error as e:
            sys.exit('Failed to connect database.',e)
        
        #如果数据库不存在则创建，否则则使用
        try:
            self.cur.execute(
                'CREATE DATABASE IF NOT EXISTS  zhihu;'
            )
        except Exception as e:
            raise e
            self.logger.info('The database has existed!')
        else:
            self.cur.execute(
                'USE zhihu;'
            )
    def close_spider(self,close_spider):
        self.cur.close()
        self.conn.close()
        self.logger.info('爬取结束，spider已经关闭')
    def process_item(self, item, spider):
        """
        :summary: 先判断item是否已经实例化,如果是,就把数据存储进mysql中
        :param item:
        :param spider:
        :return:
        """

        if isinstance(item,Question_Item):
            try:
                self.cur.execute(
                    'insert into question_table(q_id,q_title,q_detail,q_create_time,'\
                    'q_attention_num,q_scanner_num,answer_num,best_answer_id,q_comment_num)'\
                    'values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (
                     item['q_id'],
                     item['q_title'],
                     item['q_detail'],
                     item['q_create_time'],
                     item['q_attention_num'],
                     item['q_scanner_num'],
                     item['answer_num'],
                     item['best_answer_id'],
                     item['q_comment_num'])     
                )
                self.cur.connection.commit()
                self.logger.info(
                    'Write a question info item successfully!'
                )
            except self.conn.Error as e:
                self.logger.error('Faild to insert into question.Returned:{0:s}'.format("there is an error!!"))
        elif isinstance(item,answer_Item):
            try:
                statement=(
                    'insert into answer_table(q_id,answer_id,answer_detail,answer_img,'\
                    'create_time,thumb_num,comment_num,author_name,href_num)'\
                    'values(%s,%s,%s,%s,%s,%s,%s,%s,%s)' )
                data=(
                     item['q_id'],
                     item['answer_id'],
                     item['answer_detail'],
                     item['answer_img'],
                     item['create_time'],
                     item['thumb_num'],
                     item['comment_num'],
                     item['author_name'],
                     item['href_num']
                        )
                   
                self.cur.execute(
                    statement,
                    data
                    )
                self.cur.connection.commit()
                self.logger.info('Write a answer successfully!')
            except self.conn.Error as e:
                self.logger.error('Faild to insert into answer.Returned:{0:s}'.format("there is an error!!"))
        elif isinstance(item,answer_comment_Item):
            try:
                statement=(
                        'insert into ans_comment(answer_id,comment_detail,vote_count)values(%s,%s,%s)'
                    )
                ac_data=(
                         item['answer_id'],
                         item['comment_detail'],
                         item['vote_count'])
                self.cur.execute(
                    statement,
                    ac_data
                    )
                self.cur.connection.commit()
                self.logger.info('Write a answer comments successfully!')
            except self.conn.Error as e:
                self.logger.error('Faild to insert into answer_comment_Item.Returned:{0:s}'.format("there is an error!!"))

        elif isinstance(item,author_seeds_Item):
            try:
                sql='insert into author_seeds(url_token,is_crawled)values(%s,%s)'
                seeds_data=(
                        item['url_token'],
                        item['is_crawled'])
                self.cur.execute(
                        sql,
                        seeds_data
                        )
                self.cur.connection.commit()
                self.logger.info('write an author_seeds sucessfully!')
            except self.conn.Error as e:
                self.logger.error('Faild to insert into author_seeds.Returned:{0:s}'.format('there is an error!'))
                
                
#        elif isinstance(item,key_words_table):
#            try:
#                sql='update key_words_table set is_crawled={0:s} where key_word={1:s}'.format(item['is_crawled'],item['key_word'])
#                self.cur.execute(sql)
#                self.cur.connection.commit()
#                self.logger.info('update the is_crawled_table successfully!')
#            except self.conn.Error as e:
#                self.logger.error('Faild to uodate the is_crawled_table!')
        return item




























