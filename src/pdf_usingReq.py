from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from fpdf import FPDF
import time
import fanfic_list
import login_info
# cls 터미널 비우기

LOGIN_URL = 'https://hygall.com/index.php'
LOGIN_DATA = {
    'uid': login_info.id,
    'upw': login_info.password
}

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    'referer':'https://hygall.com/index.php?mid=hy&act=dispMemberLoginForm'
}
 
data = {
    'uid': 'erwin',
    'upw': 'please'
}

nextHeader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    # 'referer':'https://hygall.com/',
    # 'PHPSESSID':''
}

session = requests.Session()

# with requests.Session() as s:
    # res = session.post(LOGIN_URL, data=data, headers=header) # verify=True
    # res.raise_for_status() #오류 발생하면 예외 발생
    # print("test", session.cookies.get_dict())

    # for key in keyword:
    #     response = session.get(f"https://hygall.com/?mid=hy&search_target=title_content&search_keyword={key}", headers={"User-Agent": "Mozilla/5.0"})
    #     html = response.text
    #     soup = BeautifulSoup(html, 'html.parser') # 'lxml'
    #     body = soup.find("tbody")
    #     fanfics = body.find_all("a", attrs={"class":"exJsHotTrackA"})

    #     # pdf 파일 만들기
    #     pdf = FPDF()
    #     pdf.add_page()
    #     pdf.add_font('ArialUnicodeMS', '', 'C:/inflearn_2022/Arial-Unicode-Regular.ttf', uni=True)
    #     pdf.set_font('ArialUnicodeMS', '', size=11)

    #     for fanfic in fanfics:
    #         title = fanfic.text
    #         if "축제 [아매별추] 정리글" in title:
    #             continue
    #         print(title)
    #         content = session.get(fanfic['href'], headers={"User-Agent": "Mozilla/5.0"})
    #         content_html = content.text
    #         content_soup = BeautifulSoup(content_html, 'html.parser')
    #         content_head = content_soup.find("div", attrs={"class":"cntBody"})

    #         # pdf 내용 쓰기
    #         pdf.multi_cell(0, 10, txt = title, align = 'L')
    #         pdf.multi_cell(0, 10, txt = content_head.text, align = 'C')

    #     pdf.output(f"{key}.pdf", 'F')


res = session.post(LOGIN_URL, data=data, headers=header) # verify=True
res.raise_for_status() #오류 발생하면 예외 발생
# print("test ", session.cookies.get_dict()) # {'PHPSESSID': 'tuajkui28104q8ben6ucr0pqm2'}
# sessID = session.cookies.get_dict()
# nextHeader['PHPSESSID'] = sessID['PHPSESSID']

for key in fanfic_list.keyword:
    response = session.get(f"https://hygall.com/?mid=hy&search_target=title_content&search_keyword={key}", headers=nextHeader)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser') # 'lxml'
    body = soup.find("tbody")
    fanfics = body.find_all("a", attrs={"class":"exJsHotTrackA"})

    # pdf 파일 만들기
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('ArialUnicodeMS', '', 'C:/inflearn_2022/Arial-Unicode-Regular.ttf', uni=True)
    pdf.set_font('ArialUnicodeMS', '', size=11)

    for fanfic in fanfics:
        title = fanfic.text
        if "축제 [아매별추] 정리글" in title:
            continue
        print(title)
        content = session.get(fanfic['href'], headers=nextHeader)
        content_html = content.text
        content_soup = BeautifulSoup(content_html, 'html.parser')
        content_head = content_soup.find("div", attrs={"class":"cntBody"})

        # pdf 내용 쓰기
        pdf.multi_cell(0, 10, txt = title, align = 'L')
        pdf.multi_cell(0, 10, txt = content_head.text, align = 'C')

    pdf.output(f"{key}.pdf", 'F')


# 처음 세션을 만들고 POST로 로그인했을 때는 성인글이 정상적으로 보임
# 그러나 해당 추후 GET에서 세션 유지가 안 됨