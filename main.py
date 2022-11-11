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
from Util.ToolTip import ToolTip

# Save Path Select Check
global bool
bool = False

class GUI():
    def __init__(self):
        self.win = tk.Tk()

        self.win.title("뉴스 크롤링")
        self.win.resizable(False, False)

        self.create_widgets()

    def click_search(self):
        site = self.select_site.get()
        keyword = self.search_ward.get()
        count = self.search_count.get()
        version = self.version.get()

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
            google_crawling(keyword, count, self.progress, dir, version)
        elif(site == 'All'):
            naver_crawling(keyword, count, self.progress, dir)
            google_crawling(keyword, count, self.progress, dir, version)

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
        tabControl = ttk.Notebook(self.win)

        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='웹 크롤링')

        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='설정 및 도움말')

        tabControl.pack(expand=1, fill="both")

        web = ttk.LabelFrame(tab1, text=' Web Crawling ')
        web.grid(column=0, row=0, pady=5, sticky=tk.N)

        # Keyward
        search_ward_label = ttk.Label(web, text="검색어를 입력하세요")
        search_ward_label.grid(column=0, row=0, sticky=tk.W)

        self.search_ward = tk.StringVar()
        search_ward_entered = ttk.Entry(web, width=30, textvariable=self.search_ward)
        search_ward_entered.grid(column=0, row=1, padx=3, sticky=tk.W)

        # Count
        search_count_label = ttk.Label(web, text="개수")
        search_count_label.grid(column=1, row=0, padx=3, sticky=tk.W)

        self.search_count = tk.IntVar()
        search_count_entered = ttk.Entry(web, width=5, textvariable=self.search_count)
        search_count_entered.grid(column=1, row=1, padx=3, sticky=tk.W)

        # Site
        self.select_crawing = ttk.Label(web, text="사이트 선택")
        self.select_crawing.grid(column=2, row=0, padx=3, sticky=tk.W)

        self.select_site = ttk.Combobox(web, width=7 ,height=2, state='readonly')
        self.select_site['value'] = ('Naver', 'Google', 'All')
        self.select_site.current(0)
        self.select_site.grid(column=2, row=1, padx=3, sticky=tk.W)

        self.search = ttk.Button(web, text="검색", command=self.click_search)
        self.search.grid(column=3, row=1, sticky=tk.W)

        # --------------------------------------------------------------------------------------------------------
        file = ttk.LabelFrame(tab1, text=' Save ')
        file.grid(column=0, row=2, pady=8, sticky=tk.W)

        # Folder Select
        self.file_select = ttk.Label(file, text="저장 위치")
        self.file_select.grid(column=0, row=0, sticky=tk.W)

        self.directory = tk.StringVar()
        self.directory_entered = ttk.Entry(file, width=48, textvariable=self.directory, state='readonly')
        self.directory_entered.grid(column=0, row=1, padx=5, sticky=tk.W)

        self.select = ttk.Button(file, text="찾아보기", command=self.file_select)
        self.select.grid(column=1, row=1, sticky=tk.W)

        self.progress = ttk.Label(file, text='')
        self.progress.grid(column=0, row=2, pady=5, sticky=tk.W)

        # --------------------------------------------------------------------------------------------------------
        setting = ttk.LabelFrame(tab2, text=' Chrome Version Setting ')
        setting.grid(column=0, row=0, pady=5, sticky=tk.W)

        # Chrome Version Select
        self.version = tk.IntVar(value=107)

        self.radio1 = ttk.Radiobutton(setting, text='108', variable=self.version, value=108)
        self.radio1.grid(column=0, row=0, padx=10, sticky=tk.W)

        self.radio2 = ttk.Radiobutton(setting, text='107', variable=self.version, value=107)
        self.radio2.grid(column=1, row=0, padx=10, sticky=tk.W)

        self.radio3 = ttk.Radiobutton(setting, text='106', variable=self.version, value=106)
        self.radio3.grid(column=2, row=0, padx=10, sticky=tk.W)

        # Help
        help = ttk.LabelFrame(tab2, text=' 도움말')
        help.grid(column=0, row=1, pady=5, sticky=tk.W)

        self.use = tk.Text(help, width=54, height=8, font=('맑은 고딕', 11, ''))
        self.use.config(state="normal")
        self.use.insert(tk.END,
                        "[사용 방법]\n키워드, 뉴스 개수, 뉴스 사이트를 선택 후 검색 버튼을 누르면 검색 결과가 "
                        "기본적으로 현제 프로젝트 파일 경로에 엑셀 파일로 저장된다. \n\n엑셀 파일의 저장 위치는 지정할 수 있다.\n\n"
                        "[주의 사항]\n사이트를 Google로 선택 시 Chrome -> 도움말 -> Chrome Version을 확인하여 위의 Chrome Version"
                        "을 선택한다.\n"
                        )
        self.use.config(state="disabled")
        self.use.grid(column=0, row=0)

        # --------------------------------------------------------------------------------------------------------
        # ToolTip
        ToolTip(self.select_crawing, "Default Chrome Driver version = 107")
        ToolTip(self.file_select, "Default Save Path : 현제 프로젝트 파일")

        # Icon
        self.win.iconbitmap('Util/news.ico')

# Start GUI
start = GUI()
start.win.mainloop()