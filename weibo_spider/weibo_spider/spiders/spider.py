#!/usr/bin/python
# coding: utf-8

"""
    Author: ztt
    Email: qq282699766@gmail.com
    Date created: 2017/1/12
"""
import re
import time
from scrapy.http import Request
from scrapy import Selector
from scrapy.spiders import CrawlSpider
from weibo_spider.settings import bigV
from weibo_spider.items import TweetsItem, UserItem, CompleteItem, CommentItem


class Spider(CrawlSpider):
    name = "weibo"
    host = "http://weibo.cn"
    start_user_id = bigV
    scrawl_ID = set(start_user_id)  # 记录待爬的用户ID
    finish_ID = set()  # 记录已爬的用户ID

    def start_requests(self):
        while self.scrawl_ID.__len__():
            user_id = self.scrawl_ID.pop()
            self.finish_ID.add(user_id)  # 加入已爬队列
            user_id = str(user_id)

            url_tweets = "http://weibo.cn/%s/profile?filter=0&page=1" % user_id  # filter 0所有 1原创
            url_information0 = "http://weibo.cn/attgroup/opening?uid=%s" % user_id
            yield Request(url=url_information0, meta={"user_id": user_id}, callback=self.parse_user_0)  # 去爬个人信息
            yield Request(url=url_tweets, meta={"user_id": user_id}, callback=self.parse_tweets)  # 去爬微博

    def parse_user_0(self, response):
        """ 抓取个人信息-第一部分：微博数、关注数、粉丝数 """
        user_item = UserItem()
        selector = Selector(response)
        text0 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
        if text0:
            num_tweets = re.findall(u'\u5fae\u535a\[(\d+)\]', text0)  # 微博数
            num_follows = re.findall(u'\u5173\u6ce8\[(\d+)\]', text0)  # 关注数
            num_fans = re.findall(u'\u7c89\u4e1d\[(\d+)\]', text0)  # 粉丝数
            if num_tweets:
                user_item["ctweets"] = int(num_tweets[0])
            if num_follows:
                user_item["cfollows"] = int(num_follows[0])
            if num_fans:
                user_item["cfans"] = int(num_fans[0])
            user_item["_id"] = response.meta["user_id"]
            url_information1 = "http://weibo.cn/%s/info" % response.meta["user_id"]
            yield Request(url=url_information1, meta={"item": user_item}, callback=self.parse_user_1)

    def parse_user_1(self, response):
        """ 抓取个人信息2 """
        user_item = response.meta["item"]
        selector = Selector(response)
        text1 = ";".join(selector.xpath('body/div[@class="c"]/text()').extract())  # 获取标签里的所有text()

        nickname = re.findall(u'\u6635\u79f0[:|\uff1a](.*?);', text1)  # 昵称
        intro = re.findall(u'\u7b80\u4ecb[:|\uff1a](.*?);', text1)  # 简介
        auth = re.findall(u'\u8ba4\u8bc1[:|\uff1a](.*?);', text1)  # 认证信息

        gender = re.findall(u'\u6027\u522b[:|\uff1a](.*?);', text1)  # 性别
        place = re.findall(u'\u5730\u533a[:|\uff1a](.*?);', text1)  # 地区（包括省份和城市）
        birthday = re.findall(u'\u751f\u65e5[:|\uff1a](.*?);', text1)  # 生日
        sexorientation = re.findall(u'\u6027\u53d6\u5411[:|\uff1a](.*?);', text1)  # 性取向
        marriage = re.findall(u'\u611f\u60c5\u72b6\u51b5[:|\uff1a](.*?);', text1)  # 婚姻状况
        url = re.findall(u'\u4e92\u8054\u7f51[:|\uff1a](.*?);', text1)  # 首页链接

        if nickname:
            user_item["nickname"] = nickname[0]
        if auth:
            user_item["auth"] = auth[0]
        if intro:
            user_item["intro"] = intro[0]
        user_item['t'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        yield user_item

    def parse_tweets(self, response):
        """ 抓取微博数据 """
        selector = Selector(response)
        tweets = selector.xpath('body/div[@class="c" and @id]')
        for tweet in tweets:
            tweets_item = TweetsItem()
            tweets_id = tweet.xpath('@id').extract_first()  # 微博ID
            content = tweet.xpath('div/span[@class="ctt"]/text()').extract_first()  # 微博内容
            clike = re.findall(u'\u8d5e\[(\d+)\]', tweet.extract())  # 点赞数
            ctransfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', tweet.extract())  # 转载数
            ccomment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.extract())  # 评论数
            master = re.findall(u'\u539f\u6587\u8f6c\u53d1(.*?)\u539f\u6587\u8bc4\u8bba', tweet.extract())  # 提取转发信息
            reason = re.findall(u'\u8f6c\u53d1\u7406\u7531:</span>(.*?)\u8d5e', tweet.extract())  # 转发理由
            others = tweet.xpath('div/span[@class="ct"]/text()').extract_first()  # 求时间和使用工具（手机或平台）
            comment_raw = re.findall(u'repost(.*?)fav', tweet.extract())  # 提取转发信息
            comment__url = re.findall(u'<a href="(.*?)" class="cc">\u8bc4\u8bba', comment_raw[0])[0]  # 评论准备
            comment_count = re.findall(u'">\u8bc4\u8bba\[(.*?)]</a>', comment_raw[0])[0]

            cooridinates = tweet.xpath('div/a/@href').extract_first()  # 定位坐标

            tweets_item["_id"] = tweets_id
            tweets_item["user_id"] = response.meta["user_id"]
            if clike:
                tweets_item["clike"] = int(clike[0])
            if ctransfer:
                tweets_item["ctransfer"] = int(ctransfer[0])
            if ccomment:
                tweets_item["ccomment"] = int(ccomment[0])
            if master:
                tweets_item["master_id"] = 'M_%s' % master[0].split('comment/')[1].split('?')[0]
                if reason:
                    reason = reason[0].split('//')[0].strip()
                    if reason.endswith('<a href="http:'):
                        reason = reason[:-14].strip()
                    tweets_item["content"] = reason
            else:
                if content:
                    tweets_item["content"] = content.strip(u"[\u4f4d\u7f6e]")  # 去掉最后的"[位置]"
            if others:
                others = others.split(u"\u6765\u81ea")
                tweets_item["pub_time"] = others[0]
            tweets_item['t'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield tweets_item

            if int(comment_count) != 0:
                yield Request(comment__url, meta={"master_id": tweets_id}, callback=self.parse_comment)
                hot_comment_url = 'http://weibo.cn/comment/hot/%s?rl=2' % tweets_id.strip('M_')
                yield Request(hot_comment_url, meta={"master_id": tweets_id}, callback=self.parse_comment)

        url_next = selector.xpath(
            u'body/div[@id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0],
                          meta={"user_id": response.meta["user_id"]},
                          callback=self.parse_tweets)
        else:
            complete_item = CompleteItem()
            complete_item["_id"] = response.meta["user_id"]
            complete_item['t'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield complete_item

    def parse_comment(self, response):
        master_id = response.meta["master_id"]  # master_id
        selector = Selector(response)
        comments = selector.xpath('body/div[@class="c" and @id]')
        for comment in comments:
            comment_id = comment.xpath('@id').extract_first()  # comment_id
            if comment_id == 'M_':
                continue
            water_name = comment.xpath('a/@href').extract_first().strip('/u/')  # auth_water_name
            auth_id = re.findall(u'fuid=(.*?)&type', comment.xpath('a/@href').extract()[1])[0]  # auth_id
            clike = re.findall(u'\u8d5e\[(\d+)\]', comment.extract())  # 点赞数  [u'1']
            content = comment.xpath('span[@class="ctt"]')  # 内容，回复对象
            text = content.xpath('text()').extract()

            if auth_id not in self.finish_ID:  # 新的ID，如果未爬则加入待爬队列
                self.scrawl_ID.add(auth_id)

            comment_item = CommentItem()
            comment_item['_id'] = comment_id
            comment_item['author_id'] = auth_id
            comment_item['water_name'] = water_name
            comment_item['master_id'] = master_id
            if clike:
                comment_item['clike'] = int(clike[0])
            if len(text) == 2:
                comment_item['content'] = text[1].strip(':')
                comment_item['reply_nickname'] = content.xpath('a/text()').extract_first().strip('@')
            else:
                comment_item['content'] = text[0]

            comment_item['t'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield comment_item
        url_next = selector.xpath(
            u'body/div[@id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()

        if url_next:
            yield Request(url=self.host + url_next[0],
                          meta={"master_id": master_id},
                          callback=self.parse_comment)
        else:
            complete_item = CompleteItem()
            complete_item["_id"] = master_id
            complete_item['t'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield complete_item
