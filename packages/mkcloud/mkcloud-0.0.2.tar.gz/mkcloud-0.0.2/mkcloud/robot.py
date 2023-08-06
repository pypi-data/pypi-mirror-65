# -*- coding: UTF-8 -*-
import json
import requests
class robot:
    key=''
    lanauage='zh'
    def __init__(self,key,lanauage):
        print(self.lanauage)

    def setLanguage(self,lanauage):
        self.lanauage = lanauage

    def chat(self,receivedMessage):
        if self.lanauage == 'zh':
            print('调用成功AAAA')
            sess = requests.get('https://api.ownthink.com/bot?spoken='+receivedMessage + '?')
            answer = sess.text
            answer = json.loads(answer)
            return answer['data']['info']['text']
        else:
            return('is en')
            