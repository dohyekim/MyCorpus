import pymysql

def get_conn():
    return pymysql.connect(
        host='127.0.0.1',
        user='dooo',
        password='1234',
        port=3306,
        db='corpusdb',
        charset='utf8')



def getLastId(sql):
    conn = get_conn()
    cur = conn.cursor()    
    cur.execute(sql)
    lastid = cur.fetchall()
    cur.close()
    return lastid   

def saveUpdata(updatesql, ids, diff='isKorean'):
    try: 
        print(" UPDATE STARTED ")
        conn = get_conn()
        conn.autocommit = False
        cur = conn.cursor()

        cur.execute(updatesql)
        conn.commit()
        print(" DIFF UPDATE SUCCESS >> ", diff, cur.rowcount, "id>> ", ids)

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

def updateTalk():

    sqlupdateId = "select talk_id from Talk where isKorean is null"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sqlupdateId)
    uid = cur.fetchall()

    if len(uid) == 0:
        return

    uplastid = uid[0][0]
    print(uplastid)
    sqlUpdate = '''update Talk t set isKorean = (select case when max(k.kor) is null then 0 else 1 end
                                from English e left outer join Korean k on e.talk_id = k.talk_id
                                where e.talk_id = t.talk_id)
                    where talk_id >= ''' + str(uplastid)

    saveUpdata(sqlUpdate, uplastid)


def updateDiff():
    print(" ============ Update Diff Started ==================")
    sqlupdateId = "select talk_id from Talk where diff is null"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sqlupdateId)
    uid = cur.fetchall()

    if len(uid) == 0:
        return

    uplastid = uid[0][0]

    sqlseleng = "select engcue from English where talk_id = {} order by engcue desc limit 1".format(uplastid)
    sqlselkor = "select korcue from Korean where talk_id = {} order by korcue desc limit 1".format(uplastid)

    cur = conn.cursor()
    cur.execute(sqlseleng)
    
    # English table의 row수
    engcnt = cur.fetchall()
    # if len(engcnt) != 0:
    engs = engcnt[0][0]

    # Korean table의 row수
    cur = conn.cursor()
    cur.execute(sqlselkor)
    korcnt = cur.fetchall()
    if len(korcnt) != 0:
        kors = korcnt[0][0]
    else:
        sqlupdate_2 = 'update Talk set diff = 2 where talk_id = {}'.format(uplastid)
        saveUpdata(sqlupdate_2, uplastid, '2222222')
        return

    # 3개 이상 차이가 나면 skip
    sqlupdate_0 = 'update Talk set diff = 0 where talk_id = {}'.format(uplastid)

    # 3개 이하로 차이가 나는 경우
    sqlupdate_1 = 'update Talk set diff = 1 where talk_id = {}'.format(uplastid)


    if abs(engs - kors) > 3 and kors != 0:

        saveUpdata(sqlupdate_0, uplastid, '00000000')

    else:
        saveUpdata(sqlupdate_1, uplastid, '111111111')
