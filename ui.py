import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QDialog, QFormLayout, QLabel, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import pyttsx3
import speech_recognition as sr
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
        response = Main_Brain(user_message)  # Use Main_Brain to generate the response
        self.chat_display.append(f"<p style='color: #66cc99;'><b>Chatbot:</b> {response}</p>")
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.End)
        self.chat_display.setTextCursor(cursor)

        # Speak response if voice output is enabled
        if self.voice_output_checkbox.isChecked():
            self.tts_engine.say(response)
            self.tts_engine.runAndWait()

    def start_file_organizer(self):
        organizer_root = tk.Tk()
        organizer_root.title("File Organizer")

        frame = ttk.Frame(organizer_root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        directory_label = ttk.Label(frame, text="Select Directory:")
        directory_label.grid(row=0, column=0, sticky=tk.W)

        directory_entry = ttk.Entry(frame, width=50)
        directory_entry.grid(row=0, column=1, padx=5, pady=5)

        browse_button = ttk.Button(frame, text="Browse", command=lambda: browse_directory(directory_entry))
        browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Create progress_var and progress_label here
        progress_var = tk.IntVar()
        progress_label = ttk.Label(frame, text="Progress: 0 / 0")
        progress_label.grid(row=2, column=1, pady=5)

        organize_button = ttk.Button(frame, text="Organize", command=lambda: organize(directory_entry.get(), progress_var, progress_label, organizer_root))
        organize_button.grid(row=1, column=1, pady=10)

        organizer_root.mainloop()

# Voice Input Thread
class VoiceInputThread(QThread):
    recognized_text = pyqtSignal(str)

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio_data)
                self.recognized_text.emit(text)
            except sr.UnknownValueError:
                self.recognized_text.emit("Sorry, I didn't catch that.")
            except sr.RequestError:
                self.recognized_text.emit("Sorry, there was an error with the speech recognition service.")

# Login Dialog
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 150)

        layout = QFormLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.authenticate)

        layout.addRow(QLabel("Username:"), self.username_input)
        layout.addRow(QLabel("Password:"), self.password_input)
        layout.addRow(self.login_button)

        self.setLayout(layout)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin@123":
            self.accept()
        else:
            self.reject()

# Helper functions for File Organizer
def browse_directory(entry):
    directory = filedialog.askdirectory()
    if directory:
        entry.delete(0, tk.END)
        entry.insert(0, directory)

def organize(directory, progress_var, progress_label, root_window):
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Invalid directory path")
        return
    organize_files(directory, progress_var, progress_label, root_window)
    messagebox.showinfo("Success", "Files organized successfully")

# Main Function
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # Show login dialog
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        chatbot_window = ChatbotWindow()
        chatbot_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()
