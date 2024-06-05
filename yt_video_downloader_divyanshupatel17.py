"""
Hi, I'm Divyanshu. You can check out my GitHub profile at divyanshupatel17. 
I'm seeking help to further develop my YouTube video and playlist downloader script. 
Any suggestions or contributions would be greatly appreciated!
LOVE!
"""
import os
import re
import time
from pytube import Playlist, YouTube
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
 
def get_available_resolutions(video):
    """
    Retrieves and sorts all available progressive stream resolutions for the given video.
    """
    streams = video.streams.filter(progressive=True)
    resolutions = sorted(set([stream.resolution for stream in streams]), key=lambda x: int(x[:-1]))
    return resolutions
 
def download_video(video, resolution, video_path, download_type):
    """
    Downloads a single video with the specified resolution and download type.
    Displays a progress bar for the download.
    """
    # Select the appropriate video stream based on the download type
    if download_type == 1:
        video_stream = video.streams.filter(only_audio=True).first()
    elif download_type == 2:
        video_stream = video.streams.filter(only_video=True, res=resolution).first()
    else:
        video_stream = video.streams.filter(res=resolution, progressive=True).first()
 
    # If no specific resolution stream is found, select the highest resolution available
    if not video_stream:
        highest_resolution_stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()
        video_stream = highest_resolution_stream
 
    # Check if the video already exists
    if os.path.exists(video_path):
        print(f"{video_path} already exists")
        return
 
    # Get sanitized video name and total size for progress bar
    video_name = sanitize_filename(video_stream.default_filename)
    print(f"{Fore.GREEN}Downloading {video_name} in {video_stream.resolution if download_type != 1 else 'audio only'}")
    total_size = video_stream.filesize
 
    # Start time for calculating download speed
    start_time = time.time()
 
    # Initialize alive_progress bar for the video download
    with alive_bar(total_size, title=video_name, bar='smooth', spinner='dots_waves2', force_tty=True, enrich_print=False,
                   theme='classic', stats=False) as progress_bar:
 
        # Callback function to update progress bar
        def on_progress(stream, chunk, bytes_remaining):
            progress_bar(len(chunk))
 
        # Register progress callback and start download
        video.register_on_progress_callback(on_progress)
        video_stream.download(filename=video_path)
 
    # Calculate elapsed time and display download stats
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{Fore.CYAN}Downloaded {video_name} ({total_size / (1024 * 1024):.2f} MB) in {elapsed_time:.2f} seconds")
    print(f"{Fore.CYAN}Average Speed: {total_size / elapsed_time / (1024 * 1024):.2f} MB/s")
 
def download_playlist(playlist_url, resolution, download_type, download_location, start_index=None, end_index=None):
    """
    Downloads a playlist with the specified resolution and download type.
    Displays an overall progress bar for the entire playlist and individual progress bars for each video.
    """
    # Initialize playlist and sanitize playlist name
    playlist = Playlist(playlist_url)
    playlist_name = sanitize_filename(re.sub(r'\W+', '-', playlist.title))
    total_videos = len(playlist.video_urls)
    
    print(f"{Fore.MAGENTA}Total number of videos in the playlist: {total_videos}")
    
    # Create directory for the playlist
    playlist_path = os.path.join(download_location, playlist_name)
    if not os.path.exists(playlist_path):
        os.mkdir(playlist_path)
 
    # Set default range for downloading all videos if not specified
    if start_index is None or end_index is None:
        start_index, end_index = 1, total_videos
 
    # Loop through each video in the specified range and download
    for index, video in enumerate(playlist.videos[start_index-1:end_index], start=start_index):
        video_title = sanitize_filename(video.title)
        video_path = os.path.join(playlist_path, f"{index}-{video_title}.mp4")
        download_video(video, resolution, video_path, download_type)
        print("----------------------------------")
 
if __name__ == "__main__":
    # Main script execution starts here
    option = input(f"{Fore.YELLOW}Select an option: 1 for video, 2 for playlist: ").strip()
    
    if option == '2':
        # Handle playlist download option
        playlist_url = input(f"{Fore.YELLOW}Enter the playlist url: ").strip()
        download_location = input(f"{Fore.YELLOW}Enter the download location: ").strip()
        playlist = Playlist(playlist_url)
        total_videos = len(playlist.video_urls)
        print(f"{Fore.MAGENTA}Total number of videos in the playlist: {total_videos}")
 
        # Display and select download type
        download_types = ["1 for audio only", "2 for video only", "3 for both audio and video"]
        for download_type in download_types:
            print(download_type)
        download_type = int(input(f"{Fore.YELLOW}Select download type: ").strip())
        
        # Get available resolutions from the first video in the playlist
        first_video = YouTube(playlist.video_urls[0])
        resolutions = get_available_resolutions(first_video)
        for i, res in enumerate(resolutions, start=1):
            print(f"{i} for {res}")
        res_option = int(input(f"{Fore.YELLOW}Select a resolution: ").strip())
        resolution = resolutions[res_option - 1]
 
        # Ask user if they want to download all videos or a specific range
        range_option = input(f"{Fore.YELLOW}Do you want to download all videos or a range? (all/range): ").strip().lower()
        if range_option == 'range':
            start_index = int(input(f"{Fore.YELLOW}Enter the starting video number (1 to {total_videos}): ").strip())
            end_index = int(input(f"{Fore.YELLOW}Enter the ending video number ({start_index} to {total_videos}): ").strip())
            download_playlist(playlist_url, resolution, download_type, download_location, start_index, end_index)
        else:
            download_playlist(playlist_url, resolution, download_type, download_location)
    elif option == '1':
        # Handle single video download option
        video_url = input(f"{Fore.YELLOW}Enter the video url: ").strip()
        download_location = input(f"{Fore.YELLOW}Enter the download location: ").strip()
        
        video = YouTube(video_url)
        resolutions = get_available_resolutions(video)
        for i, res in enumerate(resolutions, start=1):
            print(f"{i} for {res}")
        res_option = int(input(f"{Fore.YELLOW}Select a resolution: ").strip())
        resolution = resolutions[res_option - 1]
 
        # Display and select download type
        download_types = ["1 for audio only", "2 for video only", "3 for both audio and video"]
        for download_type in download_types:
            print(download_type)
        download_type = int(input(f"{Fore.YELLOW}Select download type: ").strip())
 
        video_title = sanitize_filename(video.title)
        video_path = os.path.join(download_location, f"{video_title}.mp4")
        download_video(video, resolution, video_path, download_type)
        print(f"{Fore.CYAN}Downloaded {video_title} in {resolution}")
    else:
        print(f"{Fore.RED}Invalid option. Please enter '1' for video or '2' for playlist.")