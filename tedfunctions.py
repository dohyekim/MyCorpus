import pymysql

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


def updateTalk():

    sqlupdateId = "select talk_id from Talk where isKorean is null"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sqlupdateId)
    uid = cur.fetchall()

    if len(uid) == 0:
        return

    uplastid = uid[0][0]


    sqlUpdate = '''update Talk t set isKorean = (select case when max(k.kor) is null then 0 else 1 end
                                from English e left outer join Korean k on e.talk_id = k.talk_id
                                where e.talk_id = t.talk_id)
                    where talk_id >= ''' + str(uplastid) + ';'

    try: 
        print(" UPDATE STARTED ")
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sqlUpdate)
        conn.commit()
        print(" UPDATE SUCCESS >> ", cur.rowcount)

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

