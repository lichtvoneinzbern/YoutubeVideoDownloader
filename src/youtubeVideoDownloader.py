from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
from yt_dlp import YoutubeDL
import os
import pyperclip

class DownloadWindow:
    def __init__(self, root, url, outDir):
        self.root = root
        self.url = url
        self.outDir = outDir
        self.should_stop = False
        self.create_window()

    def create_window(self):
        self.window = Toplevel(self.root)
        self.window.title("ダウンロード中...")
        self.window.resizable(width=False, height=False)
        icon = PhotoImage(file="./icon.png")
        self.window.iconphoto(False, icon)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.label = Label(self.window, text="ダウンロード中...")
        self.label.pack()

        self.progress_bar = ttk.Progressbar(
            self.window, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.pack()

        self.start_download()

        self.window.grab_set()

    # submethod
    def start_download(self):
        self.thread = Thread(target=self.download_video)
        self.thread.start()

    def download_video(self):
        ydl_opts = {
            'format': 'best',
            'outtmpl': self.outDir+'/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook]
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                if not self.should_stop:
                    self.on_complete()
        except Exception as e:
            if not self.should_stop:
                self.on_error(str(e))

    def progress_hook(self, d):
        if self.should_stop:
            raise Exception('Cancelled')
        if d['status'] == 'downloading':
            self.progress_bar.configure(
                value=d['downloaded_bytes'] * 100. / d['total_bytes'])
        elif d['status'] == 'finished':
            pass

    def on_complete(self):
        self.progress_bar.configure(value=100)

        messagebox.showinfo("Complete!!!", "ダウンロードが完了しました！")
        self.window.after(100, self.window.destroy)

    def on_error(self, message):
        messagebox.showerror(
            "エラー", f"エラーが発生しました。\nURLが正しいか確認してください！\n{message}")
        self.window.destroy()

    def on_cancel(self):
        self.should_stop = True

    def on_close(self):
        self.should_stop = True
        self.window.destroy()

class InputWindow:
    def __init__(self):
        self.desktopPath = os.path.join(os.path.expanduser("~"), "Desktop")
        self.outDir = ""

    def createWindow(self):
        self.root = Tk()
        self.root.title("Youtube Video Downloader")
        self.root.resizable(width=False, height=False)  # 幅と高さを固定
        icon = PhotoImage(file="./icon.png")
        self.root.iconphoto(False, icon)

        # Output dir
        self.dirFrame = Frame(self.root)
        self.dirFrame.pack(side=TOP, anchor="w", pady=(5, 0))

        self.outDirLabel = Label(self.dirFrame, text="保存場所")
        self.outDirLabel.pack(side=LEFT)

        self.outDirTextbox = Text(self.dirFrame, height=1, width=50)
        self.outDirTextbox.insert("1.0", self.desktopPath)
        self.outDirTextbox.pack(side=LEFT)

        self.selectDirButton = Button(
            self.dirFrame, text="選択", command=self.select_dir)
        self.selectDirButton.pack(side=RIGHT, padx=(5, 0))

        # URL
        self.urlFrame = Frame(self.root)
        self.urlFrame.pack(side=TOP, anchor="w", padx=(2, 0), pady=(5, 0))

        self.entryLabel = Label(self.urlFrame, text="動画URL")
        self.entryLabel.pack(side=LEFT)

        self.entry = Entry(self.urlFrame, width=58)
        self.entry.pack(side=LEFT)

        self.pasteButton = Button(
            self.urlFrame, text="貼り付け", command=self.paste_from_clipboard)

        self.pasteButton.pack(side=LEFT, padx=(5, 0))

        self.button = Button(self.root, text="ダウンロード",
                             command=self.download_video, width=20, height=2)
        self.button.pack(pady=(10, 0))

        self.root.geometry("500x120")

        self.root.mainloop()

    # submethod
    def download_video(self):
        self.url = self.entry.get()
        self.outDir = self.outDirTextbox.get(1.0, "end-1c")
        self.window = DownloadWindow(self.root, self.url, self.outDir)

    def select_dir(self):
        self.outDir = filedialog.askdirectory()
        self.outDirTextbox.delete(1.0, END)
        self.outDirTextbox.insert(END, self.outDir)

    def paste_from_clipboard(self):
        text = pyperclip.paste()
        self.entry.delete(0, END)
        self.entry.insert(END, text)


inputWindowIns = InputWindow()
inputWindowIns.createWindow()
