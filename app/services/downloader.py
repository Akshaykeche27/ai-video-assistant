import yt_dlp
import os

def download_audio(url, output_folder):
 

    ydl_opts = {

        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
        except Exception as e:
            return f"Downlode failed: {str(e)}"