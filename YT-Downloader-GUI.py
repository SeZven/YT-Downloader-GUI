# Import the necessary modules
from pytube import Playlist
import os
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QProgressBar, QMessageBox
from PyQt5.QtCore import QThread

class PlaylistDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create the input field for the playlist URL
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Enter playlist URL')

        # Create the download button
        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.downloadPlaylist)
        
        # Create progress bar
        self.progress_bar = QProgressBar(self)

        # Create a layout and add the input field and button
        layout = QVBoxLayout(self)
        layout.addWidget(self.url_input)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)

        # Set the window title and show the widget
        self.setWindowTitle('Playlist Downloader')
        self.show()

    # not used anymore after bug with progress bar not updating
    def downloadPlaylistOLD(self):
        # Get the playlist URL from the input field
        playlist_url = self.url_input.text()
        # Disable button after click
        self.download_button.setEnabled(False)
        # Add code here to download the playlist using pytube and convert the audio streams to MP3
        # Create a Playlist object and pass the URL of the YouTube playlist to the constructor
        playlist = Playlist(f"{playlist_url}")

        # Iterate through the list of videos in the playlist and download the audio stream with the highest bitrate for each video
        i = 0
        for video in playlist.videos:
            i += 1
            self.progress_bar.setValue(int((i) / len(playlist.videos) * 100))

            audio_streams = video.streams.filter(only_audio=True)
            sorted_streams = sorted(audio_streams, key=lambda s: s.abr)
            best_audio = sorted_streams[-1]
            
            # Download the audio stream to a temporary file
            tmp_file = best_audio.download(output_path='downloads')
            base, ext = os.path.splitext(tmp_file)
            new_file = base + '.mp3'
            os.rename(tmp_file, new_file)
        self.close()

    def downloadPlaylist(self):
    # Get the playlist URL from the input field
        playlist_url = self.url_input.text()

    # Create an instance of the DownloadThread class and pass the playlist URL
        download_thread = DownloadThread(playlist_url, self)

    # Connect the finished signal of the thread to a slot that resets the progress bar
        download_thread.finished.connect(self.closeApplication)

    # Start the thread
        download_thread.start()

    def closeApplication(self):
        # Display a message in a pop-up window
        QMessageBox.information(self, "Download finished", "The download has finished.")
        # Close the program
        QApplication.exit()

# Used so that the progessbar can update also when GUI is not seen
class DownloadThread(QThread):
    def __init__(self, playlist_url, parent=None):
        super().__init__(parent)
        self.playlist_url = playlist_url

    def run(self):
        # Create a Playlist object and pass the URL of the YouTube playlist to the constructor
        playlist = Playlist(f"{self.playlist_url}")

        # Iterate through the list of videos in the playlist and download the audio stream with the highest bitrate for each video
        for i, video in enumerate(playlist.videos):
            # Update the progress bar
            self.parent().progress_bar.setValue(int((i+1) / len(playlist.videos) * 100))

            audio_streams = video.streams.filter(only_audio=True)
            sorted_streams = sorted(audio_streams, key=lambda s: s.abr)
            best_audio = sorted_streams[-1]

            # Download the audio stream to a temporary file
            tmp_file = best_audio.download(output_path='downloads')
            base, ext = os.path.splitext(tmp_file)
            new_file = base + '.mp3'
            os.rename(tmp_file, new_file)
    
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = PlaylistDownloader()
    sys.exit(app.exec_())
