from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import youtube_dl
from pytube import YouTube
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os



class Youtube:
    LINK = "https://www.youtube.com/"
    DOWNLOAD_DIR_NAME = "Downloads"

    def __init__(self):
        self.download_path = None
        self.driver =  None
    def open_browser(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(Youtube.LINK)
        self.driver.maximize_window()
        # Handeling Coookies
        self.driver.implicitly_wait(4)
        #wait = WebDriverWait(self.driver,10)
        #cookies = wait.until(EC.element_to_be_clickable((By.XPATH,"//ytd-button-renderer[2]/a/tp-yt-paper-button")))
        #cookies.click()

    def create_download_folder(self):
        #Setting the path
        if self.download_path is None:
            working_dir = os.path.abspath(os.getcwd())
            self.download_path = os.path.join(working_dir,Youtube.DOWNLOAD_DIR_NAME)
        #Creating the directory
        if not os.path.isdir(self.download_path):
            os.mkdir(self.download_path)
        

    def close_browser(self):
        self.driver.quit()

    def set_download_path(self, new_path):
        self.download_path = new_path

    def get_download_path(self):
        return self.download_path

    #Searches a video by its name and returns the first link on the result search
    def search_by_name(self, video_name):
        # Searches a video enters on that video and returns its link
        wait = WebDriverWait(self.driver,10)
        input_box = wait.until(EC.element_to_be_clickable((By.XPATH,'//input[@id="search"]')))

        # Clicking Clearing and entering the video name search
        input_box.click()
        input_box.clear()
        input_box.send_keys(video_name)
        input_box.send_keys(Keys.RETURN)

        # Returning The video link
        return self.driver.current_url

    #Returns true if the link is a valid youtube video link
    def valid_yt_link(self, video_link):
    
        return True

    def download_mp3(self, link=None):
        # Dowloads the current video  or a video from the given link to a specified location
        # Has the option to download only audio or mp3
        if not link:
            if self.valid_yt_link(self.driver.current_url):
                link = self.driver.current_url
            else:
                raise Exception('Not a valid link!')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': self.download_path+'/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([link])
            except:
                ydl.download([link])

    def download_video(self, link=None):
        if not link:
            if self.valid_yt_link(self.driver.current_url):
                link = self.driver.current_url
            else:
                raise Exception('Not a valid link!')
        video = YouTube(link)
        video_stream = video.streams.get_highest_resolution()
        video_stream.download(self.download_path)


mytube = Youtube()
