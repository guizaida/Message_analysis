import tkinter as tk
from threading import Thread
import time
import os,re
import tkinter.scrolledtext as tksb
import Getdata as gd
from PIL import Image, ImageTk
from tkinter import END,INSERT
def Get():
    global states#將變數轉變為全域變數
    button1["state"] = tk.DISABLED#將分析按鈕鎖住
    usid=id.get()#獲取id欄位的值
    if str(usid) == '':#檢查值是否為空
        pass
    else:
        usid=re.sub(r"\s+", "", usid)#去除所有空白以防止複製貼上多空白
        gd.run(usid)#啟動主程式
    img=Image.open('1.png')#開啟分析圖片
    img1=img.resize((320,240))#壓縮至GUI尺寸
    img1.save('2.png')#儲存
    img=Image.open('2.png')#開啟圖片
    img_png1 = ImageTk.PhotoImage(img)#插入gui中
    label3.configure(image=img_png1)
    label3.image=img_png1
    goodwords=[]
    badwords=[]
    for i in range(len(gd.m.Goodwordscount)):
        goodwords.append(gd.m.Goodwordscount[i][0]+':'+str(gd.m.Goodwordscount[i][1]))#將正面詞與出現次數加入列表
        text1.insert(tk.INSERT,goodwords[i]+'\n')#將正面詞以及出現出量插入Gui中
    for i in range(len(gd.m.Badwordscount)):
        badwords.append(gd.m.Badwordscount[i][0]+':'+str(gd.m.Badwordscount[i][1]))
        text2.insert(tk.INSERT,badwords[i]+'\n')
    button1["state"] = tk.NORMAL#釋放分析按鈕
    #以下為清空所有資料
    gd.m.Badwordscount={}
    gd.m.Goodcount=0
    gd.m.Badcount=0
    gd.m.Goodwordscount={}
    gd.m.Goodworddata=[]
    gd.m.Badworddata=[]
    gd.m.Goodwords=[]
    gd.m.Badwords=[]
    gd.m.wordata=[]
    gd.m.wordata1=[]
    gd.m.wordata2=[]
    gd.m.wordata3=[]
    gd.m.urls=[]
    gd.m.namber=0
    gd.m.wordnamber={}
    gd.m.namberlist=[]
    gd.m.wordcount=0
    gd.m.wordcount1=0
    gd.m.id=''
    states=True#轉換states狀態
def closeNewWindow():
        global newWindow,Convertcontroller
        states=True#轉換states狀態
        newWindow.destroy()#關閉新視窗
def Showstate():
    global winMain,newWindow,Convertprinter,states
    img=Image.open('0.png')#開啟預設空白圖片
    img_png1 = ImageTk.PhotoImage(img)#插入Gui中
    label3.configure(image=img_png1)
    label3.image=img_png1
    text1.delete(1.0,tk.END)#清空正面詞彙
    text2.delete(1.0,tk.END)#清空負面詞彙
    newWindow = tk.Toplevel(winMain)#設定新視窗名稱
    center_window1(175, 110)#設定視窗大小
    newWindow.resizable(width=0, height=0)
    newWindow.transient(winMain)
    newWindow.title('程式執行中')#設定新視窗標題
    newWindow.protocol("WM_DELETE_WINDOW",closeNewWindow)
    Convertprinter = tk.StringVar()#獲取文字
    Convertprinter.set("搜尋中")#設定視窗內標籤顯示文字
    PrinterLabel = tk.Label(newWindow,anchor="w",textvariable=Convertprinter,font=(fontName,12),compound='center',width=16)#視窗中顯示標籤
    PrinterLabel.grid(padx=10,pady=10,row=0,column=0,sticky='w')#設定標籤位置
    states=False#初始化states狀態
    show=Thread(target = state)#設定線程1
    show.start()#線程一起動
    get=Thread(target = Get)#設定線程2
    get.start()#線程2啟動

def center_window(w, h):
    #獲取主螢幕解度
    ws = winMain.winfo_screenwidth()
    hs = winMain.winfo_screenheight()
    # 計算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    winMain.geometry('%dx%d+%d+%d' % (w, h, x, y))#將視窗位置設定於螢幕正中央  
def center_window1(w, h):
    # 獲取主螢幕解析度
    ws = newWindow.winfo_screenwidth()
    hs = newWindow.winfo_screenheight()
    # 計算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    newWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))#將視窗位置設定於螢幕正中央 

def state():
    global states
    #以下為新視窗搜尋中...變動的方式
    while states == False:
        textstr = "搜尋中"
        for item in range(1,7):
            if item == 1:
                Convertprinter.set("搜尋中")#更改標籤文字
                time.sleep(1)
            else:
                textstr = "搜尋中" + ("."*(item-1))
                Convertprinter.set(textstr)#更改標籤文字
                time.sleep(1)
        if states == True:#當主程式執行完退出此循環
            break
    newWindow.destroy()#視窗關閉
fontName = "標楷體"#設定字體
winMainName='留言分析系統'#主視窗標題
winMain = tk.Tk()  # 產生 TK 介面物件
center_window(840, 600)#將視窗介面設定為螢幕正中間
winMain.title(winMainName)#設定主視窗標題
label1=tk.Label(text='請輸入ID',width=20,font=(fontName,20))#設定請輸入id標籤
label1.place(x=5,y=5)
id=tk.Entry(winMain,width=20,font=(fontName,20))#設定id輸入框
id.place(x=10,y=50)
button1=tk.Button(winMain,text='分析',font=(fontName,16),width=10,command=Showstate)#設定按鈕command=後面接上點擊後觸發的函式
button1.place(x=80,y=90)
label2=tk.Label(winMain,text='正負面比例圖',width=20,font=(fontName,20))
label2.place(x=10,y=200)
img=Image.open('0.png')
img_png = ImageTk.PhotoImage(img)
label3=tk.Label(winMain,image=img_png,width =320,height=240,font=(fontName,20))
label3.place(x=10,y=250)
label4=tk.Label(winMain,text='正面詞彙',font=(fontName,20))
label4.place(x=500,y=5)
text1=tksb.ScrolledText(height=10,width=20,font=(fontName,16))
text1.place(x=440,y=50)
label5=tk.Label(winMain,text='負面詞彙',font=(fontName,20))
label5.place(x=500,y=280)
text2=tksb.ScrolledText(height=10,width=20,font=(fontName,16))
text2.place(x=440,y=330)
winMain.mainloop()#啟動無限循環使視窗持續顯示
os._exit(0)