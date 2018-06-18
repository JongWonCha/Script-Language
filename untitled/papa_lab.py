from tkinter import *
from tkinter import font
import urllib
import urllib.request
# -*- coding: utf-8 -*-
import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import telepot
#from bs4 import BeautifulSoup
import traceback
import time

g_Tk = Tk()
g_Tk.geometry("1100x800+100+100")
DataList = []
SandDataList = []
url = str("")
bot = None

def InitTopText():
    TempFont = font.Font(g_Tk, size=30, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="[아빠 어디가?(관광정보서비스)]")
    MainText.pack()
    MainText.place(x=200)
    SearchFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
    SearchWhat = Label(g_Tk, font = SearchFont, text="[관광지 검색]")
    SearchWhat.pack()
    SearchWhat.place(x = 10, y = 70)

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font = TempFont, width = 84, borderwidth = 12, relief = 'ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=127)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=18, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=1000, y=127)

def InitSelectLabel():  # 이미지 와 선택시 등 처리
    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')

    selectLabel = Label(g_Tk, bg="white", height=20, width=50, borderwidth = 12, relief = 'ridge')  #사진창
    selectLabel.pack()
    selectLabel.place(x=300, y=215)

    selectLabel_2 = Label(g_Tk, bg="white", height=20, width=50, borderwidth=12, relief='ridge')  # 지도창
    selectLabel_2.pack()
    selectLabel_2.place(x=700, y=215)

    selectText = Text(g_Tk, width=107, height=12, borderwidth=12, relief='ridge') #밑창
    selectText.pack()
    selectText.place(x=300, y=570)

def SearchButtonAction():
    RenderText.configure(state='normal')
    RenderText.delete(0, END)
    SearchWhere()
    RenderText.bind('<<ListboxSelect>>', onselect)

def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)

    #print('You selected item %d: "%s"' % (index, value))
    #print(DataList)
    url = DataList.index(value) - 4
    url = DataList[url]
    print(url)

    from io import BytesIO
    from PIL import Image, ImageTk

    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    ph = ImageTk.PhotoImage(im)

    selectLabel = Label(g_Tk, image=ph, height=300, width=350)
    selectLabel.image = ph
    selectLabel.pack()
    selectLabel.place(x=310, y=225)

    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    selectText = Text(g_Tk, width=68, height=7, borderwidth=12, relief='ridge', font = TempFont)

    selectText.insert(INSERT, '관광지 : ')
    selectText.insert(INSERT, value)
    selectText.insert(INSERT, "\n")
    selectText.insert(INSERT, '전화 : ')
    selectText.insert(INSERT, DataList[DataList.index(value) - 1])
    selectText.insert(INSERT, "\n")
    selectText.insert(INSERT, '주소 : ')
    selectText.insert(INSERT, DataList[DataList.index(value) - 5])
    selectText.insert(INSERT, "\n")

    import spam
    print(spam.pick(value))

    SandDataList.clear()
    SandDataList.append(value)
    SandDataList.append(DataList[DataList.index(value) - 1])
    SandDataList.append( DataList[DataList.index(value) - 5])

    selectText.pack()
    selectText.place(x=300, y=570)

    import http.client
    import os
    import sys

    client_id = "ljwYPkFrTSfUQbLGr5Gb"
    client_secret = "hiJ0MWlJEr"
    aaaaa = DataList[DataList.index(value) - 3] + "," + DataList[DataList.index(value) - 2]
    map_server = "https://openapi.naver.com/v1/map/staticmap.bin?clientId=" + client_id + "&url=" + "https://kpu.ac.kr" + "&scale=1&crs=EPSG:4326&center=" \
                 + aaaaa + "&level=10&w=350&h=300&baselayer=default&markers=" + aaaaa # xml 결과

    request = urllib.request.Request(map_server)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if (rescode == 200):
        response_body = response.read()

        with urllib.request.urlopen(request) as a:
            raw_data = a.read()

        imm = Image.open(BytesIO(response_body))
        phm = ImageTk.PhotoImage(imm)

        selectLabel_2 = Label(g_Tk, image=phm, height=300, width=350)
        selectLabel_2.image = phm
        selectLabel_2.pack()
        selectLabel_2.place(x=710, y=225)

    else:
        print("Error Code:" + rescode)

def SearchWhere():
    import http.client
    from xml.dom.minidom import parse, parseString

    conn = None
    path = InputLabel.get()
    encText = urllib.parse.quote(path)

    server = "api.visitkorea.or.kr"
    servicekey = "5um4f7TgO48adXL7VSsi25MWHSnQG9sduzwQ%2FF7x0sh3jo5Wn6BJNpFYyzc%2F%2FMOOBo3EP%2BsNiTY71km2LEWdJA%3D%3D"
    conn = http.client.HTTPConnection(server)
    conn.request("GET", "/openapi/service/rest/KorService/searchKeyword?serviceKey=" + servicekey +
                 "&MobileApp=AppTest&MobileOS=ETC&pageNo=1&startPage=1&numOfRows=999&pageSize=10&listYN=Y&arrange=O&contentTypeId=12&keyword=" + encText)
    req = conn.getresponse()

    if int(req.status) == 200:
        response_body = req.read().decode('utf-8')

        parseData = parseString(response_body)

        GeoInfoWhere = parseData.childNodes

        row = GeoInfoWhere[0].childNodes[1].childNodes[0].childNodes

        global DataList
        DataList.clear()
        for item in row:
            list = item.childNodes
            for lis in list:
                if lis.nodeName == 'addr1':
                    DataList.append(lis.firstChild.nodeValue)
                if lis.nodeName == 'firstimage':
                    DataList.append(lis.firstChild.nodeValue)
                if lis.nodeName == 'tel':
                    DataList.append(lis.firstChild.nodeValue)
                if lis.nodeName == 'title':
                    DataList.append(lis.firstChild.nodeValue)
                    RenderText.insert(END, lis.firstChild.nodeValue)
                if lis.nodeName == 'mapx':
                    DataList.append(lis.firstChild.nodeValue)
                if lis.nodeName == 'mapy':
                    DataList.append(lis.firstChild.nodeValue)
    else:
        print("Error!")

def InitRenderText():
    global RenderText
    RenderText = Listbox(g_Tk, width=35, height=32, borderwidth=12, relief='ridge')
    RenderText.pack()
    RenderText.place(x=10, y=215)

def InitsnadButton():
    TempFont = font.Font(g_Tk, size=13, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="이메일전송", command=sandAction)
    SearchButton.pack()
    SearchButton.place(x=990, y=80)

def InitTeleButton():
    TempFont = font.Font(g_Tk, size=13, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="텔레그램", command=TeleAction)
    SearchButton.pack()
    SearchButton.place(x=900, y=80)

def TeleAction():
    global bot
    bot = telepot.Bot('618308633:AAEjq-PhyB4wCBk4QWHMDXooHTp-iDfQ0HA')
    bot.getMe()

    bot.message_loop(Handle)

    print("Listening...")


    #bot.sendMessage("518224794", "아빠 어디가?")


def Handle(msg):
    global bot
    import http.client
    from xml.dom.minidom import parse, parseString
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg['text'])
    if content_type != 'text':
        bot.sendMessage("518224794", '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return



    conn = None
    path = msg['text']
    encText = urllib.parse.quote(path)

    server = "api.visitkorea.or.kr"
    servicekey = "5um4f7TgO48adXL7VSsi25MWHSnQG9sduzwQ%2FF7x0sh3jo5Wn6BJNpFYyzc%2F%2FMOOBo3EP%2BsNiTY71km2LEWdJA%3D%3D"
    conn = http.client.HTTPConnection(server)
    conn.request("GET", "/openapi/service/rest/KorService/searchKeyword?serviceKey=" + servicekey +
                 "&MobileApp=AppTest&MobileOS=ETC&pageNo=1&startPage=1&numOfRows=999&pageSize=10&listYN=Y&arrange=O&contentTypeId=12&keyword=" + encText)
    req = conn.getresponse()
    if int(req.status) == 200:
        response_body = req.read().decode('utf-8')

        parseData = parseString(response_body)

        GeoInfoWhere = parseData.childNodes

        row = GeoInfoWhere[0].childNodes[1].childNodes[0].childNodes

        for item in row:
            st = str()
            list = item.childNodes
            for lis in list:
                if lis.nodeName == 'addr1':
                    st += "주소 : " + lis.firstChild.nodeValue
                if lis.nodeName == 'tel':
                    st += "\n전화번호 : " + lis.firstChild.nodeValue
                if lis.nodeName == 'title':
                    #bot.sendMessage("518224794",lis.firstChild.nodeValue)
                    st += "\n이름 : " + lis.firstChild.nodeValue
                    bot.sendMessage("518224794", st)







def sandAction():
    print(SandDataList)


    # global value
    host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
    port = "587"
    htmlFileName = "logo.html"

    senderAddr = "chajw950@gmail.com" # 보내는 사람 email 주소.
    recipientAddr = "gagongin@naver.com"  # 받는 사람 email 주소.

    msg = MIMEText("관광지명 : " + SandDataList[0] + "\n" + "전화 : " + SandDataList[1] + "\n" + "주소: " + SandDataList[2])
    #msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = "아빠 어디가 이메일 왔습니다."
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    # MIME 문서를 생성합니다.
    '''htmlFD = open(htmlFileName, 'rb')
    HtmlPart = MIMEText(htmlFD.read(), 'html', _charset='UTF-8')
    htmlFD.close()'''

    # 만들었던 mime을 MIMEBase에 첨부 시킨다.
    #msg.attach(HtmlPart)

    # 메일을 발송한다.
    s = mysmtplib.MySMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("chajw950@gmail.com","ok1942kodk&U")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()

InitTopText()
InitInputLabel()
InitSearchButton()
InitRenderText()
InitSelectLabel()
InitsnadButton()
InitTeleButton()
g_Tk.mainloop()