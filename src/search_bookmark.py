from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from fpdf import FPDF
import time
import pyautogui
import login_info
import address
import re

options = webdriver.ChromeOptions()
# options.headless = True
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")

browser = webdriver.Chrome('C:/chromedriver.exe', options=options)
browser.get(address.main)
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
    'referer': address.login_referer
}
nextHeader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}

session.headers.update(header)
session.cookies.update(cookie_dict)
# 로그인 후 세션 유지

keyword = pyautogui.prompt("키워드 입력")
start_page = int(pyautogui.prompt("시작 페이지 수 입력"))
end_page = int(pyautogui.prompt("끝 페이지 수 입력"))

# 오류난 fanfic 제목을 저장하는 파일
f = open('../error.txt', 'a', encoding='utf-8', newline='')# 기존에 있던 내용에 이어서 쓰는 옵션 a

for index in range(start_page, end_page + 1):
    response = session.get(address.bookmark_search(keyword, index), headers=nextHeader)
    
    # 북마크 페이지 하나
    html = response.text
    soup = BeautifulSoup(html, 'html.parser') # 'lxml'
    body = soup.find("tbody")
    fanfics = body.find_all("a", attrs={"class":"document_title"})

    for fanfic in fanfics:
        try:
            # pdf 파일 만들기
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font('ArialUnicodeMS', '', '../font/Arial-Unicode-Regular.ttf', uni=True)
            pdf.set_font('ArialUnicodeMS', '', size=11)

            title = fanfic.text
            print(title)

            content = session.get(fanfic['href'], headers=nextHeader)
            content_html = content.text
            content_soup = BeautifulSoup(content_html, 'html.parser')
            content_head = content_soup.find("div", attrs={"class":"cntBody"})

            sliced_title = title.partition('-')[0]
            new_title = re.sub('[/:*?"<>\n\r\t]', "", sliced_title)
            # pdf 내용 쓰기
            pdf.multi_cell(0, 10, txt = new_title, align = 'L')
            pdf.multi_cell(0, 10, txt = content_head.text, align = 'L')

            file_path = f'../fanfics/short/{new_title}'
            pdf.output(f"{file_path}.pdf", 'F')
        except IndexError:# 범위를 벗어난 인덱스에 접근하여 에러가 발생했을 때 실행됨
            f.write(new_title)


# 오류
# OSError: [Errno 22] Invalid argument: 'C:/inflearn_2022/make_fanfics_pdf/fanfics/short/\r\n\t\t    \t\t\t
# >>> re.sub 정규식으로 제목에서 \n\r\t 제외해서 해결
# 해결했다고 생각했더니 pdf파일에 이상한 네모 특수문자 발견
# >>> 정규식으로 특수문자를 제외한 new_title을 파일 이름뿐만이 아니라 pdf에도 적용해서 문제 해결

# IndexError: list index out of range
# 🧊🐿 같은 아이콘 때문에 그런 것으로 보임
# >>> try except로 예외 처리하고 error.txt에 오류난 fanfic 제목들을 써서 추후 따로 pdf화하는 것으로 해결

# 페이지가 제대로 넘어가지 않는 오류
# pyautogui로 입력한 숫자가 string이므로 int로 변환해서 해결

# error.txt 파일이 초기화됨
# open 함수의 옵션을 w에서 a로 바꾸는 것으로 해결