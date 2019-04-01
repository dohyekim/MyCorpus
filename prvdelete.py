import re
import json
from bs4 import BeautifulSoup
import random
import time
import pymysql
import os
import tedfunctions as f

# if os.path.exists("html/" + str(self.num) + ".htm") == False:
#     nos.append(self.num)
#     return

# print('========================= Detail SQl {} started ============================='.format(self.num))


talk = []
speaker = []
korean = []
english = []
talkspeaker = []

htmls = ''
with open("html/" + str(1) +".htm", 'r', encoding='utf-8') as rfile:
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
    
    talk=[(1, title, event, talk_year, tags)]

    #---------------------------------speaker json------------------------------------
    pattern = re.compile('"speakers":(.*),\"url')
    speakers = re.findall(pattern, script)
    spkJson = json.loads(speakers[0])
    speaker_id = spkJson[0]['id']
    name = spkJson[0]['firstname'] + ' ' + spkJson[0]['lastname']
    field = spkJson[0]['description']
    speaker=[(speaker_id, name, field)]
    talkspeaker=[(1, speaker_id)]

    saveSpeaker()
    saveTalkSpeaker()
    saveTalk()

except Exception as err:
    # global error
    # error.append(self.num)
    print("error >>>>>>>>>>>> ", err)
    print(plyrtalks)
