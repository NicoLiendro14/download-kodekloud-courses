import os.path
import re

import requests
from bs4 import BeautifulSoup
from VimeoDownloader import VimeoDownloader
from browser_service import get_courses_url
from scraper_bs4 import get_video_player_link

# Configurar nivel de registro de logging a ERROR
import logging
logging.basicConfig(level=logging.ERROR)

list_video_url = get_courses_url()
all_videos = []
print("Cantidad de cursos: ", len(list_video_url))
index = 1
for course_url in list_video_url:
    print("Curso " + str(index) + "/" + str(len(list_video_url)))
    print("URL: ", course_url)
    #all_videos.append()
    list_videos_to_download_course = get_video_player_link(course_url)
    root_path = r"E:\Cursos kodekloud"

    response = requests.get(course_url)
    soup = BeautifulSoup(response.text, "html.parser")
    titulo = soup.title.string
    titulo = re.sub(r'[^\w\s]+', '', titulo)

    folder_path = os.path.join(root_path, titulo)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    vimeo_down_ = VimeoDownloader(path=folder_path)
    for video_download in list_videos_to_download_course:
        pattern = r"/(\d+)$"
        match = re.search(pattern, video_download[0])
        video_id = match.group(1)
        vimeo_down_.download_video(video_id=video_id)

        list_format_video = vimeo_down_.get_format_audios(video_download[0])
        vimeo_down_sound = VimeoDownloader(format_=list_format_video[0], path=folder_path)
        vimeo_down_sound.download_audio(video_id=video_id)
    index += 1
print("Cantidad de videos en total de la plataforma: ", len(all_videos))
