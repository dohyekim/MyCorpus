from bs4 import BeautifulSoup
import requests
import random
import time
import json
import os

# with open("chart", "w", encoding="utf-8") as chartfile:
#     chartfile.write("D1 ,K1 ,E1  ,\n")

# with open("chart", "a", encoding="utf-8") as addfile:
#     addfile.write("D{},K{},E{}, \n".format(i,i,i))

sqllastid = 'select talk_id from Korean order by talk_id desc limit 1'
sqlTalk = '''insert into Talk(talk_id, title, event, talk_year, tags) 
                        values( %s,%s,%s,%s,%s)'''
sqlSpeaker = "insert into Speaker(speaker_id, name, field) values(%s, %s, %s)"
sqlEnglish = "insert into English(talk_id, engcue, eng) values(%s,%s,%s)"
sqlKorean = "insert into Korean(talk_id, korcue, kor) values(%s,%s,%s)"
sqlTalkSpeaker = "insert into TalkSpeaker (talk_id, speaker_id) values (%s, %s)"


nfound = []
ifkorean = []
error = []

class TedCrawl():
    
    
    num = 0
    isEng = True
    isNF = True
    talk = []
    speaker = []
    korean = []
    english = []
    talkspeaker = []

    def __init__(self):
        a = []
        with open("chart","r",encoding="utf-8") as readfile:
            for line in readfile:
                a.append(line[1])
            number = len(a)
        self.num = number


    def engcrawl(self, lang='en'):
        self.num += 1
        print("============================{} started ====================================".format(self.num))

        if os.path.exists("html/" + lang + str(self.num) + ".json") == True:
            print(" {} English json already exists".format(self.num))
            return
        else:
            time.sleep(random.randrange(5,10))
            url = 'https://www.ted.com/talks/' + str(self.num) + '/transcript.json?language=' + lang
            stat_json = requests.get(url)
            if stat_json.status_code == 404:
                print("----------------------------English PAGE DO NOT EXIST----------------------------")
                self.isEng = False
                print("{} translation does not exist".format(lang), stat_json.status_code)
                return

            else:
                print(stat_json.status_code)
                # 저장하기
                jjson = stat_json.json()
                print("{} Requests succeess".format(lang))
                with open("html/" + lang + str(self.num) + ".json", 'w') as engjson:
                    json.dump(jjson, engjson)


    def korcrawl(self, lang='ko'):

        if os.path.exists("html/" + lang + str(self.num) + ".json") == True:
            print(" {} Korean json already exists".format(self.num))
            return
        else:
            time.sleep(random.randrange(5,10))
            url = 'https://www.ted.com/talks/' + str(self.num) + '/transcript.json?language=' + lang
            if self.isEng == False:
                print(" No need to get Korean Translation ")
                return
            else:
                stat_json = requests.get(url)
                if stat_json.status_code == 404:
                    print("----------------------------Korean PAGE DO NOT EXIST----------------------------")

                    print("{} translation does not exist".format(lang), stat_json.status_code)
                    return

                else:
                    print(stat_json.status_code)
                    # 저장하기
                    jjson = stat_json.json()
                    print("{} Requests succeess".format(lang))
                    with open("html/" + lang + str(self.num) + ".json", 'w') as engjson:
                        json.dump(jjson, engjson)


    
    def getDetail(self):
        if self.isEng == False:
            with open("chart", "a", encoding="utf-8") as addfile:
                addfile.write("D{}\n".format(self.num))
            return

        if os.path.exists("html/" + str(self.num) + ".htm"):
            print(" Detail page already exists")
            with open("chart", "a", encoding="utf-8") as addfile:
                addfile.write("D{}\n".format(self.num))
            return

        else:
            time.sleep(random.randrange(5,10))
            url = 'https://www.ted.com/talks/' + str(self.num)
            req = requests.get(url)
            print(req.status_code)
            html = req.text

            print("{} Detail requests success ".format(self.num))

            with open("html/{}.htm".format(self.num), 'w', encoding='utf-8') as file:
                file.write(html)
            with open("chart", "a", encoding="utf-8") as addfile:
                addfile.write("D{}\n".format(self.num))



