import tkinter as tk
from tkinter import ttk
from pygame import mixer
from mutagen.easyid3 import EasyID3
import os

mixer.init()



# Function to play music
def play_music():
    # Replace with the actual path of your music file
    music_file = "music/My Bloody Valentine - When You Sleep.flac"
    
    if os.path.exists(music_file):
        mixer.music.load(music_file)
        mixer.music.play()

        # Extract and display metadata
        title, artist = get_song_metadata(music_file)
        song_title_label.config(text=title)
        artist_label.config(text=artist)
        now_playing_label.config(text="Playing...")

    else:
        now_playing_label.config(text="Music file not found")

    # Function to stop music
def stop_music():
    mixer.music.stop()

# Function to pause music
def pause_music():
    mixer.music.pause()

# Function to unpause music
def unpause_music():
    mixer.music.unpause()


def get_song_metadata(file_path):
    try:
        audio = EasyID3(file_path)
        print("Metadata for the song:", audio.pprint())
        title = audio.get('title', ['Unknown Title'])[0]
        artist = audio.get('artist', ['Unknown Artist'])[0]
        return title, artist
    except Exception as e:
        return "Unknown Title", "Unknown Artist"


# Create the main window
root = tk.Tk()
root.title("Now Playing")
root.geometry("300x200")

# Create and place widgets
# Now Playing Section

now_playing_frame = ttk.Frame(root, padding="10")
now_playing_frame.grid(row=0, column=0, padx=10, pady=10)

# Default labels, will be updated with real metadata when music is played
song_title_label = ttk.Label(now_playing_frame, text="Title", font=("Helvetica", 14, "bold"))
song_title_label.grid(row=0, column=0, sticky="W")

artist_label = ttk.Label(now_playing_frame, text="Artist", font=("Helvetica", 10))
artist_label.grid(row=1, column=0, sticky="W")

# Status section to show play/pause etc.
now_playing_label = ttk.Label(now_playing_frame, text="Status")
now_playing_label.grid(row=2, column=0, sticky="W")

# Controls Section
controls_frame = ttk.Frame(root, padding="10")
controls_frame.grid(row=1, column=0, padx=10, pady=10)

play_button = ttk.Button(controls_frame, text="Play", command=play_music)
play_button.grid(row=0, column=0, padx=5)

pause_button = ttk.Button(controls_frame, text="Pause", command=pause_music)
pause_button.grid(row=0, column=1, padx=5)

unpause_button = ttk.Button(controls_frame, text="Unpause", command=unpause_music)
unpause_button.grid(row=0, column=2, padx=5)

stop_button = ttk.Button(controls_frame, text="Stop", command=stop_music)
stop_button.grid(row=0, column=3, padx=5)

# Run the application
root.mainloop()