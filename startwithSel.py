from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from fpdf import FPDF
import time
import fanfic_list
import login_info

options = webdriver.ChromeOptions()
# options.headless = True
# options.add_argument("window-size=1920X1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")

browser = webdriver.Chrome('C:/chromedriver.exe', options=options)
# browser.maximize_window()
browser.get('https://hygall.com/') # 웹사이트 열기
browser.implicitly_wait(5) # 로딩이 끝날 때까지 5초까지는 기다려 줌

# 로그인
browser.find_element_by_xpath('//*[@id="gnb"]/ul/li[13]/a').click()
id = browser.find_element_by_css_selector('input#uid')
id.click()
id.send_keys(login_info.id)
password = browser.find_element_by_css_selector('input#upw')
password.click()
password.send_keys(login_info.password)
time.sleep(2)
browser.find_element_by_xpath('//*[@id="fo_member_login"]/fieldset/center/input[3]').click()
browser.implicitly_wait(3)
# 로그인 완료

cookies = browser.get_cookies()
cookie_dict = {}
for cookie in cookies:
    cookie_dict[cookie['name']] = cookie['value']

# print(cookie_dict)
browser.quit()

session = requests.Session()

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    'referer':'https://hygall.com/index.php?mid=hy&act=dispMemberLoginForm'
}
nextHeader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}

session.headers.update(header)
session.cookies.update(cookie_dict)

for key in fanfic_list.keyword:
    response = session.get(f"https://hygall.com/?mid=hy&search_target=title_content&search_keyword={key}", headers=nextHeader)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser') # 'lxml'
    body = soup.find("tbody")
    fanfics = body.find_all("a", attrs={"class":"exJsHotTrackA"})

    fanfics.reverse()

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

    new_title = key.replace('-중장', '')
    pdf.output(f"{new_title}.pdf", 'F')

# 최종본
# 셀레니움으로 시작해서 로그인
# 로그인 상태의 쿠키를 가져와서 저장
# 세션을 생성하고 헤더와 쿠키 정보 업데이트
# pdf 파일 만들기 반복

# * referer 설정하지 않으면 성인글 안보임
# * 첫 페이지 글밖에 가져오지 못함

# 오류
# OSError: [Errno 22] Invalid argument: '아이스매브가 탑-건 이전에 이미 정략결혼한 사이라면??.pdf' 오류
# >>> 저장 경로나 파일명에 사용할 수 없는 특수문자를 사용했기 때문에 발생

# in _putTTfontwidths - if (font['cw'][cid] == 0):IndexError: list index out of range
# >>> fpdf can't ignore characters which can't print / 같은 오류를 겪는 사람들 발견