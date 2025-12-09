import yt_dlp
import os
from django.conf import settings
from pathlib import Path

def down(link):
    downloads_folder = str(Path.home() / "Downloads")
    os.makedirs(downloads_folder, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        filename = info.get('title', 'audio') + ".mp3"
        filepath = os.path.join(downloads_folder, filename)

    return filepath 
