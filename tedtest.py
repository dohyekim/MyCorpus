from bs4 import BeautifulSoup
import requests
import re
import json
# from pprint import pprint
import time
# import pymysql
   
resultpg = {}
pgnum = 1
# num=1
# lang="en"
# texts = []
url = 'https://www.ted.com/talks/' + str(num) + '/transcript.json?language=' + lang
# params = {
#     'language' : lang
# }
stat_json = requests.get(url)
jjson = stat_json.text
if stat_json.status_code != 200:
    print("{} translation does not exist".format(lang))
    pass
else:
    print("Requests succeess")
jsonData = json.loads(jjson, encoding="utf-8") 

t = ''
#paragraphs
pgs = jsonData['paragraphs']
# skips = ['(Laughter)', '(laughter)', '(Applause)', '(applause)']
# koskips = ['(박수)', '(웃음)', '(폭소)']
for cues in pgs:
    texts = cues['cues']
    for text in texts:
        t = text['text']

        # if lang == 'en' and t in skips:
        #     continue
        # elif lang == 'ko' and t in koskips:
        #     continue
        # else: 
        if '\n' in t:
            t = t.replace('\n',' ')
        resultpg[pgnum] = t
        pgnum += 1
#     # for cue in cues:
#     text = cues['text']
#         # if text[-1] == ' ' :
#         #         t = t + text
#         #         t = t.replace('\n', ' ')
#         # else :
#         #     t = t + text + ' ' 
#         #     t = t.replace('\n', ' ')
# resultpg[pgnum] = text
#     # resultpg[pgnum] = t
# pgnum += 1

#     # t = ''
    
print(resultpg)

a = [(1,2,3)]
print(type(a))
print(type(a[0]))

q = 'q'
w = 'w'
e = 'e'
b = []
b.append((q,w,e))
print(b)
print(type(b))
print(type(b[0]))