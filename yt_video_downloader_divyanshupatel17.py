"""
Hi, I'm Divyanshu. You can check out my GitHub profile at divyanshupatel17. 
I'm seeking help to further develop my YouTube video and playlist downloader script. 
Any suggestions or contributions would be greatly appreciated!
LOVE!
"""
import os
import re
import time
import yt_dlp
from alive_progress import alive_bar
from colorama import Fore, Style, init
 
# Initialize colorama for colorful terminal output
init(autoreset=True)
 
def sanitize_filename(filename):
    """
    Sanitizes the filename by replacing any characters that are not alphanumeric or common symbols
    with underscores.
    """
    return re.sub(r'[^\w\-_\. ]', '_', filename)
 

def download_video(video_url, download_location):
    """
    Downloads a single video in the best available progressive format using yt-dlp.
    """
    ydl_opts = {
        'outtmpl': os.path.join(download_location, '%(title)s.%(ext)s'),
        'progress_hooks': [yt_dlp_hook],
        'noplaylist': True,
        'format': 'best[ext=mp4]/best',
        'ignoreerrors': True
    }
    print(f"{Fore.GREEN}Downloading video...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def download_playlist(playlist_url, download_location):
    """
    Downloads a playlist in the best available progressive format using yt-dlp.
    """
    ydl_opts = {
        'outtmpl': os.path.join(download_location, '%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s'),
        'progress_hooks': [yt_dlp_hook],
        'noplaylist': False,
        'format': 'best[ext=mp4]/best',
        'ignoreerrors': True
    }
    print(f"{Fore.GREEN}Downloading playlist...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

def yt_dlp_hook(d):
    if d['status'] == 'downloading':
        print(f"{Fore.YELLOW}Downloading: {d.get('filename', '')} - {d.get('_percent_str', '').strip()} at {d.get('_speed_str', '').strip()}", end='\r')
    elif d['status'] == 'finished':
        print(f"\n{Fore.GREEN}Done downloading: {d['filename']}")

if __name__ == "__main__":
    option = input(f"{Fore.YELLOW}Select an option: 1 for video, 2 for playlist: ").strip()
    if option == '2':
        playlist_url = input(f"{Fore.YELLOW}Enter the playlist url: ").strip()
        download_location = input(f"{Fore.YELLOW}Enter the download location: ").strip()
        print(f"{Fore.MAGENTA}yt-dlp will download the entire playlist in the best available progressive format (audio+video, no ffmpeg required).")
        download_playlist(playlist_url, download_location)
    elif option == '1':
        video_url = input(f"{Fore.YELLOW}Enter the video url: ").strip()
        download_location = input(f"{Fore.YELLOW}Enter the download location: ").strip()
        print(f"{Fore.MAGENTA}yt-dlp will download the video in the best available progressive format (audio+video, no ffmpeg required).")
        download_video(video_url, download_location)
    else:
        print(f"{Fore.RED}Invalid option. Please enter '1' for video or '2' for playlist.")