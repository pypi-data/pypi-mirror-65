# -*- coding: UTF-8 -*-
# 打包 python3 setup.py sdist
# 上传 python3 setup.py sdist upload -r pypi 
import json
import requests
class Robot:
    key = ''
    lanauage = 'zh'
    def __init__(self, key = '',lanauage = 'zh'):
        self.key = key
        self.lanauage = lanauage

    def setLanguage(self, lanauage):
        self.lanauage = lanauage

    def chat(self, receivedMessage):
        if self.lanauage == 'zh':
            sess = requests.get('https://api.ownthink.com/bot?spoken='+receivedMessage + '?')
            answer = sess.text
            answer = json.loads(answer)
            return answer['data']['info']['text']
        else:
            return('英文服务尚未提供,敬请期待')

robot = Robot()