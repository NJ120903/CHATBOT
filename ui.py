import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QDialog, QFormLayout, QLabel, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import pyttsx3
import platform
import subprocess
import speech_recognition as sr
import webbrowser
from brain import Main_Brain

# File Organizer logic
file_types = {
    'Images': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
    'Documents': ['txt', 'doc', 'docx', 'pdf', 'xls', 'xlsx', 'ppt', 'pptx'],
    'Videos': ['mp4', 'avi', 'mov', 'mkv'],
    'Music': ['mp3', 'wav', 'flac', 'aac'],
    'Archives': ['zip', 'rar', '7z', 'tar', 'gz'],
    'Executables': ['exe', 'msi', 'bat'],
    'Programming': ['py', 'java', 'c', 'cpp', 'h', 'html', 'css', 'js'],
    'Others': []
}

def organize_files(directory, progress_var, progress_label, root_window):
    progress_var.set(0)
    total_files = sum(len(files) for _, _, files in os.walk(directory))

    for dir_path, _, files in os.walk(directory):
        for file in files:
            src_path = os.path.join(dir_path, file)
            file_ext = file.split('.')[-1].lower()
            category = 'Others'

            if not file_ext or file_ext in ('', ' '):
                pass
            else:
                for cat, extensions in file_types.items():
                    if file_ext in extensions:
                        category = cat
                        break

            dest_folder = os.path.join(directory, category)
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, file)
            shutil.move(src_path, dest_path)

            progress_var.set(progress_var.get() + 1)
            progress_label.config(text=f'Progress: {progress_var.get()} / {total_files}')
            root_window.update()

# Chatbot GUI
class ChatbotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MGM Chatbot")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #1b1f23; color: white;")

        main_layout = QVBoxLayout()

        # Top controls layout
        top_controls_layout = QHBoxLayout()

        # Voice output toggle
        self.voice_output_checkbox = QCheckBox("Enable Voice Output")
        self.voice_output_checkbox.setFont(QFont("Arial", 12))
        self.voice_output_checkbox.setStyleSheet("color: white;")
        top_controls_layout.addWidget(self.voice_output_checkbox)

        # File Organizer button
        self.file_organizer_button = QPushButton("📂 Open File Organizer")
        self.file_organizer_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.file_organizer_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5e6c;
                color: white;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #ff5e6c;
            }
            QPushButton:hover {
                background-color: #ff7489;
            }
        """)
        self.file_organizer_button.clicked.connect(self.start_file_organizer)
        top_controls_layout.addWidget(self.file_organizer_button)

        main_layout.addLayout(top_controls_layout)

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setFont(QFont("Arial", 14))
        self.chat_display.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #262b30, stop:1 #1e2126);
            color: white;
            border: 2px solid #ff5e6c;
            border-radius: 15px;
            padding: 10px;
        """)
        self.chat_display.setReadOnly(True)
        main_layout.addWidget(self.chat_display)

        # Input and buttons layout
        input_buttons_layout = QHBoxLayout()

        # Input area
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Arial", 14))
        self.input_field.setStyleSheet("""
            background-color: #2c3136;
            color: white;
            border-radius: 10px;
            padding: 10px;
            border: 2px solid #ff5e6c;
        """)
        self.input_field.returnPressed.connect(self.handle_return_pressed)
        input_buttons_layout.addWidget(self.input_field)

        # Send button
        self.send_button = QPushButton("🚀 Send")
        self.send_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5e6c;
                color: white;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #ff5e6c;
            }
            QPushButton:hover {
                background-color: #ff7489;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_buttons_layout.addWidget(self.send_button)

        # Voice input button
        self.voice_input_button = QPushButton("🎤 Speak")
        self.voice_input_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.voice_input_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5e6c;
                color: white;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #ff5e6c;
            }
            QPushButton:hover {
                background-color: #ff7489;
            }
        """)
        self.voice_input_button.clicked.connect(self.handle_voice_input)
        input_buttons_layout.addWidget(self.voice_input_button)

        main_layout.addLayout(input_buttons_layout)

        self.setLayout(main_layout)

        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()

        # Set up the voice input thread
        self.voice_input_thread = VoiceInputThread()
        self.voice_input_thread.recognized_text.connect(self.handle_recognized_text)

    def handle_return_pressed(self):
        if self.input_field.text().strip():
            self.send_message()

    def send_message(self):
        message = self.input_field.text()
        if message:
            self.chat_display.append(f"<p style='color: #ff5e6c;'><b>You:</b> {message}</p>")
            self.input_field.clear()

            # Simulate typing animation
            self.chat_display.append("<p style='color: #888;'><i>MGM Chatbot is thinking...</i></p>")
            QTimer.singleShot(2000, lambda: self.display_response(message))  # 2-second delay to simulate thinking

    def handle_voice_input(self):
        self.chat_display.append("<p style='color: #888;'><i>You are being listened to...</i></p>")
        self.voice_input_thread.start()

    def handle_recognized_text(self, text):
        self.input_field.setText(text)
        self.send_message()

    def display_response(self, user_message):
        if user_message.startswith("open app"):
            app_name = user_message.split("open app", 1)[1].strip()
            response = self.open_application(app_name)
        elif user_message.startswith("open website"):
            website = user_message.split("open website", 1)[1].strip()
            webbrowser.open(f"http://{website}")
            response = f"Opening website {website}"
        else:
            response = Main_Brain(user_message)  # Use Main_Brain to generate the response

        self.chat_display.append(f"<p style='color: #66cc99;'><b>Chatbot:</b> {response}</p>")
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.End)
        self.chat_display.setTextCursor(cursor)

        # Speak response if voice output is enabled
        if self.voice_output_checkbox.isChecked():
            self.tts_engine.say(response)
            self.tts_engine.runAndWait()

    def open_application(self, app_name):
        if platform.system() == 'Windows':
            # Common directories for application executables
            common_dirs = [
                os.environ.get('PROGRAMFILES', ''),
                os.environ.get('PROGRAMFILES(X86)', ''),
                os.environ.get('LOCALAPPDATA', '')
            ]
            
            # Known application paths for common applications
            known_apps = {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'wordpad': 'wordpad.exe'
                # Add more known apps here if needed
            }
            
            # Check if the app_name is in the known apps
            if app_name.lower() in known_apps:
                app_path = known_apps[app_name.lower()]
                try:
                    subprocess.Popen(app_path)
                    return f"{app_name.capitalize()} has been opened."
                except Exception as e:
                    return f"Error opening {app_name}: {str(e)}"

            # General search in common directories
            for directory in common_dirs:
                if directory:
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            if file.lower().startswith(app_name.lower()) and file.lower().endswith(('.exe', '.bat')):
                                try:
                                    subprocess.Popen(os.path.join(root, file))
                                    return f"Opened {app_name}"
                                except Exception as e:
                                    return f"Error opening {app_name}: {str(e)}"
            
            return f"{app_name} not found on your PC."
        else:
            return "This feature is only available on Windows."

    def start_file_organizer(self):
        file_organizer_window = tk.Tk()
        file_organizer_window.title("File Organizer")

        # Initialize progress variable
        progress_var = tk.DoubleVar()

        # Progress label
        progress_label = tk.Label(file_organizer_window, text="Progress: 0 / 0", font=("Arial", 14))
        progress_label.pack(pady=10)

        def browse_directory():
            directory = filedialog.askdirectory()
            if directory:
                organize_files(directory, progress_var, progress_label, file_organizer_window)
                messagebox.showinfo("File Organizer", "Files have been organized.")

        browse_button = tk.Button(file_organizer_window, text="Browse Directory", command=browse_directory, font=("Arial", 14))
        browse_button.pack(pady=10)

        file_organizer_window.mainloop()

class VoiceInputThread(QThread):
    recognized_text = pyqtSignal(str)

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                self.recognized_text.emit(text)
            except sr.UnknownValueError:
                self.recognized_text.emit("Sorry, I did not understand that.")
            except sr.RequestError:
                self.recognized_text.emit("Sorry, there was an error with the speech recognition service.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    chatbot = ChatbotWindow()
    chatbot.show()
    sys.exit(app.exec_())
