import urllib.request
import json
import sys
import random

from openpyxl import load_workbook
from bs4 import BeautifulSoup

naver_client_id = "testing" # 개발자센터에서 발급받은 Client ID 값
naver_client_secret = "testing" # 개발자센터에서 발급받은 Client Secret 값

tr_flag = False

def toeic_schedule() :
    url = "https://appexam.ybmnet.co.kr/toeic/receipt/receipt.asp"
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    size = [17, 18, 18, 7, 6]
    st = '|          시험일자           |            접수마감              |              성적발표             |    응시료    |         구분          |\n'
    keylist = []

    for tr in soup.find("table", class_="table_info").find_all("tr"):
        keyward = "|  "
        temp = tr.find_all("td")
        for td in range(len(temp)) :
            keyward += temp[td].text
            if "낮" in temp[td].text:
                keyward += ' '
            if "정기" in temp[td].text:
                keyward += '    '
            for i in range((size[td] - len(temp[td].text))):
                keyward +=" "
            keyward +="  |  "    
        if len(keyward) > 20:
            keylist.append(keyward)
    st += u'\n'.join(keylist)+'\n'+"https://appexam.ybmnet.co.kr/toeic/receipt/receipt.asp"
    return st

def today_words():
    keywords = []
    url = "https://endic.naver.com/?sLn=kr"
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    soup = soup.find("ul", class_ = "component_today_word")
        
    for i in soup.find_all("li", class_ = "item") :
        keywords.append(i.find("a").text)
        for j in i.find("div", class_="txt_trans").text.split('\n'):
            keywords.append(j.strip())
    print(keywords)
    return u'\n'.join(keywords)

def recommend_popsong():
    keywords = []
    url = "https://music.bugs.co.kr/genre/chart/pop/pop/total/day"
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    
    title = []
    artist = []
    for p in soup.find_all("p", class_ = "title") :
        title.append(p.find("a").text)
    for p in soup.find_all("p", class_ = "artist") :
        artist.append(p.find("a").text)
    
    r = random.choice(range(100))
    st = "지금은 " + artist[r]+"의 "+ title[r] + "어떠세요?"
    return st

def saved_words():
    keywords = []
    engg = load_workbook(filename = 'english.xlsx')
    sheet1 = engg['Sheet1']
    dic =[]

    for i in sheet1.rows:
        num = i[0].value
        eng = i[1].value
        mean = i[2].value
        st = str(num) +"  "+ eng +"  "+mean
        dic.append(st)

    for i in range(5):
        keywords.append(random.choice(dic)) 
    return u'\n'.join(keywords)    

def sentence_translation(text):
    encText = urllib.parse.quote(text[12:])
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",naver_client_id)
    request.add_header("X-Naver-Client-Secret",naver_client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        tr = json.loads(response_body)["message"]["result"]["translatedText"]
        return u'번역 : '+ tr
    else:
        return u'번역에 실패했습니다.'    

def make_bot_respone(text):
    global tr_flag
    if len('<@UEXDG2P34>') == len(text):
        st = '[영어 도우미 ToicsBot]\n\n'
        st += '사용 가능한 기능!\n'
        st += '- 토익 일정                                                                 ex) 토익 일정 알려줘\n'
        st += '- 토익 빈출단어(저장된 단어를 가져옵니다)          ex) 토익 빈출 영단어 알려줘\n'
        st += '- 오늘의 영단어                                                         ex) 오늘의 영단어 알려줘\n'
        st += '- 팝송 추천                                                                 ex) 팝송 추천 해줘\n'
        st += '- 번역                                                                          ex)번역해줘\n'
        return st

    if "토익" in text and "일정" in text :
        return toeic_schedule()
    if "오늘" in text and "영단어" in text :
        return today_words()
    if "팝송" in text and "추천" in text :
        return recommend_popsong()
    if "빈출" in text and "영단어" in text :
        return saved_words()
    if "번역" in text :
        tr_flag = True
        return u"어떤말을 번역할까요?"
    if tr_flag :
        tr_flag = False
        return sentence_translation(text)
          
    return '무슨 말인지 모르겠어요'