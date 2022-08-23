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

# 마이페이지 북마크
# browser.find_element_by_xpath('//*[@id="exheader"]/div[2]/a[1]').click()
# browser.find_element_by_xpath('//*[@id="memberModule"]/ul/li[4]/a').click()

# search = browser.find_element_by_name('search_keyword')
# search.click()
# search.send_keys('뱃슨뱃')
# search.send_keys(Keys.ENTER)
# browser.implicitly_wait(3)

# 이후 북마크된 글 가져오기
# browser.get_screenshot_as_file("a.png")

search = browser.find_element_by_xpath('//*[@id="exsearch"]/input[2]')
search.click()

for key in fanfic_list.keyword:
    # 검색창에 검색
    search.send_keys(key)
    search.send_keys(Keys.ENTER)
    time.sleep(3)

    # body에서 글 리스트 가져오기
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find("tbody")
    fanfics = body.find_all("a", attrs={"class":"exJsHotTrackA"})

    for fanfic in fanfics:
        content = requests.get(fanfic['href'], headers={"User-Agent": "Mozilla/5.0"})
        content_html = content.text
        print(fanfic.text)
        content_soup = BeautifulSoup(content_html, 'html.parser')
        content_head = content_soup.find("div", attrs={"class":"cntBody"})

        # pdf 파일 만들기
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('ArialUnicodeMS', '', 'C:/inflearn_2022/Arial-Unicode-Regular.ttf', uni=True)
        pdf.set_font('ArialUnicodeMS', '', size=15)
        pdf.multi_cell(0, 10, txt = fanfic.text, align = 'C')
        pdf.multi_cell(0, 10, txt = content_head.text, align = 'C')
    
    pdf.output(f"{key}.pdf", 'F')

    search.click()
    search.clear()


    

# fanfics = browser.find_elements(by=By.CSS_SELECTOR, value='.exJsHotTrackA')

# 셀레니움 이용
# 검색창에 검색어를 입력하고 tbody에서 글 리스트 가져오기를 반복해야 함
# 그러나 첫 번째 검색어에서 넘어가지 못함
# 브라우저를 종료하지 않았음에도 저절로 꺼짐
# 왜인지 pdf 파일에 내용이 전부 들어가지도 않음

