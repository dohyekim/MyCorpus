import re
import json
from bs4 import BeautifulSoup
import random
import time
import pymysql
import os
import tedfunctions as f

sqllastid = 'select talk_id from Korean order by talk_id desc limit 1'
sqlTalk = '''insert into Talk(talk_id, title, event, talk_year, tags) 
                        values( %s,%s,%s,%s,%s)'''
sqlSpeaker = "insert into Speaker(speaker_id, name, field) values(%s, %s, %s)"
sqlEnglish = "insert into English(talk_id, engcue, eng) values(%s,%s,%s)"
sqlKorean = "insert into Korean(talk_id, korcue, kor) values(%s,%s,%s)"
sqlTalkSpeaker = "insert into TalkSpeaker (talk_id, speaker_id) values (%s, %s)"


nos = []
class Ted():

    talk = []
    speaker = []
    korean = []
    english = []
    talkspeaker = []
    num = 0

    def __init__(self):
        self.num = f.getLastId(sqllastid)[0][0] + 1
        global nos
        if len(nos) != 0:
            self.num = nos[0] + 1
            nos = []

    def save(self,sql, data):
        try:
            conn = f.get_conn()
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


    def sqlEngData(self, lang='en'):
        if os.path.exists("html/" + lang + str(self.num) + ".json") == False:
            return

        print('======================= English SQL {} started ============================='.format(self.num))
        with open("html/" + lang + str(self.num) + ".json", encoding='utf-8') as kjson:
            jsonData = json.load(kjson)
        eng = []
        cue = 1

        t = ''
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

    def sqlKorData(self, lang='ko'):
        if os.path.exists("html/" + lang + str(self.num) + ".json") == False:
            return

        # self.num = self.getlastId(sqllastid)
        print('========================= Korean SQl {} started ============================='.format(self.num))
        with open("html/" + lang + str(self.num) + ".json", encoding='utf-8') as kjson:
            jsonData = json.load(kjson)
        kor = []
        kcue = 1

        t = ''
        #paragraphs
        pgs = jsonData['paragraphs']
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

    def sqlDetail(self):
        if os.path.exists("html/" + str(self.num) + ".htm") == False:
            nos.append(self.num)
            return

        print('========================= Detail SQl {} started ============================='.format(self.num))

        htmls = ''
        with open("html/" + str(self.num) +".htm", 'r', encoding='utf-8') as rfile:
            for i in rfile:
                htmls += i

        soup = BeautifulSoup(htmls, 'html.parser')
        script = str(soup.find_all('script'))


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
            # global error
            # error.append(self.num)
            print("error >>>>>>>>>>>> ", err)
            print(plyrtalks)
