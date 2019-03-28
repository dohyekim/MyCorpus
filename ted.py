from bs4 import BeautifulSoup
import requests
import re
import json
import random
# from pprint import pprint
import time
import pymysql
import os

def get_conn():
    return pymysql.connect(
        host='127.0.0.1',
        user='dooo',
        password='1234',
        port=3307,
        db='corpusdb',
        charset='utf8')

def getLastId(sql):
    conn = get_conn()
    cur = conn.cursor()    
    cur.execute(sql)
    lastid = cur.fetchall()
    cur.close()
    return lastid        
sqllastid = 'select talk_id from Korean order by talk_id desc limit 1'

sqlTalk = '''insert into Talk(talk_id, title, event, talk_year, tags) 
                        values( %s,%s,%s,%s,%s)'''
sqlSpeaker = "insert into Speaker(speaker_id, name, field) values(%s, %s, %s)"
sqlEnglish = "insert into English(talk_id, engcue, eng) values(%s,%s,%s)"
sqlKorean = "insert into Korean(talk_id, korcue, kor) values(%s,%s,%s)"
sqlTalkSpeaker = "insert into TalkSpeaker (talk_id, speaker_id) values (%s, %s)"


error = []
nfound = []
# print("nfound defined")
# 값 비우기(쿼리문, num = lastid + 1)
# lastid 가져오기

# print(lastid)
# print("num >> ", num)
# exit()
class Ted:

    num = 0

    talk = []
    speaker = []
    korean = []
    english = []
    talkspeaker = []
    isEng = True
    isNF = True
    nfound = []

    def __init__(self):

        lastid = getLastId(sqllastid)
        if len(lastid) == 0:
            self.num = 1
        else:
            self.num = lastid[0][0] + 1
        global nfound
        if len(nfound) != 0:
            self.num = nfound[0] + 1
        nfound = []
        # print(self.num)
        # return

    def ifexist(self,lang):
        if os.path.exists("html/" + lang + str(self.num) + ".json") == True:
            print("html/" + lang + str(self.num) + ".json")
            with open("html/" + lang + str(self.num) + ".json", encoding='utf-8') as kjson:
                jjson = json.load(kjson)
                # jjson = json.loads(prejson)
                print(" ################### Used existing data ##############") 
            # if jjson['status'] and jjson['status'] == 404:
            #     nfound.append(self.num)
            #     return
        else:
            print("html/" + lang + str(self.num) + ".json")
            url = 'https://www.ted.com/talks/' + str(self.num) + '/transcript.json?language=' + lang
            stat_json = requests.get(url)
            if stat_json.status_code == 404:
                print("----------------------------PAGE DO NOT EXIST----------------------------")
                nfound.append(self.num)
                print(nfound)
                self.isNF = False
                print("{} translation does not exist".format(lang), stat_json.status_code)
                jjson = False
                return self.isNF
            else:
                print(stat_json.status_code)
                # 저장하기
                jjson = stat_json.json()
                print("Requests succeess")
                with open("html/" + lang + str(self.num) + ".json", 'w') as engjson:
                    json.dump(jjson, engjson)
        return jjson

    def getEngData(self, lang='en'):
        print('============================={} started ============================='.format(self.num))
        # if len(nfound) != 0:
        #     return
        # jjson = {}
        if self.isNF == False:
            return
        jjson = self.ifexist('en')
        print(type(jjson)) 
        if jjson == False:
            return
        else:
            jsonData = jjson
        # print(self.num)
        # return
        eng = []
        cue = 1

        t = ''
        #paragraphs
        pgs = jsonData['paragraphs']
        for cues in pgs:
            texts = cues['cues']
            for text in texts:
                t = text['text']

                if '\n' in t:
                    t = t.replace('\n',' ')
                eng.append((self.num, cue, t))
                cue += 1
        self.english = eng
        
        self.saveEnglish()

    def getDetail(self):
        if self.isEng == False:
            return
        elif self.isNF == False:
            # self.isNF == True
            return
        html = ''
        # print('============================={} started ============================='.format(self.num))
        # exit()
        if os.path.exists("html/" + str(self.num) + ".htm"):
            with open("html/" + str(self.num) +".htm", 'r', encoding='utf-8') as rfile:
                for i in rfile:
                    html += i
                # print(rfile)
                # html = rfile
                # print(html)
                print(" ################### Used existing data ##############") 

        else:
            url = 'https://www.ted.com/talks/' + str(self.num)
            req = requests.get(url)
            html = req.text
            if req.status_code == 404:
                print("----------------------------PAGE DO NOT EXIST----------------------------")
                nfound.append(self.num)
                time.sleep(1)
                print(nfound)
                return
            else:
                nfound.clear()
                with open("html/{}.htm".format(self.num), 'w', encoding='utf-8') as file:
                    file.write(html)

        soup = BeautifulSoup(html, 'html.parser')
        # with open("lecturer.htm", "r", encoding='utf8') as file:
        #     soup = BeautifulSoup(file, 'html.parser')
        script = str(soup.find_all('script'))
        # print(script)


        #---------------------------------title json------------------------------------
        pattern = re.compile('"player_talks":(.*),\"ratings')
        plyrtalks = re.findall(pattern, script)
        try:
            jsonTitle = json.loads(plyrtalks[0])
            jsonData = jsonTitle[0]
            title = jsonData['title']
            #---------------------------------detailinfo json------------------------------------
            targeting = jsonData['targeting']
            #talk_id == num
            # talk_id = targeting['id']
            tags = targeting['tag']
            talk_year = targeting['year']
            event = targeting['event'] 
            
            self.talk=[(self.num, title, event, talk_year, tags)]

            #---------------------------------speaker json------------------------------------
            pattern = re.compile('"speakers":(.*),\"url')
            speakers = re.findall(pattern, script)
            spkJson = json.loads(speakers[0])
            speaker_id = spkJson[0]['id']
            name = spkJson[0]['firstname'] + ' ' + spkJson[0]['lastname']
            field = spkJson[0]['description']
            self.speaker=[(speaker_id, name, field)]
            self.talkspeaker=[(self.num, speaker_id)]

            self.saveSpeaker()
            self.saveTalkSpeaker()
            self.saveTalk()

        except Exception as err:
            error.append(self.num)
            print("error >>>>>>>>>>>> ", err, "Status code >> ", req.status_code)
            print(plyrtalks)
    
    def getKorData(self, lang='ko'):
        # if len(nfound) != 0:
        #     return
        kor = []
        kcue = 1
        # kjjson = {}
        if self.isNF == False:
            return

        if self.isEng == True:
            kjjson = self.ifexist('ko')
            if kjjson == False:
                return
        else:
            print("---------DO NOT NEED TO GET KOREAN TRANSLATION----------------")
            try: 
                sqlifkor = "update Talk set isKorean = 0 where talk_id = " + str(self.num)
                conn = get_conn()
                cur = conn.cursor()
                cur.execute(sqlifkor)
                conn.commit()

            except Exception as err:
                conn.rollback()
                print("Error!!", err)

            finally:
                try:
                    cur.close()
                except:
                    print("Error on close cursor")
                try:
                    conn.close()
                    print ("OOKKKK")
                except Exception as err2:
                    print("Fail to connect!!", err2)
            return
            # if kstat_json.status_code != 200:
            #     nfound.append(self.num)
            #     print("{} translation does not exist".format(lang))
            #     return
            # else:
            #     print("Requests succeess")
        kjsonData = kjjson
        print(type(kjsonData)) 
        # print(type(kjsonData))

        t = ''
        pgs = kjsonData['paragraphs']
        for cues in pgs:
            texts = cues['cues']
            for text in texts:
                t = text['text']

                if '\n' in t:
                    t = t.replace('\n',' ')
                kor.append((self.num, kcue, t))
                kcue += 1
        self.korean = kor
        self.saveKorean()

    def save(self,sql, data):
        try:
            conn = get_conn()
            conn.autocommit = False
            cur = conn.cursor()
            
            cur.executemany(sql, data)
            if sql == sqlEnglish:
                print("Affected RowCount is {}/{}".format(cur.rowcount,len(self.english)) )
            elif sql == sqlKorean:
                print("Affected RowCount is {}/{}".format(cur.rowcount,len(self.korean)) )
            else:
                print("Affected RowCount is ", cur.rowcount)
            conn.commit()

            # sql = "select text1 from AAA"
            # cur.execute(sql)
            # aaa = cur.fetchall()
            # print(aaa[0][0].replace('\\',''))

        except Exception as err:
            conn.rollback()
            print("Error!!", err)

        finally:
            try:
                cur.close()
            except:
                print("Error on close cursor")
            try:
                conn.close()
                print ("OOKKKK")
            except Exception as err2:
                print("Fail to connect!!", err2)

    def saveTalk(self):
        self.save(sqlTalk, self.talk)
        print('@@@@@@@@@@@@@@@@@@@@@@@@ Talk Done @@@@@@@@@@@@@@@@@@@@@@@@')

    def saveSpeaker(self):
        self.save(sqlSpeaker, self.speaker)
        print('@@@@@@@@@@@@@@@@@@@@@@@@ Speaker Done @@@@@@@@@@@@@@@@@@@@@@@@')

    def saveEnglish(self):
        self.save(sqlEnglish, self.english)
        print('@@@@@@@@@@@@@@@@@@@@@@@@ English Done @@@@@@@@@@@@@@@@@@@@@@@@')

    def saveKorean(self):
        self.save(sqlKorean, self.korean)
        print('@@@@@@@@@@@@@@@@@@@@@@@@ Korean Done @@@@@@@@@@@@@@@@@@@@@@@@')

    def saveTalkSpeaker(self):
        self.save(sqlTalkSpeaker, self.talkspeaker)
        print('@@@@@@@@@@@@@@@@@@@@@@@@ TalkSpeaker Done @@@@@@@@@@@@@@@@@@@@@@@@')


for i in range(1,11):
    ted = Ted()
    ted.getEngData()
    time.sleep(random.randrange(5, 10))
    ted.getKorData()
    time.sleep(random.randrange(5, 10))
    ted.getDetail()
    time.sleep(random.randrange(5, 10))



print(error)
print(nfound)