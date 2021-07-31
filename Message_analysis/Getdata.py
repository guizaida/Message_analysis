import requests as req
from bs4 import BeautifulSoup
import re,time,jieba,math,sqlite3
from threading import Thread
import matplotlib.pyplot as plt
def Getmessage(i):
    url='https://www.pttweb.cc/user/'+m.id+'?t=message&page='+str(i)
    data=req.get(url).text#獲取原始碼
    root=BeautifulSoup(data,"lxml")#使用lxml格式進行解析
    datas=root.find_all('span',{'class':'yellow--text text--darken-2'},{'data-v-4977f262':''})#尋找所有此標籤內的文字
    for a in datas:
        m.wordata.append(a.text)
        m.wordcount+1
    for i in range(m.wordcount1,m.wordcount):
        pattern = re.sub(r'[^\u4e00-\u9fa5]','', m.wordata[i])#去除所有非中文的字符
        m.wordata[i]=pattern
        m.wordcount1+=1
def Getpage(url):
    data=req.get(url).text#獲取原始碼
    root=BeautifulSoup(data,"lxml")#使用lxml格式進行解析
    namber=root.find('div',{'class':'headline e7-block-title pl-3 mt-4'}).text#尋找留言數
    namber=namber.split(m.id)
    m.namber=re.sub("[^0-9]", '', namber[1])#去除除了數字以外的文字
def Filterwords():
    for i in range(len(m.wordata)):
        m.wordata1.append(m.wordata[i])
    for i in range(len(m.wordata1)):
        pattern = re.sub(r'[^\u4e00-\u9fa5]','', m.wordata1[i])#去除所有非中文的字符
        m.wordata2.append(pattern)
    for sentence in m.wordata2:
        seg_list = jieba.lcut(sentence)#分詞
        for i in range(len(seg_list)):
            if seg_list[i] != '':#刪除空字串
                m.wordata3.append(seg_list[i])
    for i in range(len(m.wordata3)):#計算出現次數
        counts=sentence.count(m.wordata3[i])
        m.wordnamber[m.wordata3[i]]=counts+1#計算出現次數因從0開始所以+1
def GoodorBadcount():
    con = sqlite3.connect('wordsdatabase.db')#連結資料庫
    cursorObj = con.cursor()
    db=cursorObj.execute('SELECT * FROM worddata')#取出所有資料
    for item in db:#將資料一筆一筆拿出來是正面詞放入正面詞的列表,不是則放進負面詞的列表
        if str(item[2]) == '0':
            m.Goodworddata.append(item[1])
        else:
            m.Badworddata.append(item[1])
    for i in range(len(m.wordata3)):#使用jieba分好詞的資料來比對計算正負面的數量
        if m.wordata3[i] in m.Goodworddata:
            m.Goodcount+=1
            m.Goodwords.append(m.wordata3[i])
        elif m.wordata3[i] in m.Badworddata:
            m.Badcount+=1
            m.Badwords.append(m.wordata3[i])
def goodcount():
    for i in range(len(m.Goodwords)):#計算出現次數
        counts=m.Goodwords.count(m.Goodwords[i])
        m.Goodwordscount[m.Goodwords[i]]=counts+1#計算出現次數因從0開始所以+1
    m.Goodwordscount=(sorted(m.Goodwordscount.items(), key=lambda d:d[1], reverse = True))#對正面字詞出現數量進行排序
def badcount():
    for i in range(len(m.Badwords)):#計算出現次數
        counts=m.Badwords.count(m.Badwords[i])
        m.Badwordscount[m.Badwords[i]]=counts+1#計算出現次數因從0開始所以+1
    m.Badwordscount=(sorted(m.Badwordscount.items(), key=lambda d:d[1], reverse = True))#對正面字詞出現數量進行排序
def Database_mapping():
    xdata1=[m.Goodcount,m.Badcount]#正負面詞出現次數
    plt.rcParams['font.family']='Microsoft YaHei'#設定圖片字體
    plt.rcParams['font.size']=20#設定圖片字體大小
    lb=['正面詞','負面詞']#設定標籤
    colors=['gold','royalblue']#標籤代表研社
    explode=[0,0]#是否分離
    plt.pie(xdata1,labels=lb,colors=colors,shadow=True,explode=explode,autopct='%1.1F%%')#畫圓餅圖
    plt.axis('equal')
    plt.savefig('1.png')#儲存圖片
    plt.close()#關閉圖片這步必須要有不然其他程式無法開啟

class m():
    Badwordscount={}
    Goodcount=0
    Badcount=0
    Goodwordscount={}
    Goodworddata=[]
    Badworddata=[]
    Goodwords=[]
    Badwords=[]
    wordata=[]
    wordata1=[]
    wordata2=[]
    wordata3=[]
    urls=[]
    namber=0
    wordnamber={}
    namberlist=[]
    wordcount=0
    wordcount1=0
    id=''
def run(id):
    m.id=id
    url='https://www.pttweb.cc/user/'+m.id+'?t=message'
    Getpage(url)
    pagenamber=int(m.namber)-10#扣除第一頁留言
    pagenamber=pagenamber/10#一頁是十個留言,計算頁數
    pagenamber=math.ceil(pagenamber)#無條件進位
    pagenamber=int(pagenamber)#將浮點數float轉換成int整數型別
    if pagenamber > 49:
        pagenamber=49
    threadA=[]
    for i in range(pagenamber+1):#使用多線程縮短爬取時間
        threadA.append(Thread(target =Getmessage , args = (i,)))
        threadA[i].start()
        time.sleep(1)
    for i in range(pagenamber):#讓線程會等待不然他會直接執行後面的程式碼
        threadA[i].join
    Filterwords()
    GoodorBadcount()
    goodcount()
    badcount()
    Database_mapping()
if __name__ == '__main__':#這個是如果直接執行這個.py檔案的話會執行的動作但如果在別的.py檔案import這個檔案將不會運行
    time_start = time.time()#計時開始
    run('wuzhuzhu')
    print(m.Goodcount,m.Badcount)
    time_end = time.time() #計時終止
    time_c= time_end - time_start#計算使用秒數
    print("執行時間：%f 秒" % (time_c))
