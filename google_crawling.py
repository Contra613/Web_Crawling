# import
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests
from datetime import datetime

def google_crawling(ward, status):
    date = str(datetime.now())  # 데이터 저장 시간
    date = date[:date.rfind(':')].replace(' ', '_')
    date = date.replace(':', '시') + '분'

    # 검색어 입력
    keywords = ward

    # 웹드라이버 호출
    driver = webdriver.Chrome(r'C:\Users\kmg87\PycharmProjects\Project\Chrome\chromedriver.exe')
    driver.get('https://news.google.com/?hl=ko&gl=KR&ceid=KR%3Ako')
    driver.implicitly_wait(3)

    # driver.implicitly_wait()와 time.sleep()은 약간의 차이가 있다.
    # time.sleep() : 무조건 정해진 시간만큼 대기
    # driver.implicitly_wait() : 브라우저에서 사용되는 시간만큼 대기하다가 그 사이에 파싱되면 다음 단계로 진행

    # Google News 검색창 Xpath
    search = driver.find_element_by_xpath(
        '//*[@id="gb"]/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[1]/input[2]')

    # 검색어 입력 및 실행
    search.send_keys(keywords)
    search.send_keys(Keys.ENTER)
    driver.implicitly_wait(10)

    # 현재 주소 가져오기
    url = driver.current_url

    # 현재 주소로부터 'lxml' 파싱
    resp = requests.get(url)
    soup = bs(resp.text, 'lxml')

    # 제목, 주소의 빈 리스트 자료형 만들기
    titles = []
    links = []

    # `lxml` 파싱한 결과물에서 제목과 링크 추출 후 데이터로 저장
    for link in soup.select('h3 > a'):
        href = 'https://news.google.com' + link.get('href')[1:]
        title = link.string
        titles.append(title)
        links.append(href)

    data = {'title': titles, 'link': links}
    data_frame = pd.DataFrame(data, columns=['title', 'link'])

    folder_path = os.getcwd()  # 작업 경로 반환 folder_path
    xlsx_file_name = '구글 뉴스_{}_{}.xlsx'.format(keywords, date)
    data_frame.to_excel(excel_writer=folder_path + '\\' + xlsx_file_name)

    status.configure(text='크롤링 저장 완료' + '\n경로 : ' + folder_path + '\n파일 이름 : ' + xlsx_file_name)
    driver.close()
    os.startfile(folder_path)  # 폴더 열기

# date = str(datetime.now())  # 데이터 저장 시간
# date = date[:date.rfind(':')].replace(' ', '_')
# date = date.replace(':', '시') + '분'
#
# # 검색어 입력
# keywords = input('Search keyword: ')
#
# # 웹드라이버 호출
# driver = webdriver.Chrome(r'C:\Users\kmg87\PycharmProjects\Project\Chrome\chromedriver.exe')
# driver.get('https://news.google.com/?hl=ko&gl=KR&ceid=KR%3Ako')
# driver.implicitly_wait(3)
#
# # driver.implicitly_wait()와 time.sleep()은 약간의 차이가 있다.
# # time.sleep() : 무조건 정해진 시간만큼 대기
# # driver.implicitly_wait() : 브라우저에서 사용되는 시간만큼 대기하다가 그 사이에 파싱되면 다음 단계로 진행
#
# # Google News 검색창 Xpath
# search = driver.find_element_by_xpath(
#     '//*[@id="gb"]/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[1]/input[2]')
#
# # 검색어 입력 및 실행
# search.send_keys(keywords)
# search.send_keys(Keys.ENTER)
# driver.implicitly_wait(10)
#
# # 현재 주소 가져오기
# url = driver.current_url
#
# # 현재 주소로부터 'lxml' 파싱
# resp = requests.get(url)
# soup = bs(resp.text, 'lxml')
#
# # 제목, 주소의 빈 리스트 자료형 만들기
# titles = []
# links = []
#
# # `lxml` 파싱한 결과물에서 제목과 링크 추출 후 데이터로 저장
# for link in soup.select('h3 > a'):
#     href = 'https://news.google.com' + link.get('href')[1:]
#     title = link.string
#     titles.append(title)
#     links.append(href)
#
# # xlsx_file_name = '네이버뉴스_{}_{}.xlsx'.format(query, date)
# # news_df.to_excel(excel_writer=folder_path + '\\' + xlsx_file_name)
#
# data = {'title': titles, 'link': links}
# data_frame = pd.DataFrame(data, columns=['title', 'link'])
#
# folder_path = os.getcwd()  # 작업 경로 반환 folder_path
# xlsx_file_name = '구글 뉴스_{}_{}.xlsx'.format(keywords, date)
# #data_frame.to_excel('./' + keywords + date + '.xlsx')
# data_frame.to_excel(excel_writer=folder_path + '\\' + xlsx_file_name)
#
# print("Complete!")
#
# driver.close()
# os.startfile(folder_path)  # 폴더 열기