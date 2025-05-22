import sqlite3
import json

def ClientBK(uphone,pnumber,unumber,stime):                    # 客戶訂位 進場時間 車位號碼 客戶電話 車牌號碼
    try:
        conn = sqlite3.connect('booking.db')
        conn.execute( f"insert into Booking(Pnumber , Phone, Number, Time)\
                            select '{pnumber}', '{uphone}', '{unumber}' ,'{stime}' \
                        where not exists(\
                            select 1 from Booking where Pnumber='{pnumber}' and Phone='{uphone}' and Number='{unumber}' and Time='{stime}');")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')
    else: print("訂位成功")

def ClientEdit(uphone,pnumber,unumber,stime):                  # 修改訂位內容
    try:
        conn = sqlite3.connect('booking.db')
        cursor = conn.execute(f"select * from Booking where Phone='{uphone}'")
        data = cursor.fetchall()
        print("\n原訂位內容：")
        if len(data) > 0:
            for record in data:
                print(f"日期:{record[3]}")
        conn.execute(f"update Booking set Time='{stime}' where Name='{pnumber}' and Phone='{uphone}'and Number='{unumber}'")
        cursor = conn.execute(f"select * from Booking where Name='{pnumber}' and Phone='{uphone}'and Number='{unumber}'")
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

def ClientSearch(uphone):                           # 查詢訂位內容
    try:
        conn = sqlite3.connect('booking.db')
        cursor = conn.execute(f"select * from Booking where Phone='{uphone}'")
        data = cursor.fetchall()
        print("\n已訂位時段：")
        if len(data) > 0:
            for record in data:
                return record
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'=>資料庫連接或資料表建立失敗，錯誤訊息為{e}')
