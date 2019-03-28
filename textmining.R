# mysql ##########

drv = dbDriver("MySQL") #database를 연결해주는 bridge

#db와 연결
conn = dbConnect(drv, host='127.0.0.1', port=3307, dbname='corpusdb', user='dooo', password='1234')

#한글설정
# dbGetQuery(conn, "SHOW VARIABLES LIKE 'character_set_%';")
# options(encoding='UTF-8')
# dbSendQuery(conn, 'set character set utf8')   # set utf-8


dbListTables(conn)

# query문 하나만 실행하고 싶을 때
dbSendQuery(conn, 'set character set utf8')


# query문 여러개 실행하고 싶을 때 
rsdf = dbGetQuery(conn, "select * from MS_Song limit 5")
rsdf = changeCode(rsdf)

rsdf
dbGetQuery(conn, "update Song set title='선물1' where songno = '30514366'")

# Transaction
dbBegin(conn);
dbGetQuery(conn, "update Song set title='선물1' where songno = '30514366'");
dbRollback(conn) 
dbCommit(conn)


# close 필수 (#show processlist 확인하기)
dbDisconnect(conn)

#마지막에!! 한 번만 !!
# unload하면 expired돼서 다시 연결 못함 (Ctrl+Shift+F10하기 전까지는)
dbUnloadDriver(drv)
dbGetQuery(conn, "select * from MS_Song limit 5")

stopwords('english') #영어에서 쓰이는 불용
stopwords(c('a','b','c'))
crude = tm_map(crude, removeWords, stopwords("english"))
# stemdocument() : 어근
crude = tm_map(crude, stemDocument, language="english")


crude[[1]]
crude[[1]][1] #내용

# 이 때 n 사라짐
crude = tm_map(crude, stripWhitespace)
crude[[1]][1]

# 아예 다 소문자로 만들어서 하기
crude = tm_map(crude, content_transformer(tolower))
crude[[1]][1]

# 이때 \도 날아감
crude = tm_map(crude, removePunctuation)
crude[[1]][1]

crude = tm_map(crude, removeWords, stopwords("english"))
crude[[1]][1]

crude = tm_map(crude, stripWhitespace)
crude[[1]][1]

install.packages('SnowballC')
crude = tm_map(crude, stemDocument, language="english")
crude[[1]][1]

tdm = TermDocumentMatrix(crude) # 행:term(단어), 열:document(문서)
tdm

rownames(tdm)
tail(as.matrix(tdm))
tdm['year',]

tdm$i
tdm$j
tdm$v
tdm = removeSparseTerms(tdm, 0.8)
tdm
rownames(tdm)
dtm = t(tdm)
inspect(tdm)
inspect(tdm[1:5, 1:10])




# 참고 (특정 단어 제거)
# crude = tm_map(crude, removeWords, c("xxx", "yyy"))

# entry는 보통 한 문장 (단어나 문단도 될 수 있음)
# sparsity 희소성 (90%라고 뜨면 90%가 거의 한 번만 쓰였다는 뜻, 80% 이상이 되면 재사용이 없다고 보면 됨)

# 빈도 분석 #####

#findFreqTerms(tdm, 20) #### : 이상 / 이하
findFreqTerms(tdm, 20)
findFreqTerms(tdm, 20, 30)
findFreqTerms(tdm, 0, 10)

#findAssocs(<Data>, <단어>, <비율>) #### <단어>와 관련 있는 단어
findAssocs(tdm, "last", 0.5)
findAssocs(tdm, "oil", .7)

#rowSums(matrix) 단어별 빈도수 계산 ####
rowSums(as.matrix(tdm))
wFreq = sort(rowSums(as.matrix(tdm)), decreasing=T)
wFreq

names(wFreq) #단어만 (row는 단어(term)이니까)

wFreq > 10 # True/False 반환

#subset() 특정 조건으로 잘라내기 ####
wFreq = subset(wFreq, wFreq > 10)
wFreq

