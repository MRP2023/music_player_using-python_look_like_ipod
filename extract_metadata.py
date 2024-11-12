import os
import sys
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC

# Function to extract song metadata based on file type
def get_song_metadata(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    try:
        # Check the file extension to determine how to read the metadata
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.mp3':
            audio = MP3(file_path, ID3=ID3)
            title = audio.get('TIT2', 'Unknown Title').text[0] if audio.get('TIT2') else 'Unknown Title'
            artist = audio.get('TPE1', 'Unknown Artist').text[0] if audio.get('TPE1') else 'Unknown Artist'
        
        elif file_extension == '.flac':
            audio = FLAC(file_path)
            title = audio.get('title', ['Unknown Title'])[0]
            artist = audio.get('artist', ['Unknown Artist'])[0]
        
        else:
            print("Error: Unsupported file format. Please use an MP3 or FLAC file.")
            return

        # Print title, artist, and full metadata
        print(f"Title: {title}")
        print(f"Artist: {artist}")
        print("\nFull Metadata:")
        for key, value in audio.items():
            print(f"{key}: {value[0]}")

    except Exception as e:
        print(f"Error extracting metadata: {e}")

if __name__ == "__main__":
    file_path ="music/My Bloody Valentine - When You Sleep.flac"
    get_song_metadata(file_path)
