# import
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver                          # selenium version = 3.14.1
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests
from datetime import datetime


from tkinter import messagebox

def google_crawling(ward, count, status, dir, version):
    date = str(datetime.now())
    date = date[:date.rfind(':')].replace(' ', '_')
    date = date.replace(':', '시') + '분'

    keywords = ward

    # Chrome Driver Version Check
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')

        driver = webdriver.Chrome(executable_path=f'Chrome/{version}.exe', chrome_options=options)
        driver.get('https://news.google.com/?hl=ko&gl=KR&ceid=KR%3Ako')
        driver.implicitly_wait(3)
    except:
        messagebox.showerror(title='Error', message="Chrome Version을 확인 후 Driver을 다시 설정해주세요.")
        return


    search = driver.find_element_by_xpath(
        '//*[@id="gb"]/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[1]/input[2]')

    search.send_keys(keywords)
    search.send_keys(Keys.ENTER)
    driver.implicitly_wait(10)

    url = driver.current_url

    resp = requests.get(url)
    soup = bs(resp.text, 'lxml')

    titles = []
    links = []
    news_cnt = 0

    for link in soup.select('h3 > a'):
        if(count > news_cnt):
            href = 'https://news.google.com' + link.get('href')[1:]
            title = link.string
            titles.append(title)
            links.append(href)
            news_cnt = news_cnt + 1
        else:
            break

    data = {'title': titles, 'link': links}
    data_frame = pd.DataFrame(data, columns=['title', 'link'])

    folder_path = dir
    xlsx_file_name = '구글 뉴스_{}_{}.xlsx'.format(keywords, date)
    data_frame.to_excel(excel_writer=folder_path + '\\' + xlsx_file_name)

    status.configure(text='크롤링 저장 완료' + '\n경로 : ' + folder_path + '\n파일 이름 : ' + xlsx_file_name)
    driver.close()
    os.startfile(folder_path)
