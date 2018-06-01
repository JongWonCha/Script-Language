from tkinter import *
from tkinter import font
import urllib
import urllib.request

#인증키 : 5um4f7TgO48adXL7VSsi25MWHSnQG9sduzwQ%2FF7x0sh3jo5Wn6BJNpFYyzc%2F%2FMOOBo3EP%2BsNiTY71km2LEWdJA%3D%3D

g_Tk = Tk()
g_Tk.geometry("970x800+100+100")
DataList = []
url = str("")

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="[아빠 어디가?(관광정보서비스)]")
    MainText.pack()
    MainText.place(x=200)
    SearchFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    SearchWhat = Label(g_Tk, font = SearchFont, text="[관광지 검색]")
    SearchWhat.pack()
    SearchWhat.place(x = 10, y = 70)

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font = TempFont, width = 50, borderwidth = 12, relief = 'ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=120)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=870, y=127)

def InitSelectLabel():  # 이미지 와 선택시 등 처리
    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')

    selectLabel = Label(g_Tk, bg="white", height=15, width=45, borderwidth = 12, relief = 'ridge')
    selectLabel.pack()
    selectLabel.place(x=470, y=215)

    selectText = Text(g_Tk, width=45, height=5, borderwidth=12, relief='ridge')
    selectText.pack()
    selectText.place(x=470, y=635)

def SearchButtonAction():
    RenderText.configure(state='normal')
    RenderText.delete(0, END)
    SearchWhere()
    RenderText.bind('<<ListboxSelect>>', onselect)

    #RenderText.configure(state='disabled')

def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print('You selected item %d: "%s"' % (index, value))
    print(DataList)
    url = DataList.index(value) - 2
    url = DataList[url]
    print(url)

    from io import BytesIO
    from PIL import Image, ImageTk

    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    ph = ImageTk.PhotoImage(im)

    selectLabel = Label(g_Tk, image=ph, height=375, width=450)
    selectLabel.image = ph
    selectLabel.pack()
    selectLabel.place(x=480, y=225)

    selectText = Text(g_Tk, width=45, height=5, borderwidth=12, relief='ridge')

    selectText.insert(INSERT, '관광지명 : ')
    selectText.insert(INSERT, value)
    selectText.insert(INSERT, "\n")
    selectText.insert(INSERT, '전화 : ')
    selectText.insert(INSERT, DataList[DataList.index(value) - 1])
    selectText.insert(INSERT, "\n")
    selectText.insert(INSERT, '주소 : ')
    selectText.insert(INSERT, DataList[DataList.index(value) - 3])
    selectText.insert(INSERT, "\n")

    selectText.pack()
    selectText.place(x=470, y=635)

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
        #print(GeoInfoLibrary)
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
    else:
        print("Error!")

def InitRenderText():
    global RenderText

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Listbox(g_Tk, width=40, height=20, borderwidth=12, relief='ridge')#, yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)

InitTopText()
InitInputLabel()
InitSearchButton()
InitRenderText()
InitSelectLabel()
g_Tk.mainloop()