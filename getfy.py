#-*- coding: UTF-8 -*
import requests, re, json, time
from sendmail import Mail

targetCityName = "杭州"   # 你所关注的城市  该城市的数据发生变动将会触发邮件提醒

class FY:
    def __init__(self):
        self.url = 'https://3g.dxy.cn/newh5/view/pneumonia'
        self.chinaConfirmCount = 0
        self.chinaDeadCount = 0
        self.chinaCuredCount = 0
        self.jsonData = {}
        self.result = ""
        self.targetCityName = targetCityName
        self.targetCityData = {}
        self.sendMailBj = False

    def parse(self, result):
        # print(result)
        self.jsonData = json.loads(result)
        print(self.jsonData)
        for item in self.jsonData:
            self.chinaConfirmCount += item['confirmedCount']
            self.chinaDeadCount = item['deadCount']
            self.chinaCuredCount = item['curedCount']
            if self.targetCityName != None and self.targetCityName in str(item['cities']):
                for city in item['cities']:
                    if city['cityName'] == self.targetCityName:
                        if self.targetCityData != city and self.targetCityData != {}:
                            self.sendMailBj = True
                        self.targetCityData = city
                        

    def getfy(self):
        self.chinaConfirmCount = 0    # 初始化数据
        self.chinaDeadCount = 0
        self.chinaCuredCount = 0
        res = requests.get(self.url)
        res.encoding = 'utf-8'
        rawresult = re.search('<script id="getAreaStat">(.*)</script>', res.text)
        rawlists = re.search(r'\[.*\]', rawresult.group()).group().split('catch')
        # for i in rawlists:
        #     print(i)
        result = rawlists[0]
        result = result[0:-1]   # 去掉最后一位 多余的反大括号
        self.parse(result)

    def printResult(self):
        self.result = time.asctime( time.localtime(time.time()) ) + '\n\n'
        self.result += "{:14}\t 确诊: {}\t 死亡: {}\t 治愈: {} \n\n\n".format(self.targetCityData.get('cityName'), self.targetCityData.get('confirmedCount'), self.targetCityData.get('deadCount'), self.targetCityData.get('curedCount'))
        for item in self.jsonData:
            self.result += "{:14}\t 确诊: {}\t 死亡: {}\t 治愈: {} \n".format(item.get('provinceName'), item.get('confirmedCount'), item.get('deadCount'), item.get('curedCount'))
        print(self.result)
    
    def sendMail(self):
        self.sendMailBj = False
        print("检测到关注城市肺炎人数变动  开始发送邮件")

        receivers = ['*******']    # 收件人列表
        subject = '新型肺炎感染人数增加通知'  # 发送的主题
        content = self.result  # 发送的内容
        sender = "*******"     # 发件人邮箱
        sender_name = "****"       # 发件人姓名
        receivers_name = ['******']   # 收件人姓名

        mail = Mail(sender, receivers)
        mail.send(subject, content, sender_name, receivers_name)


if  __name__ == '__main__':
    distance = FY()
    while True:
        distance.getfy()
        distance.printResult()
        if distance.sendMailBj == True:
            distance.sendMail()   # 若想关闭邮件提醒 将此行删去即可
        time.sleep(10)

