# import
import requests                     # 웹페이지 소스 추출
from pandas import DataFrame        # 데이터 프레임, 엑셀 변환
from bs4 import BeautifulSoup       # HTML 파싱, 필요 태그 및 소스 추출
import re                           # 조건부 문자열(정규 표현식), 태그 탐색 시 일반화 조건을 사용하는 용도
from datetime import datetime
import os


def naver_crawling(ward, count, status):
    date = str(datetime.now())  # 데이터 저장 시간
    date = date[:date.rfind(':')].replace(' ', '_')
    date = date.replace(':', '시') + '분'

    query = ward  # 검색어 입력
    news_num = count  # 뉴스 개수 입력
    query = query.replace(' ', '+')  # ' '을 +로 바꾸는 이뉴 -> 띄어쓰기 시 URL 조건 절에서 '+'로 적용되어 요청 인자가 들어가기 때문이다.

    news_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'

    req = requests.get(news_url.format(query))  # requests의 패키지의 get 함수를 이용하여 HTML 코드를 받아온다.
    soup = BeautifulSoup(req.text, 'html.parser')  # 받아온 코드를 BeautifulSoup에 파싱

    news_dict = {}
    idx = 0
    cur_page = 1

    print()
    print('크롤링 중...')

    while idx < news_num:
        table = soup.find('ul', {'class': 'list_news'})
        li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
        area_list = [li.find('div', {'class': 'news_area'}) for li in li_list]
        a_list = [area.find('a', {'class': 'news_tit'}) for area in area_list]

        for n in a_list[:min(len(a_list), news_num - idx)]:
            news_dict[idx] = {'title': n.get('title'),
                              'url': n.get('href')}
            idx += 1

        cur_page += 1

        pages = soup.find('div', {'class' : 'sc_page_inner'})
        next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page)][0].get('href')

        req = requests.get('https://search.naver.com/search.naver' + next_page_url)
        soup = BeautifulSoup(req.text, 'html.parser')

    print('크롤링 완료')

    print('데이터프레임 변환')
    news_df = DataFrame(news_dict).T

    folder_path = os.getcwd()  # 작업 경로 반환 folder_path
    xlsx_file_name = '네이버뉴스_{}_{}.xlsx'.format(query, date)

    news_df.to_excel(excel_writer=folder_path + '\\' + xlsx_file_name)

    # Excel 파일 저장
    print('엑셀 저장 완료 | 경로 : {}\\{}'.format(folder_path, xlsx_file_name))
    status.configure(text='크롤링 저장 완료' + '\n경로 : ' + folder_path + '\n파일 이름 : ' + xlsx_file_name)
    os.startfile(folder_path)  # 폴더 열기