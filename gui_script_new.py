import tkinter as tk
from tkinter import filedialog, messagebox
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC
import os
import pygame
from PIL import Image, ImageTk
import io

# Function to extract song metadata based on file type
def get_song_metadata(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: File '{file_path}' does not exist.")

    try:
        # Check the file extension to determine how to read the metadata
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.mp3':
            audio = MP3(file_path, ID3=ID3)
            title = audio.get('TIT2', 'Unknown Title').text[0] if audio.get('TIT2') else 'Unknown Title'
            artist = audio.get('TPE1', 'Unknown Artist').text[0] if audio.get('TPE1') else 'Unknown Artist'
            album_art = audio.get('APIC:Cover', None)  # Extract album art
        
        elif file_extension == '.flac':
            audio = FLAC(file_path)
            title = audio.get('title', ['Unknown Title'])[0]
            artist = audio.get('artist', ['Unknown Artist'])[0]
            album_art = audio.pictures[0].data if audio.pictures else None
        
        else:
            raise ValueError("Error: Unsupported file format. Please use an MP3 or FLAC file.")

        return title, artist, audio, album_art

    except Exception as e:
        raise RuntimeError(f"Error extracting metadata: {e}")

# Function to play the selected music file
def play_music():
    # music_file = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3 *.flac")])
    # if not music_file:
    #     return  # User cancelled file dialog

    music_file = "music/My Bloody Valentine - When You Sleep.flac"

    try:
        title, artist, metadata, album_art = get_song_metadata(music_file)
        # Display song title and artist in the GUI
        title_label.config(text=title)
        artist_label.config(text=artist)

        # Initialize Pygame mixer and play music
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()

        # Display full metadata in the text widget
        metadata_text.insert(tk.END, "Full Metadata:\n")
        for key, value in metadata.items():
            metadata_text.insert(tk.END, f"{key}: {value[0]}\n")

        # Display album art if available
        if album_art:
            display_album_art(album_art)
        else:
            album_art_image = Image.open("path/to/default_image.png")  # Use a default image if no album art
            display_album_art(album_art_image)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to display album art
def display_album_art(album_art_data):
    # Convert bytes data to an image
    if isinstance(album_art_data, bytes):
        album_art_image = Image.open(io.BytesIO(album_art_data))
    else:
        album_art_image = album_art_data

    # Resize image
    album_art_image = album_art_image.resize((200, 200), Image.LANCZOS)
    album_art_image_tk = ImageTk.PhotoImage(album_art_image)

    # Display image on the label
    album_art_label.config(image=album_art_image_tk)
    album_art_label.image = album_art_image_tk  # Keep a reference to avoid garbage collection

def stop_music():
    pygame.mixer.music.stop()

# Function to pause music
def pause_music():
    pygame.mixer.music.pause()


# Initialize the Tkinter GUI
root = tk.Tk()
root.title("iPod Music Player")
root.geometry("600x300")  # Adjust height for the new layout
root.configure(bg="#ffffff")  # Background color

# Create a Main Frame for Album Art and Info
main_frame = tk.Frame(root, bg="#ffffff")
main_frame.pack(pady=10)

# Create Album Art Label
album_art_label = tk.Label(main_frame, bg="#ffffff")
album_art_label.pack(side=tk.LEFT, padx=10)

# Create a Frame for Title and Artist
info_frame = tk.Frame(main_frame, bg="#ffffff")
info_frame.pack(side=tk.LEFT, padx=10)

# Title Label
title_label = tk.Label(info_frame, text="Title: Unknown", font=("Helvetica", 20), bg="#ffffff", fg="#333333")
title_label.pack(pady=5)

# Artist Label
artist_label = tk.Label(info_frame, text="Artist: Unknown", font=("Helvetica", 16), bg="#ffffff", fg="#777777")
artist_label.pack(pady=5)

# Create Control Frame
control_frame = tk.Frame(root, bg="#ffffff")
control_frame.pack(pady=20)

# Control Buttons
button_style = {
    "font": ("Helvetica", 14),
    "width": 10,
    "bg": "#007AFF",
    "fg": "white",
    "borderwidth": 0,
    "activebackground": "#005BB5"
}

play_button = tk.Button(control_frame, text="Play", command=play_music, **button_style)
play_button.grid(row=0, column=0, padx=20)

pause_button = tk.Button(control_frame, text="Pause", command=pause_music, **button_style)
pause_button.grid(row=0, column=1, padx=20)

stop_button = tk.Button(control_frame, text="Stop", command=stop_music, **button_style)
stop_button.grid(row=0, column=2, padx=20)

# Create a Text widget to display full metadata
metadata_text = tk.Text(root, height=10, width=70, font=("Helvetica", 12), bg="#f7f7f7", borderwidth=1)
metadata_text.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()