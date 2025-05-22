import sqlite3
import json

def AdminCheck(account, password):                               # admin帳密比對
    try:
        with open('pass.json','r', encoding='UTF-8') as D:
            AdminData = json.load(D)
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')
    else:
        for ch in AdminData:
            if (account, password) == (ch['帳號'], ch['密碼']):
                return True

def BuildDB():                                          # 建立訂位資料庫
    conn = sqlite3.connect('Booking.db')
    conn.execute('''create table if not exists Booking(
            Phone   char(10)  not null ,
            Pnumber  char(15)  not null ,
            Number     char(15)  not null primary key,
            Time     char(20)  not null ,
            State    char(20)  not null
        );''')
    print('=>資料庫已建立')
    conn.commit()
    conn.close()



def AdminDelete(unumber):                           # 取消訂位
    try:
        conn = sqlite3.connect('Booking.db')
        conn.execute(f"delete from Booking where Number='{unumber}'")
        conn.commit()
        conn.close()
        return"已取消訂位"
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')


def SearchAll():                                    # 列出所有資料
    try:
        conn = sqlite3.connect('Booking.db')
        cursor = conn.execute(" select * from Booking ")
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')

def ClientBK(uphone,pnumber,unumber,stime,State):                    # 客戶訂位 : 車位號碼 客戶電話 車牌號碼 進場時間
    try:
        conn = sqlite3.connect('Booking.db')
        conn.execute( f"insert into Booking(Pnumber , Phone, Number, Time, State)\
                            select '{pnumber}', '{uphone}', '{unumber}' ,'{stime}', '{State}' \
                        where not exists(\
                            select 1 from Booking where Pnumber='{pnumber}' and Phone='{uphone}' and Number='{unumber}' and Time='{stime}' and State='{State}');")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')
    else: print("訂位成功")

def ClientEdit(uphone,pnumber,unumber,stime,State):                  # 修改訂位內容
    try:
        conn = sqlite3.connect('Booking.db')
        cursor = conn.execute(f"select * from Booking where Number='{unumber}'")
        data = cursor.fetchall()
        print("\n原訂位內容：")
        if len(data) > 0:
            for record in data:
                print(f"日期:{record[3]}")
        conn.execute(f"update Booking set State='{State}', Time='{stime}' where Pnumber='{pnumber}' and Phone='{uphone}'and Number='{unumber}'")
        cursor = conn.execute(f"select * from Booking where Pnumber='{pnumber}' and Phone='{uphone}'and Number='{unumber}'")
        data = cursor.fetchall()
        print("修改成功")
        print("\n修改後訂位內容：", end="")
        if len(data) > 0:
            for record in data:
                print(f"日期:{record[3]}")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')

def ClientSearch(unumber):                           # 查詢訂位內容
    try:
        conn = sqlite3.connect('Booking.db')
        cursor = conn.execute(f"select * from Booking where Number='{unumber}'")
        data = cursor.fetchall()
        print("\n已訂位時段：")
        if len(data) > 0:
            for record in data:
                return record
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')


def RecordDB():
    conn = sqlite3.connect('Booking.db')                                      # 建立紀錄資料庫
    conn.execute('''create table if not exists Record(
            Phone   char(10)  not null ,
            Pnumber  char(10)  not null ,
            Number   char(10)  not null,
            InTime    char(20)  not null ,
            OutTime    char(20)  not null ,
            Amount    char(6)  not null ,
            Note      char(6)  not null
        );''')
    print('=>資料庫已建立')
    conn.commit()
    conn.close()

def RecordLogin(Phone,pnumber,number,intime,outtime,amount,Note):                    # 電話 車位 車牌 進場時間 離場時間 金額 狀態
    try:
        conn = sqlite3.connect('Booking.db')
        conn.execute( f"insert into Record(Phone ,Number , Pnumber, InTime, OutTime, Amount, Note)\
                            select '{Phone}','{number}', '{pnumber}', '{intime}' ,'{outtime}','{amount}','{Note}' \
                        where not exists(\
                            select 1 from Record where Number='{number}' and InTime='{intime}' and OutTime='{outtime}' and Amount='{amount}'and Note='{Note}' and Phone='{Phone}');")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')
    else: print("登錄成功")

def LogAll():                                    # 列出所有紀錄
    try:
        conn = sqlite3.connect('Booking.db')
        cursor = conn.execute(" select * from Record ")
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')

def PaylogEdit(pnumber,outtime):                  # 修改紀錄內容 (繳費未離場)
    try:
        conn = sqlite3.connect('Booking.db')
        cursor = conn.execute(f"select * from Record where Pnumber='{pnumber}'")
        data = cursor.fetchall()
        print("\n原訂位內容：")
        if len(data) > 0:
            for record in data:
                print(f"日期:{record[3]}")
        conn.execute(f"update Record set OutTime=' ', Note='繳費未離場' where Pnumber='{pnumber}' and OutTime = '{outtime}'")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')
