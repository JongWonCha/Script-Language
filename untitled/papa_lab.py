from tkinter import *
from io import BytesIO
from tkinter import font
import urllib
import urllib.request
from PIL import Image, ImageTk

#인증키 : 5um4f7TgO48adXL7VSsi25MWHSnQG9sduzwQ%2FF7x0sh3jo5Wn6BJNpFYyzc%2F%2FMOOBo3EP%2BsNiTY71km2LEWdJA%3D%3D

g_Tk = Tk()
g_Tk.geometry("1000x800+100+100")
DataList = []

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="[아빠 어디가?(관광정보서비스)]")
    MainText.pack()
    MainText.place(x=200)
    SearchFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    SearchWhat = Label(g_Tk, font = SearchFont, text="[관광지 검색]")
    SearchWhat.pack()
    SearchWhat.place(x = 10, y = 50)

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font = TempFont, width = 50, borderwidth = 12, relief = 'ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=100)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="검색",  command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=870, y=107)


def SearchButtonAction():
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    SearchWhere()
    RenderText.configure(state='disabled')

def MakeHtmlDoc(BookList):
    from xml.dom.minidom import getDOMImplementation
    # DOM 개체를 생성합니다.
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "html", None)  # HTML 최상위 엘리먼트를 생성합니다.
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성
    body = newdoc.createElement('body')

    for bookitem in BookList:
        # Bold 엘리먼트를 생성합니다.
        b = newdoc.createElement('b')
        # 텍스트 노드를 만듭니다.
        ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
        b.appendChild(ibsnText)

        body.appendChild(b)

        # <br> 부분을 생성합니다.
        br = newdoc.createElement('br')

        body.appendChild(br)

        # title 부분을 생성합니다.
        p = newdoc.createElement('p')
        # 텍스트 노드를 만듭니다.
        titleText = newdoc.createTextNode("Title:" + bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)  # <br> 부분을 부모 에릴먼트에 추가합니다.

    # Body 엘리먼트를 최상위 엘리먼트에 추가시킵니다.
    top_element.appendChild(body)

    return newdoc.toxml()

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
                 "&MobileApp=AppTest&MobileOS=ETC&pageNo=1&startPage=1&numOfRows=10&pageSize=10&listYN=Y&arrange=A&contentTypeId=12&keyword=" + encText)
    req = conn.getresponse()
    global DataList
    DataList.clear()
    #print(req.status)

    if int(req.status) == 200:
        response_body = req.read().decode('utf-8')
        #print(response_body)

        parseData = parseString(response_body)

        MakeHtmlDoc(DataList)

        GeoInfoLibrary = parseData.childNodes
        #print(GeoInfoLibrary)
        row = GeoInfoLibrary[0].childNodes[1].childNodes[0].childNodes
        i = 0
        for item in row:
            list = item.childNodes
            for lis in list:
                if lis.nodeName == 'addr1':
                    print('주소: ',lis.firstChild.nodeValue)
                    RenderText.insert(INSERT,'주소: ')
                    RenderText.insert(INSERT, lis.firstChild.nodeValue)
                    RenderText.insert(INSERT, '\n')
                if lis.nodeName == 'addr2':
                    print('주소: ',lis.firstChild.nodeValue)
                if lis.nodeName == 'firstimage':
                    print('사진1: ',lis.firstChild.nodeValue)
                    RenderText.insert(INSERT, '사진1 : ')
                    RenderText.insert(INSERT, lis.firstChild.nodeValue)
                    RenderText.insert(INSERT, '\n')
                if lis.nodeName == 'firstimage2':
                    print('사진2: ',lis.firstChild.nodeValue)
                    RenderText.insert(INSERT, '사진2: ')
                    RenderText.insert(INSERT, lis.firstChild.nodeValue)
                    RenderText.insert(INSERT, '\n')
                if lis.nodeName == 'tel':
                    print('전화번호: ',lis.firstChild.nodeValue)
                    RenderText.insert(INSERT, '연락처: ')
                    RenderText.insert(INSERT, lis.firstChild.nodeValue)
                    RenderText.insert(INSERT, '\n')
                if lis.nodeName == 'title':
                    print('시설명: ',lis.firstChild.nodeValue)
                    RenderText.insert(INSERT, '시설명: ')
                    RenderText.insert(INSERT, lis.firstChild.nodeValue)
                    RenderText.insert(INSERT, '\n\n')
            print('\n')
            '''if item.nodeName == "addr1":
                subitems = item.childNodes

                DataList.append((subitems.firstChild.nodeValue, subitems.firstChild.nodeValue, "-"))
                print(DataList)'''

            for i in range(len(DataList)):
                RenderText.insert(INSERT, "[")
                RenderText.insert(INSERT, i + 1)
                RenderText.insert(INSERT, "] ")
                RenderText.insert(INSERT, "시설명: ")
                RenderText.insert(INSERT, DataList[i][0])
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "주소: ")
                RenderText.insert(INSERT, DataList[i][1])
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "전화번호: ")
                RenderText.insert(INSERT, DataList[i][2])
                RenderText.insert(INSERT, "\n\n")
    else:
        print("Error!")

def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=80, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

InitTopText()
InitInputLabel()
InitSearchButton()
InitRenderText()
#InitSendEmailButton()
#InitSortListBox()
#InitSortButton()
g_Tk.mainloop()