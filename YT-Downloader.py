# Import the necessary modules
from pytube import Playlist
#import subprocess
import os

# Create a Playlist object and pass the URL of the YouTube playlist to the constructor
playlist = Playlist("https://youtube.com/playlist?list=OLAK5uy_lekO7NAep_XzPEVl20DV3Or8n_Qkw4Zg0")

# Iterate through the list of videos in the playlist and download the audio stream with the highest bitrate for each video
for video in playlist.videos:
    audio_streams = video.streams.filter(only_audio=True)
    sorted_streams = sorted(audio_streams, key=lambda s: s.abr)
    best_audio = sorted_streams[-1]
    #best_audio.download(output_path='downloads')
    # Download the audio stream to a temporary file
    tmp_file = best_audio.download(output_path='downloads')

    # Call ffmpeg to convert the audio stream to MP3
    #subprocess.run(['ffmpeg', '-i', tmp_file, '-vn', '-acodec', 'libmp3lame', '-aq', '2', 'downloads/' + video.title + '.mp3'])


    base, ext = os.path.splitext(tmp_file)
    new_file = base + '.mp3'
    os.rename(tmp_file, new_file)
  
