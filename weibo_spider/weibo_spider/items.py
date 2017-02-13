# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class TweetsItem(Item):
    _id = Field()  # 微博id = user_id+tweets_id
    user_id = Field()  # 作者id
    content = Field()  # 内容
    clike = Field()  # 点赞数
    ccomment = Field()  # 评论数
    ctransfer = Field()  # 转发数
    pub_time = Field()  # 创建时间
    master_id = Field()  # 隶属id 如果是转发微博

    t = Field()


class CommentItem(Item):
    _id = Field()  # 评论ID
    author_id = Field()  # 评论人ID
    water_name = Field()  # 评论人个性域名
    master_id = Field()  # 隶属微博ID
    reply_nickname = Field()  # 若为评论的回复，记录评论的发布者昵称
    content = Field()  # 评论内容
    clike = Field()  # 评论点赞数

    t = Field()


class UserItem(Item):
    _id = Field()  # 用户id
    cfollows = Field()  # 关注数
    cfans = Field()  # 粉丝数
    ctweets = Field()  # 微博数

    nickname = Field()  # 用户昵称
    auth = Field()  # 认证信息
    intro = Field()  # 简介

    t = Field()


class CompleteItem(Item):
    _id = Field()  # 用户ID

    t = Field()
