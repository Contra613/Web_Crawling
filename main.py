# Naver
from News.naver_crawling import naver_crawling

# Google
from News.google_crawling import google_crawling

# GUI
import os
import tkinter as tk
from tkinter import ttk

from tkinter import filedialog as fd
from tkinter import messagebox

global bool
bool = False

class GUI():
    def __init__(self):
        self.win = tk.Tk()

        self.win.title("Project")
        self.win.resizable(False, False)

        self.create_widgets()

    def click_search(self):
        site = self.select_site.get()
        keyword = self.search_ward.get()
        count = self.search_count.get()

        if(bool == True):
            dir = self.file_dirName
        else:
            dir = os.getcwd()

        if(keyword == '' or count == 0):
            messagebox.showerror(title='Error', message="키워드와 개수를 다시 입력해주세요.")
            return

        if(site == 'Naver'):
            naver_crawling(keyword, count, self.progress, dir)
        elif(site == 'Google'):
            google_crawling(keyword, count, self.progress, dir)
        elif(site == 'All'):
            naver_crawling(keyword, count, self.progress, dir)
            google_crawling(keyword, count, self.progress, dir)

    def file_select(self):
        dirName = fd.askdirectory()
        self.directory.set(dirName)

        self.file_dirName = dirName.replace('/', '\\')
        global bool
        bool = True

    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    def create_widgets(self):
        tabControl = ttk.Notebook(self.win)  # Create Tab Control

        tab1 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(tab1, text='웹 크롤링')  # Add the tab
        tabControl.pack(expand=1, fill="both")  # Pack to make visible

        web = ttk.LabelFrame(tab1, text=' Web Crawling ')
        web.grid(column=0, row=0, pady=5, sticky=tk.N)

        # 검색어 입력
        search_ward_label = ttk.Label(web, text="검색어를 입력하세요")
        search_ward_label.grid(column=0, row=0, sticky=tk.W)

        self.search_ward = tk.StringVar()
        search_ward_entered = ttk.Entry(web, width=30, textvariable=self.search_ward)
        search_ward_entered.grid(column=0, row=1, padx=3, sticky=tk.W)

        # 불러올 뉴스 개수 입력
        search_count_label = ttk.Label(web, text="개수")
        search_count_label.grid(column=1, row=0, padx=3, sticky=tk.W)

        self.search_count = tk.IntVar()
        search_count_entered = ttk.Entry(web, width=5, textvariable=self.search_count)
        search_count_entered.grid(column=1, row=1, padx=3, sticky=tk.W)

        # 크롤링할 사이트 설정
        self.select_crawing = ttk.Label(web, text="사이트 선택")
        self.select_crawing.grid(column=2, row=0, padx=3, sticky=tk.W)

        self.select_site = ttk.Combobox(web, width=7 ,height=2, state='readonly')
        self.select_site['value'] = ('Naver', 'Google', 'All')
        self.select_site.current(0)
        self.select_site.grid(column=2, row=1, padx=3, sticky=tk.W)

        # Adding a Button
        self.search = ttk.Button(web, text="검색", command=self.click_search)
        self.search.grid(column=3, row=1, sticky=tk.W)


        #########################################################################################
        file = ttk.LabelFrame(tab1, text=' File ')
        file.grid(column=0, row=1, pady=8, sticky=tk.W)

        # Folder 선택
        file_select = ttk.Label(file, text="저장 위치")
        file_select.grid(column=0, row=0, sticky=tk.W)

        self.directory = tk.StringVar()
        self.directory_entered = ttk.Entry(file, width=48, textvariable=self.directory, state='readonly')
        self.directory_entered.grid(column=0, row=1, padx=5, sticky=tk.W)

        self.select = ttk.Button(file, text="찾아보기", command=self.file_select)
        self.select.grid(column=1, row=1, sticky=tk.W)

        self.progress = ttk.Label(file, text='')
        self.progress.grid(column=0, row=2, pady=10, sticky=tk.W)

# Start GUI
# ======================
gui = GUI()
gui.win.mainloop()