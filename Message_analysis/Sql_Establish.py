import sqlite3,csv,re
import pandas as pd
with open('godword.csv',encoding='utf-8') as file:#開啟檔案使用讀取模式讀取的編碼為utf-8
    goodword=csv.reader(file)#讀取檔案
    goodword=pd.DataFrame(goodword)#轉成dataframe方便提取資料
with open('badword.csv',encoding='utf-8') as files:
    badword=csv.reader(files)
    badword=pd.DataFrame(badword)
con = sqlite3.connect('wordsdatabase.db')#連接數據庫
cursorObj = con.cursor()
cursorObj.execute(
'''CREATE TABLE "worddata" (
	"id"	INTEGER,
	"word"	TEXT,
	"badorgood"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT));''')#創建數據庫格式前面為名稱後面為格式
    #PRIMARY KEY("id" AUTOINCREMENT))這段是讓id這個欄位自動生成流水號
for i in range(len(goodword)):
    word=re.sub(r'[^\u4e00-\u9fa5]','', str(goodword[0][i]))#過濾非中文字元
    GorB=re.sub(r'[^0-9]','', str(goodword[1][i]))#過濾非數字字元
    cursorObj.execute('INSERT INTO worddata (word,badorgood) VALUES (?,?)',(word,GorB))#將資料寫入資料庫
    con.commit()
for i in range(len(badword)):
    word=re.sub(r'[^\u4e00-\u9fa5]','', str(badword[0][i]))
    GorB=re.sub(r'[^0-9]','', str(badword[1][i]))
    cursorObj.execute('INSERT INTO worddata (word,badorgood) VALUES (?,?)',(word,GorB))
    con.commit()
