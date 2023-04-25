from __future__ import unicode_literals
from urllib.parse import unquote
import os
import yt_dlp
import uuid


class VimeoDownloader():
    def __init__(self, format_="bestvideo", path=r"E:\Cursos kodekloud"):
        yt_dlp.utils.std_headers['Referer'] = "https://kodekloud.com/"
        self.url_without_id = "https://player.vimeo.com/video/"
        self.save_path = path
        index = str(uuid.uuid4())
        self.ydl_opts = {
            'outtmpl': self.save_path + '/' + '- %(title)s.%(ext)s',
            'ratelimit': 9000000,
            'format': format_
        }
        self.ydl_opts_youtube = {
            'outtmpl': self.save_path + '/' + str(index) + '- %(title)s.%(ext)s',
            'format': 'best'
        }

    def get_format_audios(self, video_url):
        ydl = yt_dlp.YoutubeDL({'nocheckcertificate': True})
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get('formats', [])
        list_audios_format = []
        for f in formats:
            format_id = f.get('format_id', '')
            format_note = f.get('format_note', '')
            ext = f.get('ext', '')
            resolution = f.get('resolution', '')
            if "audio" in format_note and ext != "mp4":
                list_audios_format.append(format_id)
        return list_audios_format

    def get_format_videos(self, video_url):
        ydl = yt_dlp.YoutubeDL({'nocheckcertificate': True})
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get('formats', [])
        list_videos_format = []
        for f in formats:
            format_id = f.get('format_id', '')
            format_note = f.get('format_note', '')
            ext = f.get('ext', '')
            resolution = f.get('resolution', '')
            if not "audio" in format_note:
                list_videos_format.append(format_id)
        return list_videos_format

    def download_video(self, video_id, url=None):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            if url is not None:
                ydl.download([url])
            else:
                ydl.download([self.url_without_id + video_id])

    def download_audio(self, video_id, url=None):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            if url is not None:
                ydl.download([url])
            else:
                ydl.download([self.url_without_id + video_id])

    def download_video_youtube(self, url):
        with yt_dlp.YoutubeDL(self.ydl_opts_youtube) as ydl:
            ydl.download([url])

    def get_video_id(self, url):
        index_end_id = url.find('&key')
        if index_end_id < 0:
            return url
        index_start_id = index_end_id - 9
        video_id = url[index_start_id:index_end_id]
        return video_id

    def get_url_youtube(self, url):
        url = unquote(url)
        end_index = url.find("&key")
        start_index = end_index - 43
        new_url = url[start_index:end_index]
        return new_url


# vimeo_down_ = VimeoDownloader()
# try:
#     vimeo_down_.download_video(video_id="807005746")
# except:
#     pass
# list_formats = vimeo_down_.get_format_audios("https://player.vimeo.com/video/807005746")
# for format_audio in list_formats:
#     try:
#         vimeo_down_1 = VimeoDownloader(format_=format_audio)
#         vimeo_down_1.download_audio(video_id="807005746")
#         break
#     except Exception as e:
#         print(e)