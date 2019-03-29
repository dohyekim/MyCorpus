# 이후 Elastic Search로 Refac

import tedfunctions as f

class ElasticSearch():

    talkcnt = 0    
    findEngCue = []
    findEng = []
    findKor = []
    engtalk = []
    def __init__ (self):

        # 전체 Talk의 수 구하기
        sqltalkcnt = ''' select (@rownum := @rownum + 1) r
                        from Talk t, (select @rownum := 0) rn
                        order by r desc
                        limit 1; '''
        
        talkconn = f.get_conn()
        talkcur = talkconn.cursor()
        talkcur.execute(sqltalkcnt)
        self.talkcnt = talkcur.fetchall()[0][0]

    def get(self, search):
        # 전체 row 수만큼 loop 돌리도록 수정
        for t in range(1, 20):
            sqlseleng = "select engcue from English where talk_id = {} order by engcue desc limit 1".format(t)
            sqlselkor = "select korcue from Korean where talk_id = {} order by korcue desc limit 1".format(t)

            sqlSearch = '''select talk_id, engcue, eng from English 
                        where eng like '%{}%'
                        and talk_id = {}'''.format(search, t)
        
            conn = f.get_conn()
            cur = conn.cursor()
            cur.execute(sqlseleng)
            engcnt = cur.fetchall()
            if len(engcnt) != 0:
                engs = engcnt[0][0]
            cur.execute(sqlselkor)
            korcnt = cur.fetchall()
            if len(korcnt) != 0:
                kors = korcnt[0][0]
            # print(abs(engcnt - korcnt))
            if abs(engs - kors) > 3:
                print(" Hard to match those two ")
                continue

            else:
                cur.execute(sqlSearch)
                rows = cur.fetchall()
                if len(rows) == 0:
                    continue
                else:
                    print("rows >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ", rows)
                    for i in range(len(rows)):
                        # (talk_id, cue, english)
                        talkcue = (rows[i][0], rows[i][1], rows[i][2])
                        self.engtalk.append(talkcue)
                    print(self.engtalk)
                print("--------------- NEXT TURN -----------------")

    def korequiv(self):
        for k in range(len(self.engtalk)):
            cue = self.engtalk[k][1]
            if self.engtalk[k][1] == 1:
                sqlKorSearch = '''select korcue, kor from Korean 
                    where korcue between {} and {}
                    and talk_id = {}'''.format(cue, cue+2, self.engtalk[k][0])
            else:     
                sqlKorSearch = '''select korcue, kor from Korean 
                    where korcue between {} and {}
                    and talk_id = {}'''.format(cue-2, cue+2, self.engtalk[k][0])
            conn = f.get_conn()
            cur = conn.cursor()
            cur.execute(sqlKorSearch)
            krows = cur.fetchall() # tuple
            print(krows)
            # kstrs = " ".join(krows)
            # self.findKor.append(kstrs)
        # print(self.findKor)


s = ElasticSearch()
s.get('inspire')
s.korequiv()