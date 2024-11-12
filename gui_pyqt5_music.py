import sys
import os
import pygame
import io
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QTransform,QImage
from PyQt5.QtCore import Qt
from PIL import Image

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize Pygame mixer
        pygame.mixer.init()
        
        self.setWindowTitle("iPod Music Player")
        self.setGeometry(100, 100, 600, 400)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Window)
        
        # Layouts
        self.main_layout = QVBoxLayout(self)
        
        # Create a horizontal layout for album art and text (title and artist)
        self.album_and_text_layout = QHBoxLayout()

        
        
        # Album Art Label
        self.album_art_label = QLabel(self)
        self.album_art_label.setFixedSize(100, 100)
        # self.main_layout.addWidget(self.album_art_label, alignment=Qt.AlignLeft)
        self.album_and_text_layout.addWidget(self.album_art_label, alignment=Qt.AlignLeft)
        
        # Title and Artist Labels inside a vertical layout (stacked one on top of the other)
        self.text_layout = QVBoxLayout()
        self.title_label = QLabel("Title: Unknown", self)
        self.artist_label = QLabel("Artist: Unknown", self)
        self.title_label.setStyleSheet("font-size: 20px; color: #333333;")
        self.artist_label.setStyleSheet("font-size: 16px; color: #777777;")

        self.text_layout.addWidget(self.title_label, alignment=Qt.AlignTop)
        self.text_layout.addWidget(self.artist_label, alignment=Qt.AlignTop)
        
        # self.main_layout.addWidget(self.title_label)
        # self.main_layout.addWidget(self.artist_label)

        self.album_and_text_layout.addLayout(self.text_layout)
        self.main_layout.addLayout(self.album_and_text_layout)
        
        # Control Buttons
        self.control_layout = QHBoxLayout()

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_music)
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_music)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_music)

        self.control_layout.addWidget(self.play_button)
        self.control_layout.addWidget(self.pause_button)
        self.control_layout.addWidget(self.stop_button)

        self.main_layout.addLayout(self.control_layout)

        # Metadata Display
        self.metadata_text = QTextEdit(self)
        self.metadata_text.setReadOnly(True)
        self.main_layout.addWidget(self.metadata_text)
        
        # Set Layout
        self.setLayout(self.main_layout)

        # Example music file path (update this)
        self.music_file = "music/My Bloody Valentine - When You Sleep.flac"  # Change to your actual music file path

    def paintEvent(self, event):
        # This is where the magic happens for the acrylic-like effect.
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create a semi-transparent white background
        brush = QBrush(QColor(255, 255, 255, 180))  # 180 is the transparency level
        painter.fillRect(self.rect(), brush)

    def get_song_metadata(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: File '{file_path}' does not exist.")

        try:
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
                album_art = audio.pictures[0].data if audio.pictures else None  # Extract album art

            else:
                raise ValueError("Error: Unsupported file format. Please use an MP3 or FLAC file.")

            return title, artist, album_art

        except Exception as e:
            raise RuntimeError(f"Error extracting metadata: {e}")

    def play_music(self):
        try:
            title, artist, album_art = self.get_song_metadata(self.music_file)
            self.title_label.setText(f"Title: {title}")
            self.artist_label.setText(f"Artist: {artist}")

            # Display album art if available
            if album_art:
                # self.display_album_art(album_art)
                # self.display_3d_album_art(album_art)
                self.display_top_bottom_album_art(album_art)
                # self.display_album_art_with_title_label(album_art)
            else:
                album_art_image = Image.open("path/to/default_image.png")  # Use a default image if no album art
                # self.display_album_art(album_art_image)
                # self.display_3d_album_art(album_art_image)
                self.display_top_bottom_album_art(album_art_image)
                # self.display_album_art_with_title_label(album_art_image)

            # Play music
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play()

            file_extension = os.path.splitext(self.music_file)[1].lower()
            if file_extension == '.mp3':
                audio = MP3(self.music_file, ID3=ID3)  # Load the MP3 file metadata
            elif file_extension == '.flac':
                audio = FLAC(self.music_file)  # Load the FLAC file metadata
            else:
                raise ValueError("Unsupported file format")

            # Display full metadata
            self.metadata_text.clear()
            self.metadata_text.append("Full Metadata:\n")
            for key, value in audio.items():
                self.metadata_text.append(f"{key}: {value[0]}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # def display_album_art(self, album_art_data):
    #     # Convert bytes data to an image
        # if isinstance(album_art_data, bytes):
        #     album_art_image = Image.open(io.BytesIO(album_art_data))
        # else:
        #     album_art_image = album_art_data

        # # Resize image
        # album_art_image = album_art_image.resize((100, 100), Image.LANCZOS)
        # album_art_image.save("temp_album_art.png")  # Save to file for Qt to read
        # pixmap = QPixmap("temp_album_art.png")
    #     self.album_art_label.setPixmap(pixmap)

    def display_3d_album_art(self, album_art_data):

        if isinstance(album_art_data, bytes):
            album_art_image = Image.open(io.BytesIO(album_art_data))
        else:
            album_art_image = album_art_data

        # Resize image
        album_art_image = album_art_image.resize((100, 100), Image.LANCZOS)
        album_art_image.save("temp_album_art.png")  # Save to file for Qt to read
        pixmap = QPixmap("temp_album_art.png")

        self.album_art_label.setPixmap(pixmap)

        image=pixmap
            

        

        # # Simulate 3D perspective by scaling and skewing the image
        # transform = QTransform()
        # transform.scale(1.0, 0.9)  # Apply vertical scaling for 3D effect
        # transform.shear(-0.3, 0)   # Apply horizontal skew for perspective

        # transformed_image = image.transformed(transform, Qt.SmoothTransformation)

            # Create reflection by flipping the image vertically
        reflection_image = image.transformed(QTransform().scale(1, -1))

            # Apply transparency gradient to the reflection
        reflection = reflection_image.toImage()
        height = reflection.height()
        for y in range(height):
            # Fading effect: transparency decreases from 255 to 0
            alpha = int(255 * (1 - (y / height)))
            for x in range(reflection.width()):
                color = reflection.pixelColor(x, y)
                color.setAlpha(alpha)
                reflection.setPixelColor(x, y, color)

        reflection_pixmap = QPixmap.fromImage(reflection)

        # Ensure we remove any previous reflection label
        if hasattr(self, 'reflection_label'):
            self.reflection_label.deleteLater()

        # # Create a new QLabel to display the reflection image
        # self.reflection_label = QLabel(self)
        # self.reflection_label.setPixmap(reflection_pixmap)
        # self.reflection_label.setFixedSize(100, 100)  # Set the same size as the original album art

        # # Create a new layout to stack the original and reflection images vertically
        # image_layout = QVBoxLayout()
        # image_layout.addWidget(self.album_art_label)
        # image_layout.addWidget(self.reflection_label)

        # # Clear the main layout first to ensure we're not adding multiple layers
        # while self.main_layout.count():
        #     child = self.main_layout.takeAt(0)
        #     if child.widget():
        #         child.widget().deleteLater()

        # # Add the image layout and other UI elements back to the main layout
        # self.main_layout.addLayout(image_layout)
        # self.main_layout.addWidget(self.title_label)
        # self.main_layout.addWidget(self.artist_label)
        # self.main_layout.addLayout(self.control_layout)
        # self.main_layout.addWidget(self.metadata_text)

        # Create a new QLabel to display the reflection image
        self.reflection_label = QLabel(self)
        self.reflection_label.setPixmap(reflection_pixmap)
        self.reflection_label.setFixedSize(100, 100)  # Set the same size as the original album art

        # Only update the album art and reflection in the layout
        self.main_layout.insertWidget(0, self.album_art_label)
        self.main_layout.insertWidget(1, self.reflection_label)

    def display_top_bottom_album_art(self, album_art_data):
        if isinstance(album_art_data, bytes):
            album_art_image = Image.open(io.BytesIO(album_art_data))
        else:
            album_art_image = album_art_data

        # Resize the original album art
        album_art_image = album_art_image.resize((100, 100), Image.LANCZOS)
        album_art_image.save("temp_album_art.png")
        original_pixmap = QPixmap("temp_album_art.png")

        # Display the original album art in the existing label
        self.album_art_label.setPixmap(original_pixmap)

        # Create reflection by flipping the image vertically
        reflection_image = original_pixmap.transformed(QTransform().scale(1, -1))

        # Convert QPixmap to QImage for pixel manipulation
        reflection_image = reflection_image.toImage()

        # Create a new QImage for the reflection with fading transparency
        reflection = QImage(reflection_image.size(), QImage.Format_ARGB32)
        reflection.fill(Qt.transparent)  # Start with a transparent background

        # Apply a transparency gradient to the reflection
        height = reflection.height()
        for y in range(height):
            alpha = int(255 * (1 - (y / height)))  # Fade from opaque to transparent
            for x in range(reflection.width()):
                color = reflection_image.pixelColor(x, y)
                color.setAlpha(alpha)  # Set the alpha for the pixel
                reflection.setPixelColor(x, y, color)

        reflection_pixmap = QPixmap.fromImage(reflection)

        # Ensure we remove any previous reflection label
        if hasattr(self, 'reflection_label'):
            self.reflection_label.deleteLater()

        # Create a new QLabel to display the reflection image
        self.reflection_label = QLabel(self)
        self.reflection_label.setPixmap(reflection_pixmap)
        self.reflection_label.setFixedSize(100, 100)  # Set the same size as the original album art
        self.reflection_label.setAlignment(Qt.AlignLeft)

        # Insert the album art and reflection in the layout
        self.main_layout.insertWidget(0, self.album_art_label)
        self.main_layout.insertWidget(1, self.reflection_label)

    def display_album_art_with_title_label(self, album_art_data):

        if isinstance(album_art_data, bytes):

            album_art_image = Image.open(io.BytesIO(album_art_data))
        else:
            album_art_image = Image.open(album_art_data)

        # Resize the image to a specific size for the album art display.
        album_art_image = album_art_image.resize((100, 100), Image.LANCZOS)

        # Convert the image to a Qt-compatible format (QPixmap).
        album_art_image.save("temp_album_art.png")  # Temporarily save the image.
        pixmap = QPixmap("temp_album_art.png")

        # Set the top part of the album art.
        self.album_art_label.setPixmap(pixmap)

        # Create a reflection of the image by flipping it vertically.
        reflection_pixmap = pixmap.transformed(QTransform().scale(1, -1))

        # Convert the reflection to a QImage for transparency modifications.
        reflection_image = reflection_pixmap.toImage()
        height = reflection_image.height()

        # Apply a transparency gradient to the reflection image.
        for y in range(height):
            alpha = int(255 * (1 - (y / height)))  # Gradually decrease transparency.
            for x in range(reflection_image.width()):
                color = reflection_image.pixelColor(x, y)
                color.setAlpha(alpha)  # Apply alpha transparency.
                reflection_image.setPixelColor(x, y, color)

        # Convert the modified reflection image back to a QPixmap.
        reflection_pixmap = QPixmap.fromImage(reflection_image)

        # Ensure that any previous reflection label is removed (to prevent stacking).
        if hasattr(self, 'reflection_label'):
            self.reflection_label.deleteLater()

        # Create a new QLabel to hold the reflection image.
        self.reflection_label = QLabel(self)
        self.reflection_label.setPixmap(reflection_pixmap)
        self.reflection_label.setFixedSize(100, 100)  # Set the size same as the original album art.

        # Adjust layout to move the album art and reflection to the right.
        if hasattr(self, 'album_art_layout'):
            # Remove the previous layout to avoid stacking multiple times.
            self.album_art_layout.deleteLater()

        # Create a new vertical layout for the album art and reflection.
        self.album_art_layout = QVBoxLayout()
        self.album_art_layout.addWidget(self.album_art_label)  # Top: Original image.
        self.album_art_layout.addWidget(self.reflection_label)  # Bottom: Reflection.

        # Create a new horizontal layout to place the album art on the right.
        self.right_layout = QHBoxLayout()
        self.right_layout.addStretch(1)  # Add stretching space to the left.
        self.right_layout.addLayout(self.album_art_layout)  # Add album art on the right.

        # Set the new layout as the main layout.
        self.main_layout.addLayout(self.right_layout)


    def pause_music(self):
        pygame.mixer.music.pause()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.album_art_label.clear()  # Clear album art when stopping

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
