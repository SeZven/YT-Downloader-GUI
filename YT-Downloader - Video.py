# Import the necessary modules
from pytube import Playlist

# Create a Playlist object and pass the URL of the YouTube playlist to the constructor
playlist = Playlist("https://youtube.com/playlist?list=OLAK5uy_lekO7NAep_XzPEVl20DV3Or8n_Qkw4Zg0")

# Iterate through the list of videos in the playlist and download the video with the highest resolution for each video
for video in playlist.videos:
    # Get the highest resolution video available
    best_video = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    best_video.download(output_path='downloads')
