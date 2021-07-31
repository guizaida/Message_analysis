import sqlite3
def update(word,GorB):
    con = sqlite3.connect('wordsdatabase.db')
    cursorObj = con.cursor()
    db=cursorObj.execute('SELECT * FROM worddata')#取出所有資料
    dbdata=[]
    m.st=0
    for item in db:
        dbdata.append(item[1])
    #如果資料不再資料庫中判斷資料室面面或者負面詞將資料寫入資料庫
    if word not in dbdata:
        m.st=1
        if str(GorB) == '0':
            cursorObj.execute('INSERT INTO worddata (word,badorgood) VALUES (?,?)',(str(word),int(GorB)))
            con.commit()
            with open('goodword.csv','a',encoding='utf-8') as files:#更新csv檔案
              adddata=files.write(str(word)+',')
              adddata=files.write(str(GorB)+'\n')  
        else:
            cursorObj.execute('INSERT INTO worddata (word,badorgood) VALUES (?,?)',(str(word),int(GorB)))
            con.commit()
            with open('badword.csv','a',encoding='utf-8') as files:#更新csv檔案
              adddata=files.write(str(word)+',')
              adddata=files.write(str(GorB)+'\n')
class m():
    st=0  
if __name__ == '__main__':
    update('憋死',1)
