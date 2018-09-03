# -*- coding: utf-8 -*-
import scrapy
from UserInfo.settings import *
from UserInfo.items import author_ask_Item,author_info_Item,author_reply_Item
from UserInfo.settings import *
from scrapy.http import Request
from scrapy.selector import Selector
import pymysql
import io
import re
import sys
import json

sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


class UserinfoSpider(scrapy.Spider):
    name = 'UserInfo'
    allowed_domains = ['zhihu.com']
#    start_urls = ['https://www.zhihu.com/people/zlotus/activities']
    start_url='https://api.zhihu.com/people/{0:s}'
    answer_url='https://www.zhihu.com/api/v4/members/{0:s}/answers?include='\
    'data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%'\
    '2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Cs'\
    'uggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Cvoteup_count%2Creshipmen'\
    't_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crev'\
    'iew_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cvoting%2Cis_author%2C'\
    'is_thanked%2Cis_nothelp%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.to'\
    'pics&{1:s}&limit=20&sort_by=created'
    ask_url='https://www.zhihu.com/api/v4/members/{0:s}/questions?include=data%5B*%'\
    '5D.created%2Canswer_count%2Cfollower_count%2Cauthor%2Cadmin_closed_comment&{1:s}&limit=20'
    
    def __init__(self,*args,**kwargs):
        super(UserinfoSpider,self).__init__(*args,**kwargs)
        self.base_url='https://www.zhihu.com'
        
         
    def start_requests(self):
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
            self.cur.execute('SELECT url_token FROM zhihu.author_seeds where is_crawled=0 and url_token !="" limit 5')
        except Exception as e:
            sys.exit('the seeds is error,check and try again',e)
        all_seeds=self.cur.fetchall()
        for rec in all_seeds:
            print('the rec is ',rec[0])
            yield Request(
                    url=self.start_url.format(rec[0]),
                    headers=ZHIHU_HEADER_API,
                    cookies=ZHIHU_COOKIE,
                    dont_filter=True,
                    method='GET')
        

    def parse(self, response):
        author_info_item=author_info_Item(
        name=None,
        following_count=None,
        shared_count=None,
        pins_count=None,
        employment=None,
        favorite_count=None,
        voteup_count=None,
        lite_favorite_content_count=None,
        education=None,
        headline=None,
        gender=None,
        favorited_count=None,
        follower_count=None,
        location=None,
        badge=None,
        following_topic_count=None,
        business=None,
        columns_count=None,
        following_columns_count=None,
        answer_count=None,
        question_count=None,
        articles_count=None,
        following_question_count=None,
        thanked_count=None,
        hosted_live_count=None,
        participated_live_count=None,
        independent_articles_count=None,
        following_favlists_count=None,
        identity=None,
        url_token=None
            )
        json_body=json.loads(response.body_as_unicode())
        for per in json_body:
            if per in author_info_item:
                if per=="employment" and json_body["employment"]:
                    emp=''
                    for em in json_body['employment']:
                        for emer in em:
                            try:
                                if emer['name']!="未填":
                                    emp+=emer['name']+','
                            except KeyError as e:
                                self.logger.info('have no the attribute name',e)
                    author_info_item['employment']=emp
                elif per=="education" and json_body["education"]:
                    ed=[]
                    for edu in json_body['education']:
                        ed.append(edu['name'])
                    fed=','.join(ed)
#                    fed=json.dumps(ed,ensure_ascii=False)
                    author_info_item['education']=fed
                elif per=="location" and json_body["location"]:
                    lo=[]
                    for loc in json_body['location']:
                        lo.append(loc['name'])
                    loca=','.join(lo)
#                    loca=json.dumps(lo,ensure_ascii=False)
                    author_info_item['location']=loca
                elif per=="badge" and json_body["badge"]:
                    ba=[]
                    for ban in json_body['badge']:
                        if 'type' in ban and ban['type']=="identity":
                            author_info_item['identity']=ban['description']
                        elif 'topics' in ban and ban['type']=='best_answerer':
                            for top in ban['topics']:
                                ba.append(top['name'])
                            badge=','.join(ba)
#                            badge=json.dumps(ba,ensure_ascii=False)
                            author_info_item['badge']=badge
                            
                elif per=="business" and json_body["business"]:
                    author_info_item['business']=json_body["business"]['name']
                else:                  
                    author_info_item[per]=json_body[per]
                    author_info_item['badge']=None
                    author_info_item['url_token']=json_body['url_token']
        yield author_info_item
#        try:
#            self.cur.execute("update zhihu.author_seeds set is_crawled=1 where key_word='%s'"% url_token)
#            self.cur.connection.commit()
#            self.logger.info('update a seed successfully!')
#        except self.conn.Error as e:
#            self.logger.info('Failed update the seeds table!')

        if author_info_item['answer_count'] >0:
            yield Request(
                    url=self.answer_url.format(author_info_item['url_token'],'offset=0'),
                    headers=ZHIHU_HEADER,
                    cookies=ZHIHU_COOKIE,
                    method='GET',
#                    dont_filter=True,
                    callback=self.answer_parse)
            
        if author_info_item['question_count']>0:
            yield Request(
                    url=self.ask_url.format(author_info_item['url_token'],'offset=0'),
                    headers=ZHIHU_HEADER,
                    cookies=ZHIHU_COOKIE,
                    method='GET',
#                    dont_filter=True,
                    callback=self.ask_parse)
        
        
    def answer_parse(self,response):
        au_re=author_reply_Item(
                author_id=None,
                quetion_title=None
                )
        json_body=json.loads(response.body_as_unicode())
        data=json_body['data']
        for que in data:
            au_re['quetion_title']=que['question']['title']
            au_re['author_id']=que['author']['name']
            url_token=que['author']['url_token']
            yield au_re
        
        if 'paging' in json_body and json_body['paging']['is_end']==False:
            next_url=json_body['paging']['next']
            pattern='offset=[0-9]+'
            offset=re.findall(pattern,next_url)[0]
            A_url=self.answer_url.format(url_token,offset)
            yield Request(
                    url=A_url,
                    method="GET",
#                    dont_filter=True,
                    headers=ZHIHU_HEADER,
                    cookies=ZHIHU_COOKIE,
                    callback=self.answer_parse)

            
    def ask_parse(self,response):
        au_ask=author_ask_Item(
            author_id=None, 
            ques_title=None)
        json_body=json.loads(response.body_as_unicode())
        data=json_body['data']
        for que in data:
            au_ask['author_id']=que['author']['name']
            au_ask['ques_title']=que['title']
            url_token=que['author']['url_token']
            yield au_ask
        if 'paging' in json_body.keys() and json_body.get('paging').get('is_end')==False:
            next_url=json_body['paging']['next']
            pattern='offset=[0-9]+'
            offset=re.findall(pattern,next_url)[0]
            ask_url=self.ask_url.format(url_token,offset)
            yield Request(
                    url=ask_url,
                    method='GET',
#                    dont_filter=True,
                    cookies=ZHIHU_COOKIE,
                    headers=ZHIHU_HEADER,
                    callback=self.ask_parse)