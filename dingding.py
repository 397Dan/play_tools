#!usr/bin/python
# coding=utf-8
'''
参考文档 https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.W2TfsP&treeId=257&articleId=105735&docType=1
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import json
import copy
import argparse

class DingDing(object):
    def __init__(self):
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token=be413e328ed892cfcd18c1deab1cd28cf5a4ca58ddb09f332362d2c5b0ca2a87'
        self.head = {'Content-Type': 'application/json'}
        # self.data = {"msgtype": "",
        #              "text": {"content": '测试数据'}
        #              }

    def sendText(self,msgtype,content):
        data = {}
        data["msgtype"] = msgtype
        data[msgtype] = {}
        data[msgtype]["content"] = content
        self.postTest(data)

    def sendLink(self,msgtype,text,title = '',picUrl = '',messageUrl = ''):
        data = {}
        data["msgtype"] = msgtype
        data[msgtype] = {}
        data[msgtype]['text'] = text
        data[msgtype]['title'] = title
        data[msgtype]['picUrl'] = picUrl
        data[msgtype]['messageUrl'] = messageUrl
        self.postTest(data)

    def sendMarkdown(self,msgtype,title,text):
        data = {}
        data["msgtype"] = msgtype
        data[msgtype] = {}
        data[msgtype]["title"] = title
        data[msgtype]["text"] = text
        self.postTest(data)

    def postTest(self,data):
        req = urllib2.Request(self.url, data=json.dumps(data), headers=self.head)
        response = urllib2.urlopen(req, timeout=30)
        content = response.read()
        return content

    # def main(self):
    #     if self.text == '':
    #         return
    #     elif isinstance(self.text, str):
    #         self.postTest()


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("msg", type=str, help="must bes tring")
    # args = parser.parse_args()
    # DingDing().sendText("text",'aaaaaa \n bbbbbbbbbb \n cccccccc')
    c = "## biz有改动\n 修改了：" + "11111" + "\n\n原biz为：" + "22" + "\n\n修改为：" + "33333" + "\n\n原biz_error_count为：" + "4444444"
    DingDing().sendMarkdown("markdown", "biz有改动", c)


