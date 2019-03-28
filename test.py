import os
import json
import requests

# with open("html/eng1.json", encoding='utf-8') as data_file:
#    data_loaded = json.load(data_file)
#    a = json.loads(data_loaded)
# print(a)
# print(type(a))
# # jjson = json.load("html/eng24.js", encoding='utf-8')
# # print(type(jjson))

if os.path.exists("html/" + 'ko' + str(6) + ".json"):
   print("html/" + 'ko' + str(6) + ".json")
   with open("html/" + 'ko' + str(6) + ".json", encoding='utf-8') as kjson:
         jjson = json.load(kjson)
         print(type(jjson))
         
         
         # jjson = json.loads(prejson)
         # print(type(jjson))

# url = 'https://www.ted.com/talks/' + str(5) + '/transcript.json?language=' + 'en'
# stat_json = requests.get(url)
# # jjson = stat_json.text
# jjson = stat_json.json()
# print(type(jjson))
