#!/usr/bin/python
# coding: utf-8

"""
    Author: ztt
    Email: qq282699766@gmail.com
    Date created: 2017/1/16
"""
import base64
import os
import requests
import json
import logging
from settings import myWeiBo

logger = logging.getLogger(__name__)


def get_cookie(account, password):
    """ 获取一个账号的Cookie """
    login_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)"
    username = base64.b64encode(account.encode("utf-8")).decode("utf-8")
    post_data = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(login_url, data=post_data)
    json_str = r.content.decode("gbk")
    info = json.loads(json_str)
    if info["retcode"] == "0":
        logger.warning("Get Cookie Success!( Account:%s )" % account)
        cookie = session.cookies.get_dict()
        return json.dumps(cookie)
    else:
        logger.warning("Failed!( Reason:%s )" % info["reason"])
        return ""


def init_cookie(rconn, spider_name):
    """ 获取所有账号的Cookies，存入Redis。如果Redis已有该账号的Cookie，则不再获取。 """
    for weibo in myWeiBo:
        if rconn.get("%s:Cookies:%s--%s" % (spider_name, weibo[0], weibo[1])) is None:
            cookie = get_cookie(weibo[0], weibo[1])
            if len(cookie) > 0:
                rconn.set("%s:Cookies:%s--%s" % (spider_name, weibo[0], weibo[1]), cookie)
    cookie_num = "".join(rconn.keys()).count("%s:Cookies" % spider_name)
    logger.warning("The num of the cookies is %s" % cookie_num)
    if cookie_num == 0:
        logger.warning('Stopping...')
        os.system("pause")


def update_cookie(account_text, rconn, spider_name):
    """ 更新一个账号的Cookie """
    account = account_text.split("--")[0]
    password = account_text.split("--")[1]
    cookie = get_cookie(account, password)
    if len(cookie) > 0:
        logger.warning("The cookie of %s has been updated successfully!" % account)
        rconn.set("%s:Cookies:%s" % (spider_name, account_text), cookie)
    else:
        logger.warning("The cookie of %s updated failed! Remove it!" % account_text)
        remove_cookie(account_text, rconn, spider_name)


def remove_cookie(account_text, rconn, spider_name):
    """ 删除某个账号的Cookie """
    rconn.delete("%s:Cookies:%s" % (spider_name, account_text))
    cookie_num = "".join(rconn.keys()).count("SinaSpider:Cookies")
    logger.warning("The num of the cookies left is %s" % cookie_num)
    if cookie_num == 0:
        logger.warning('Stopping...')
        os.system("pause")
