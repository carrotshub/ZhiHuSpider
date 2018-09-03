# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class author_reply_Item(scrapy.Item):
    author_id= Field()
    quetion_title=Field()

class author_ask_Item(scrapy.Item):
    """docstring for question_comments_convers"""
    author_id=Field() 
    ques_title=Field()
    
class author_info_Item(scrapy.Item):
    """docstring for an_comments_re"""
    name=Field()
    following_count=Field()
    shared_count=Field()
    pins_count=Field()
    employment=Field()
    favorite_count=Field()
    voteup_count=Field()
    lite_favorite_content_count=Field()
    education=Field()
    headline=Field()
    gender=Field()
    favorited_count=Field()
    follower_count=Field()
    location=Field()
    badge=Field()
    following_topic_count=Field()
    business=Field()
    columns_count=Field()
    following_columns_count=Field()
    answer_count=Field()
    question_count=Field()
    articles_count=Field()
    following_question_count=Field()
    thanked_count=Field()
    hosted_live_count=Field()
    participated_live_count=Field()
    independent_articles_count=Field()
    following_favlists_count=Field()
    identity=Field()
    url_token=Field()