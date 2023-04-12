from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from threading import Thread
from yt_dlp import YoutubeDL


class DownloadWindow:
    def __init__(self, root, url):
        self.root = root
        self.url = url
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

    def start_download(self):
        self.thread = Thread(target=self.download_video)
        self.thread.start()

    def download_video(self):
        ydl_opts = {
            'format': 'best',
            'outtmpl': '~/Desktop/%(title)s.%(ext)s',
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


def download_video():
    url = entry.get()
    window = DownloadWindow(root, url)


root = Tk()
root.title("Youtube Video Downloader")
root.resizable(width=False, height=False)  # 幅と高さを固定
icon = PhotoImage(file="./icon.png")
root.iconphoto(False, icon)

label = Label(root, text="ダウンロードしたいYoutube動画のURLを入力してください")
label.pack()

entry = Entry(root, width=50)
entry.pack()

button = Button(root, text="Download", command=download_video)
button.pack()

root.geometry("400x80")

root.mainloop()
