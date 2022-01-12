from tkinter import Tk, Label, Entry, messagebox, Button,Scrollbar, Text
from tkinter.constants import CENTER, LEFT, RIGHT, TOP, X, Y
from pytube import YouTube, Playlist
from PIL import ImageTk
from urllib.request import urlopen
from pathlib import Path
import os

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Youtube Downloader")
        self.geometry("600x650")
        self.download_path = str(Path.home() / "Downloads")

        def check_url():
            try:    
                url = self.entry_url.get()
                if url.find('playlist') == -1:
                    yt = YouTube(url)
                    video(self, yt)
                else:
                    yt = Playlist(url)
                    playlist(self, yt)
                index_end()
            except: 
                messagebox.showerror("Error", "Invalid Url")

        def onCreate():
            self.h1 = Label(self, text='Input Your Url', font='Helvetica 18 bold', width=45, height=4)
            self.entry_url = Entry(self, width="80")
            self.line = Label(self, text='', height=2)
            self.btn_check = Button(self, text=" Check ", font='Helvetica 10 bold', command=check_url)

        # Index
        def index_start():
            onCreate()
            self.h1.pack()
            self.entry_url.pack()
            self.line.pack()
            self.btn_check.pack()

        def index_end():
            self.h1.pack_forget()
            self.entry_url.pack_forget()
            self.line.pack_forget()
            self.btn_check.pack_forget()

        # Download Page
        def file(self, video):
            u = urlopen(video.thumbnail_url)
            raw_data = u.read()
            u.close()
            
            photo = ImageTk.PhotoImage(data=raw_data)
            thumnail = Label(image=photo)

            thumnail.image = photo
            title = Label(self, text=video.title, font='Helvetica 10 bold')
            mp3_btn = Button(self, text="mp3", font='Helvetica 10 bold', command= lambda: mp3(self, video))
            mp4_btn = Button(self, text="mp4", font='Helvetica 10 bold', command= lambda: mp4(self, video))
            line1 = Label(self, text="=========================================================")
            line2 = Label(self, text="---------------------------------------------------------")

            line1.pack()
            thumnail.pack()
            title.pack()
            mp3_btn.pack()
            mp4_btn.pack()
            line2.pack()

            
        def mp3(self, video):
            try:
                video = video.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=self.download_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                messagebox.showinfo("Success", "Complete get mp3 file")
            except:
                messagebox.showerror("Error", "file already exist")

        def mp4(self, video):
            try:
                d_video = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                d_video.download(output_path=self.download_path)
                messagebox.showinfo("Success", "Complete get mp4 file")
            except:
                messagebox.showerror("Error", "File already exist")

        def clear(self):
            for widget in self.winfo_children():
                widget.destroy()
            
            index_start()

        def video(self, yt):
            file(self, yt)

            index_btn = Button(self, text="Back to Index", font='Helvetica 10 bold', command= lambda: clear(self))
            index_btn.pack(fill=X)

        def playlist(self, yt):
            text = Text(self, wrap="none")
            vsb = Scrollbar(orient="vertical", command=text.yview)
            text.configure(yscrollcommand=vsb.set)
            vsb.pack(side="right", fill="y")
            text.pack(fill="both", expand=True)
            
            for video in yt.videos:
                title = Label(self, text=video.title, font='Helvetica 10 bold')
                mp3_btn = Button(self, text="mp3", font='Helvetica 10 bold', command= lambda: mp3(self, video))
                mp4_btn = Button(self, text="mp4", font='Helvetica 10 bold', command= lambda: mp4(self, video))

                text.window_create("end", window=title)
                text.window_create("end", window=mp3_btn)
                text.window_create("end", window=mp4_btn)
                text.insert("end", "\n")

            index_btn = Button(self, text="Back to Index", font='Helvetica 10 bold', command= lambda: clear(self))
            index_btn.pack(fill=X)
            text.configure(state="disabled")

        index_start()
            



if __name__ == "__main__":

    app = App()
    app.mainloop()