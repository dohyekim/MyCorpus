import Ted_crawl as t
import TedSql as td
import tedfunctions as f

for i in range(1, 10):
    tedcrawl = t.TedCrawl()
    tedcrawl.engcrawl()
    tedcrawl.korcrawl()
    tedcrawl.getDetail()

for i in range(1,10):
    ted = td.Ted()
    ted.sqlEngData()
    ted.sqlKorData()
    ted.sqlDetail()

f.updateTalk()
