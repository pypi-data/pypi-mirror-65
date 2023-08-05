#-*- coding:utf-8 -*-
import json
import requests

class ding(object):
    def __init__(self,token):
        self.url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % token

    def dingtalkself(self,msgtype=None,post_string=None, at_mobiles=None,isAtAll="false"):
        data = {
            'msgtype': msgtype,msgtype:post_string,
            "at": {"atMobiles": at_mobiles, "isAtAll":isAtAll}
        }
        # if post_string != None:
        #     data.update(post_string)
        print(data)
        print(self.url)
        response = requests.post(self.url,json=data)

    def send_text(self,post_string=None, at_mobiles=None,isAtAll="false"):
        text = {
            "content": str(post_string)
            }
        self.dingtalkself("text",text,at_mobiles,isAtAll)

    def send_markdown(self,post_string=None, at_mobiles=None,isAtAll="false"):
        text ={
             "title":"title",
             "text":post_string
             }
        self.dingtalkself("markdown",text,at_mobiles,isAtAll)

    def send_actionCard(self,title="没有设置标题",post_string=None, at_mobiles=None,isAtAll="false"):
        text ={
             "title":title,
             "text":post_string}
        self.dingtalkself("actionCard",text,at_mobiles,isAtAll)

    def send_feedCard(self,post_string=None, at_mobiles=None,isAtAll="false"):
        text ={"links":post_string}
        self.dingtalkself("feedCard",text,at_mobiles,isAtAll)


if __name__ == '__main__':
    token = ''
    ding = ding(token)
    ding.send_text("cache:sfdsfjaklcache")
    ding.send_markdown("cache:#### 杭州天气 @156xxxx8827\n" +
                 "> 9度，西北风1级，空气良89，相对温度73%\n\n" +
                 "> ![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png)\n"  +
                 "> #####   # 10点20分发布 [天气](http://www.thinkpage.cn/) ")
    actionCard ='''cache
    "![screenshot](@lADOpwk3K80C0M0FoA) 
 ### 乔布斯 20 年前想打造的苹果咖啡厅 
 Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划", 
        "hideAvatar": "0", 
        "btnOrientation": "0", 
        "singleTitle" : "阅读全文",
        "singleURL" : "https://www.dingtalk.com/"
    '''
    ding.send_actionCard("cache",actionCard)

    feedCard = [
            {
                "title": "测试报告",
                "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                "picURL": "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3514361501,3291815511&fm=26&gp=0.jpg",
                "text": "chache测试报告",

            },
            {
                "title": "测试计划",
                "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                "picURL": "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3514361501,3291815511&fm=26&gp=0.jpg"
            },
            {
                "title": "适配测试计划",
                "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                "picURL": "https://www.dingtalk.com/"
            },
            {
                "title": "monkey测试计划",
                "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                "picURL": "https://www.dingtalk.com/"
            },
            {
                "title": "测试总结与回顾",
                "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                "picURL": "https://www.dingtalk.com/"
            }
        ]
    ding.send_feedCard(feedCard)


