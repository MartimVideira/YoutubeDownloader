from time import sleep
import tkinter as tk
import tkinter.font as font
from youtube import Youtube
from tkinter import filedialog


class YoutubeApp:
    def __init__(self):
        self.main_window = self.menu_window()
        # self.current_window.mainloop()

        self.youtube_browser = Youtube()
        self.path_var_tk = tk.StringVar()
        self.path_var_tk.set(self.youtube_browser.get_download_path())

    def start(self):
        self.main_window.mainloop()

    def hide_main_window(self):
        self.main_window.withdraw()

    def show_main_window(self):
        self.main_window.deiconify()

    def open_by_youtube(self):
        self.hide_main_window()
        self.youtube_window()

    def open_by_link(self):
        self.hide_main_window()
        self.link_download_window()

    def get_new_path(self):
        # Browses for a new path for the download and updates  the tk_var and yt browser
        selected_folder = filedialog.askdirectory()
        self.youtube_browser.set_download_path(selected_folder)
        self.path_var_tk.set(selected_folder)

    def download_mp3(self, link=None):
        self.youtube_browser.download_mp3(link)

    def download_video(self, link=None):
        self.youtube_browser.download_video(link)

    def menu_window(self):
        root = tk.Tk()
        root.title('Youtube Downloader')
        root.resizable(False, False)

        my_Font = font.Font(family='Courier', size=15, weight='bold')

        canvas = tk.Canvas(root, width=500, height=200)
        canvas.grid(columnspan=2, rowspan=1)

        button_open_youtube = tk.Button(root, text='Open Youtube', bg="#FF0000",
                                        fg='white', height=10, width=20, font=my_Font, command=self.open_by_youtube)
        button_open_youtube.grid(column=0, row=0)

        button_download_link = tk.Button(root, text="Download From Link",
                                         bg="#D6B417", fg='white', height=10, width=20, font=my_Font, command=self.open_by_link)
        button_download_link.grid(column=1, row=0)

        return root

    def download_buttons_frame(self, window, mp3_button_command, video_button_command):
        # Returns the frame with the mp3 download button and the video download button
        download_buttons_frame = tk.Frame(window)

        download_mp3_button = tk.Button(download_buttons_frame, text='MP3', bg="#FF0000",
                                        fg='white', height=6, width=41, command=mp3_button_command)
        download_mp3_button.grid(
            column=0, row=0, sticky="swen", padx=1)

        download_video_button = tk.Button(download_buttons_frame, text="Video",
                                          bg="#D6B417", fg='white', height=6, width=41, command=video_button_command)
        download_video_button.grid(
            column=1, row=0, sticky="swen")

        return download_buttons_frame

    def download_path_frame(self, window):
        # Labels and a button that show the download path and allow to change it
        download_path_frame = tk.Frame(window)

        download_path_label = tk.Label(
            download_path_frame, text='Download Path:')
        download_path_label.grid(column=0, row=0, sticky="e",)

        show_download_path = tk.Label(
            download_path_frame, width=60, anchor='w', relief=tk.SUNKEN, textvariable=self.path_var_tk)
        show_download_path.grid(column=1, row=0, sticky="w")

        set_path_button = tk.Button(
            download_path_frame, text='Set New Path', command=self.get_new_path)
        set_path_button.grid(column=2, row=0, sticky='nswe', padx=0)

        return download_path_frame

    def youtube_window(self):
        # Initializing the window controlls
        youtube_window = tk.Toplevel(self.main_window)
        youtube_window.resizable(False, False)

        # Opening the broser
        self.youtube_browser.open_browser()

        # Labels and button to show and set the download Path
        download_path_frame = self.download_path_frame(youtube_window)
        download_path_frame.grid(column=0, row=0, columnspan=3)

        # Download Buttons -> estão num frame para melhor organizar senao ficava feio
        download_buttons_frame = self.download_buttons_frame(
            youtube_window, self.download_mp3, self.download_video)
        download_buttons_frame.grid(
            column=0, row=1, columnspan=3, pady=4, padx=1)

        # Dont really know where this function should go but it handles the closing of the youtube_window
        def on_closing():
            youtube_window.destroy()
            self.youtube_browser.close_browser()
            self.show_main_window()
        # We pass that functio to the window
        youtube_window.protocol("WM_DELETE_WINDOW", on_closing)
        # Setting the mainloop
        youtube_window.mainloop()

    def link_download_window(self):
        link_download_window = tk.Toplevel(self.main_window)
        link_download_window.resizable(False, False)

        download_path_frame = self.download_path_frame(link_download_window)
        download_path_frame.grid(column=0, row=0, columnspan=3, pady=2, padx=2)

        insert_link_label = tk.Label(
            link_download_window, text="Insert Link:", anchor='w')
        insert_link_label.grid(column=0, row=1, sticky='e')

        link_var = tk.StringVar()
        insert_link_entry = tk.Entry(
            link_download_window, textvariable=link_var, width=70)
        insert_link_entry.grid(column=1, row=1, sticky="we")

        # Button functions:
        def mp3_link_download(): return self.download_mp3(link_var.get())
        def video_link_download(): return self.download_video(link_var.get())

        download_buttons_frame = self.download_buttons_frame(
            link_download_window, mp3_link_download, video_link_download)

        download_buttons_frame.grid(column=0, row=2, columnspan=2, pady=1)

        def on_closing():
            link_download_window.destroy()
            self.main_window.deiconify()

        link_download_window.protocol('WM_DELETE_WINDOW', on_closing)
        link_download_window.mainloop()


youtube_app = YoutubeApp()
youtube_app.start()
