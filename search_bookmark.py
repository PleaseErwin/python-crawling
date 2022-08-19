from timeit import repeat
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from fpdf import FPDF
import time
import pyautogui
import login_info
import re

options = webdriver.ChromeOptions()
# options.headless = True
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")

browser = webdriver.Chrome('C:/chromedriver.exe', options=options)
browser.get('https://hygall.com/')
browser.implicitly_wait(5)

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
# 로그인 후 세션 유지

keyword = pyautogui.prompt("키워드 입력")
page = pyautogui.prompt("페이지 수 입력")
print("keyword", keyword)

for index in page:
    response = session.get(f"https://hygall.com/index.php?mid=hy&act=dispMemberScrappedDocument&search_target=title_content&search_keyword={keyword}&page={index}", headers=nextHeader)
    
    # 북마크 페이지 하나
    html = response.text
    soup = BeautifulSoup(html, 'html.parser') # 'lxml'
    body = soup.find("tbody")
    fanfics = body.find_all("a", attrs={"class":"document_title"})

    for fanfic in fanfics:

        # pdf 파일 만들기
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('ArialUnicodeMS', '', 'C:/inflearn_2022/make_fanfics_pdf/Arial-Unicode-Regular.ttf', uni=True)
        pdf.set_font('ArialUnicodeMS', '', size=11)

        title = fanfic.text
        print(title)

        content = session.get(fanfic['href'], headers=nextHeader)
        content_html = content.text
        content_soup = BeautifulSoup(content_html, 'html.parser')
        content_head = content_soup.find("div", attrs={"class":"cntBody"})

        # pdf 내용 쓰기
        pdf.multi_cell(0, 10, txt = title, align = 'L')
        pdf.multi_cell(0, 10, txt = content_head.text, align = 'C')

        new_title = re.sub('[/:*?"<>\n\r\t]', "", title)
        file_path = f'C:/inflearn_2022/make_fanfics_pdf/fanfics/short/{new_title}'
        pdf.output(f"{file_path}.pdf", 'F')


# 오류
# OSError: [Errno 22] Invalid argument: 'C:/inflearn_2022/make_fanfics_pdf/fanfics/short/\r\n\t\t    \t\t\t
# >>> re.sub 정규식으로 제목에서 \n\r\t 제외해서 해결
# 해결했다고 생각했더니 pdf파일에 이상한 네모 특수문자 발견
