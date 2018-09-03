# -*- coding: utf-8 -*-
from ..settings import *
import pymysql
import scrapy
import json
import time
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.selector import Selector
from ..items import Question_Item,answer_Item,answer_comment_Item,author_seeds_Item
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
# 为了创建一个Spider,必须继承scrapy.Spider类
class ZhiHuUserSpider(scrapy.Spider):
    # 爬虫的名字,用于区别Spider,该名字必须是唯一的
    name = 'ZhiHuUserSpider'
    # 只爬取某个域名
    allowed_domain = ['www.zhihu.com']
    # Spider启动时爬取的第一个url 
    start_url = [
       'https://www.zhihu.com/'
    ]
    answer_url='https://www.zhihu.com/api/v4/questions/{ques_id}/answers?include='\
                    'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotatio'\
                    'n_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_e'\
                    'dit,comment_count,can_comment,content,editable_content,voteup_count,reshipment'\
                    '_settings,comment_permission,created_time,updated_time,review_info,relevant_info,'\
                    'question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;'\
                    'data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].'\
                    'topics;dci_info&limit=10&offset={offset}&sort_by=default'
                    
    comm_url='https://www.zhihu.com/api/v4/answers/{answer_id}/comments?include=data'\
                            '[*].author,collapsed,reply_to_author,disliked,content,voting,vote_count,'\
                            'is_parent_author,is_author&order=normal&limit=20&offset={offset}&status='\
                            'open'
    
    url1='https://www.zhihu.com/api/v4/search_v3?t=general&'\
            'q={0:s}&correction=1&offset=0&limit=10'
    au_set=set()
        
    def __init__(self, *args, **kwargs):
        """
        :summary: 类初始化函数, 由于知乎使用了相对url,因此在这里设置一个base_url
        :param args: 
        :param kwargs:  
        """
        super(ZhiHuUserSpider, self).__init__(*args, **kwargs)
        self.base_url = 'https://www.zhihu.com'

#    def make_requests_from_url(self, url):
#        
#        
#        return Request(url, method='GET', headers=ZHIHU_HEADER, cookies=ZHIHU_COOKIE,dont_filter= True)

    def start_requests(self):
        """
        :summary: 设置每一次访问url都给服务器发送带有cookie的请求
        :return:
        """
        self.logger.info('start.........')
#        for i in range(3,200,10):
#            url2=self.url1.format(TOPIC,i)
#            yield self.make_requests_from_url(url2)
        try:
            self.conn=pymysql.connect(
                user=MYSQL_USER,
                passwd=MYSQL_PASSWORD,
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                database=MYSQL_DB,
                charset=CHARSET)
            self.logger.info('Spider connectig to database successfully!')
            self.cur=self.conn.cursor()
        except self.conn.Error as e:
             sys.exit('Spider Failed to connect database.',e)
        
        try:
            self.cur.execute('SELECT key_word FROM zhihu.key_words_table where is_crawled=0 limit 100')
        except Exception as e:
            sys.exit('the key_word is crawled,try to add new',e)
        alldata=self.cur.fetchall()
        for rec in alldata:
            print('the current topic is :',rec[0])
            yield Request(
                    url=self.url1.format(rec[0]),
                    method='GET',
                    headers=ZHIHU_HEADER,
                    cookies=ZHIHU_COOKIE,
                    dont_filter=True,
                    meta={'topic':rec[0]})
#            yield self.make_requests_from_url(self.url1.format(rec))
    def parse(self, response):
        #加载js渲染的URL中json格式的内容
        self.logger.info('responese successfully!code={0:s}'.format(str(response)))
        topic=response.meta['topic']
        json_body=json.loads(response.body_as_unicode())
        for html_json in json_body["data"]:
            if 'object' in html_json:
                obj=html_json['object']
                if 'excerpt' in obj:
                    best_answer_id=obj['id']
                if 'question' in obj:
                    q_id=obj['question']['id']
                    ques_url='https://www.zhihu.com/question/'+ q_id
                    yield scrapy.Request(
                        url=ques_url,
                        method='GET',
                        cookies=ZHIHU_COOKIE,
                        headers=ZHIHU_HEADER,
#                        dont_filter=True,
                        callback=self.question_parse,
                        meta={'best_id':best_answer_id,'q_id':q_id}
                        )

        if 'paging' in json_body.keys() and json_body.get('paging').get('is_end')==False:
            next=json_body.get('paging').get('next')
            search_hash_id=re.findall('search_hash_id=[0-9,a-z,A-Z]+',next)[0]
            offset=re.findall('offset=[0-9]+',next)[0]
            topic_filter=re.findall('topic_filter=[0-9]+',next)[0]
            q=re.findall('q=[0-9,A-Z,a-z,%]+',next)[0]     
#            self.logger.error('the topic {} is crawled {}'.format(q,offset))
            next_url='https://www.zhihu.com/api/v4/search_v3?&correction=1&{0:s}&{1:s}&'\
                'limit=10&t=general&{2:s}&{3:s}'.format(search_hash_id,q,offset,topic_filter)
#            self.logger.error('the topic is %s the offset is %s',(topic,offset))
            yield Request(url=next_url,
                          headers=ZHIHU_HEADER,
                          cookies=ZHIHU_COOKIE,
                          method='GET',
                          callback=self.parse,
                          meta={'topic':topic},
#                          dont_filter=True
                            )
        else:
            try:
                self.cur.execute("update zhihu.key_words_table set is_crawled=1 where key_word='%s'" %(topic))
                self.cur.connection.commit()
                self.logger.info('update an key_words successfully!')
            except self.conn.Error as e:
                self.logger.error('Faild to update  key_words.Returned:{0:s}'.format("there is an error!!"))
#            is_crawled=key_words_table(is_crawled='1',
#                                       key_word=topic)
#            yield is_crawled
        
            
                

    def question_parse(self,response):
        question_item=Question_Item(
            q_id= response.meta['q_id'],
            q_title=None,
            q_detail=None,
            q_create_time=None,
            q_attention_num=None,
            answer_num=None,
            q_scanner_num=None,
            best_answer_id=response.meta['best_id'],
            q_comment_num=None
            )
        
        sel=Selector(response)#用xpath解析网页
        question_item['q_title']=sel.xpath('//div[@class="QuestionHeader-content"]/div/h1/text()').extract_first()
        question_item['q_create_time']=sel.xpath('//*[@id="root"]/div/main/div/meta[6]/@content').extract_first()

        try:
            question_item['q_detail']=sel.xpath('//*[@id="root"]/div/main/div/div[1]\
                /div[1]/div[1]/div[1]/div[2]/div/div/div/span/text()').extract()[0]
        except IndexError:
            print('have no detail!')
            question_item['q_detail']=None
        try:
            question_item['q_attention_num']=re.sub(',','',sel.xpath('//div[@class="NumberBoard-itemInner"]/strong/text()').extract()[0])
        except IndexError:
            question_item['q_attention_num']=0
        try:
            question_item['q_scanner_num']=int(re.sub(',','',sel.xpath('//div[@class="NumberBoard-itemInner"]/strong/text()').extract()[1]))
        except IndexError:
            question_item['q_scanner_num']=0
        question_comment=sel.response.xpath('//*[@id="root"]/div/main/div/\
            div[1]/div[1]/div[2]/div/div/div[2]/div[1]/button/text()').extract()[0]
        pattern='[0-9]+'
        if re.findall(pattern,question_comment):
            num_str=re.sub(',','',question_comment)
            num=re.findall(pattern,num_str)[0]
            question_item['q_comment_num']=int(num)
        else:
            question_item['q_comment_num']=0
        
        try:            
            q_answer_num=sel.xpath('//*[@id="QuestionAnswers-answers"]/div/\
                                   div/div[1]/h4/span/text()').extract()
            qan1=re.sub(',','',q_answer_num[0])
            question_item['answer_num']=int(qan1)
        except IndexError:
            question_item['answer_num']=0
        yield question_item
            
            
        if q_answer_num:
            yield Request(url=self.answer_url.format(ques_id=question_item['q_id'],offset=0),
                          method='GET',
                          cookies=ZHIHU_COOKIE,
                          headers=ZHIHU_HEADER,
                          dont_filter=False,
                          callback=self.answer_parse,
                          meta={'q_id':question_item['q_id']}
                            )

#warning!! yield 会将item提交给pipline处理，一次响应请求在此完成，所以必须注意yield提交的地方。
#如下：会产生数据混乱的情况。if yield
            
        
    def answer_parse(self,response):
        json_body=json.loads(response.body_as_unicode())['data']
        result=json.loads(response.body_as_unicode())
        qes_id=response.meta['q_id']
        answers_item=answer_Item(
            q_id=qes_id,   
            answer_id= None, 
            answer_detail=None, 
            answer_img=None, 
            create_time=None, 
            thumb_num=None, 
            comment_num=None, 
            author_name=None,
            href_num=None
        )
        au_item=author_seeds_Item(
                url_token=None,
                is_crawled=None)

        
        for i in range(len(json_body)):
            json_arry=json_body[i]
            if json_arry['type']=='answer' and ('voteup_count'and'comment_count') in json_arry:
                answers_item['answer_id']=json_arry['id']
                create_time=self.change_time(json_arry['created_time'])
                answers_item['create_time']=create_time
                answers_item['thumb_num']=json_arry['voteup_count'] 
                answers_item['comment_num']=json_arry['comment_count']
                an_content=json_arry['content']
                bs=BeautifulSoup(an_content,"html.parser")
                answers_item['answer_detail']=bs.get_text()
                img_src=bs.findAll("img",{'class':'origin_image zh-lightbox-thumb'})                 
                answers_item['answer_img']=len(img_src)
                href_num=len(bs.findAll('a'))
                answers_item['href_num']=href_num
                
                answer_author=json_arry['author']
                if answer_author['user_type']=='people':
                    answers_item['author_name']=answer_author['name']
                    au_item['url_token']=answer_author['url_token']
                    au_item['is_crawled']=0
                    yield au_item
  
                yield answers_item
                
                
                if answers_item['comment_num'] !=0:
                        yield Request(url=self.comm_url.format(answer_id=answers_item['answer_id'],offset=0),
                                      method='GET',
                                      callback=self.an_comment_parse,
                                      headers=ZHIHU_HEADER,
                                      cookies=ZHIHU_COOKIE,
                                      dont_filter=False,
                                      meta={'answer_id':answers_item['answer_id']}
                                        )            
        if 'paging' in result.keys() and result.get('paging').get('is_end')==False:
            next=result.get('paging').get('next')
            yield Request(
                    url=next,
                    method='GET',
                    dont_filter=False,
                    headers=ZHIHU_HEADER,
                    cookies=ZHIHU_COOKIE,
                    callback=self.answer_parse,
                    meta={'q_id':answers_item['q_id']})
            

    def an_comment_parse(self,response):
        comment_item=answer_comment_Item(
            answer_id=None,
            comment_detail=None,
            vote_count=None
            )
        comment_item['answer_id']=response.meta['answer_id']
        json_body=json.loads(response.body_as_unicode())
        data=json_body['data']

        
        for x in range(0,len(data)):
            content_dic=data[x]     
            if content_dic['type']=='comment':
                content=content_dic['content']
                bs=BeautifulSoup(content,"html.parser")
                
                comment_item['comment_detail']=bs.get_text()
                comment_item['vote_count']=content_dic['vote_count']
            yield comment_item
        if 'paging' in json_body.keys() and json_body.get('paging').get('is_end')==False:
            next=json_body.get('paging').get('next')
            yield Request(
                    url=next,
                    method='GET',
                    headers=ZHIHU_HEADER,
                    cookies=ZHIHU_COOKIE,
                    dont_filter=False,
                    callback=self.an_comment_parse,
                    meta={'answer_id':comment_item['answer_id']}
                    )
        
                                    
    #该函数用来去除HTML中的标签
#    def wipe_html(self,str):
#        dr=re.compile(r'<[^>]+>',re.S)
#        after_str=dr.sub('',str)
#        final_str=after_str.replace('\n','') 
#        return final_str
    def change_time(self,time_str):
        timeArray=time.localtime(time_str)
        otherstyle_time=time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherstyle_time

                     
