import yt_dlp
import re
from pathlib import Path
import os
import glob

def san(name: str) -> str:
    m = name.replace(" ", "_")
    t = re.sub(r'[\\/*?:"<>|().]', "_", m)
    c = re.sub(r'_+', "_", t)
    return c.strip("_")

def down(link: str) -> str:
    downloads_folder = Path.home() / "Downloads"
    os.makedirs(downloads_folder, exist_ok=True)

    # We use a distinct name for the process so it doesn't create 0kb placeholders 
    # that clash with your final sanitized filename.
    temp_outtmpl = str(downloads_folder / 'processing_task.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_outtmpl,
        'nopart': True,              # FIX: Stops the creation of .part / 0kb files [https://github.com]
        'keepvideo': False,          # FIX: Deletes the .webm/source after conversion
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 1. Download & Convert
        info = ydl.extract_info(link, download=True)
        
        # 2. Get the actual path created by the post-processor
        # It will be 'processing_task.mp3'
        temp_mp3 = Path(downloads_folder / 'processing_task.mp3')

        # 3. Target name
        safe_title = san(info.get("title", "audio"))
        final_mp3 = downloads_folder / f"{safe_title}.mp3"

        # 4. Final Move (This replaces any existing file)
        if temp_mp3.exists():
            if final_mp3.exists():
                final_mp3.unlink()
            os.replace(temp_mp3, final_mp3)

        # 5. REMOVE DUPLICATES: Specifically target the (1) files
        # This handles the "Song (1).mp3" issue you mentioned earlier
        for dup in glob.glob(str(downloads_folder / f"{safe_title} (*).mp3")):
            try:
                os.remove(dup)
            except:
                pass

    return str(final_mp3)
