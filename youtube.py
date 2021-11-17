from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.common import exceptions
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import youtube_dl
from pytube import YouTube
# Chromium Path\
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Youtube Link
YOUTUBE_LINK = "https://www.youtube.com/"


def abr_to_int(video_stream):
    abr_string = getattr(video_stream, 'abr')
    return int(''.join([letra for letra in abr_string if letra.isnumeric()]))


class Youtube:
    def __init__(self, driver=None):
        # Initializing Chromium
        # Opcao de estar invisivel ou visivel
        self.driver = driver
        self.download_path = 'C:/Users/mitra/Desktop'
        # You can have one object of Youtube and keep closing and opening the browser so we use this var to keep track of it
        self.quitted_browser = False

    def open_browser(self):
        if not self.driver or self.quitted_browser:
            self.driver = webdriver.Chrome(
                ChromeDriverManager().install())
            self.quitted_browser = False

        else:
            pass
        self.driver.get(YOUTUBE_LINK)
        self.driver.maximize_window()
        # Handeling Coookies
        self.driver.implicitly_wait(10)
        cookies = self.driver.find_element_by_xpath(
            '//yt-formatted-string[text()="Aceito"]').click()

    def close_browser(self):
        self.driver.quit()
        self.quitted_browser = True

    def set_download_path(self, new_path):
        self.download_path = new_path

    def get_download_path(self):
        return self.download_path

    def search_by_name(self, video_name):
        # Searches a video enters on that video and returns its link
        self.driver.implicitly_wait(10)
        input_box = self.driver.find_element_by_xpath('//input[@id="search"]')

        # Clicking Clearing and entering the video name search
        input_box.click()
        input_box.clear()
        input_box.send_keys(video_name)
        input_box.send_keys(Keys.RETURN)

        # Returning The video link
        return self.driver.current_url

    def valid_yt_link(self, video_link):
        # Verificar se o link do video é valido senao lancar uma exception
        # se o video for de uma musica na playlist ir buscar essa musica
        return True

    def search_by_link(self, video_link):
        # Enters in that video link

        link_header = "https://www.youtube.com/watch?v="
        # Verificar se o link se refere a um video do yt
        if video_link[:len(link_header)] != link_header:
            print(video_link)
            raise BaseException('The given link is not a youtube video')

        # An elif for invalid video?
        else:
            self.driver.get(video_link)

        return self.driver.current_url

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
            ydl.download([link])

    def download_video(self, link=None):
        # if not link:
        # link = self.driver.current_url
        if not link:
            if self.valid_yt_link(self.driver.current_url):
                link = self.driver.current_url
            else:
                raise Exception('Not a valid link!')
        video = YouTube(link)
        video_stream = video.streams.get_highest_resolution()
        video_stream.download(self.download_path)


if __name__ == '__main__':
    yt = Youtube()
    yt.download_video('https://www.youtube.com/watch?v=DmWWqogr_r8')
