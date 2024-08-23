# Chatbot with File Organizer and Voice Input
Welcome to the MGM Chatbot project! This application provides a chatbot interface with features such as voice input/output and a file organizer to help you manage your files efficiently. Built using PyQt5, Tkinter, and various Python libraries, this project aims to offer both convenience and functionality.

# Features
Chatbot Interface: A friendly and interactive chatbot to assist with various tasks.
Voice Input and Output: Speak to the chatbot and listen to its responses using speech recognition and text-to-speech capabilities.
File Organizer: Organize files in your selected directory based on their types (e.g., Images, Documents, Videos, etc.).
Login Functionality: Secure login system to access the chatbot functionalities.
Installation
To set up the project, follow these steps:

Clone the Repository:
```
git clone https://github.com/yourusername/CHATBOT.git
cd CHATBOT
```
Install Required Dependencies:
Ensure you have Python 3.7+ installed. Use pip to install the necessary packages:

```
pip install PyQt5 pyttsx3 SpeechRecognition rich
```
Run the Application:
```
python ui.py
```

# Usage

Login: Start the application. A login window will appear. Use the default credentials:
Username: admin
Password: admin@123

Chatbot Interaction:
Enter your messages in the input field and click "Send" or press Enter.
Enable "Voice Output" to hear the chatbot's responses.
Use the "Speak" button to provide voice input.

File Organizer:
Click on the "Open File Organizer" button to launch the file organizer window.
Select a directory and click "Organize" to sort files into predefined categories.
File Organizer Categories
The files are organized into the following categories:
Images: jpg, jpeg, png, gif, bmp <br>
Documents: txt, doc, docx, pdf, xls, xlsx, ppt, pptx <br>
Videos: mp4, avi, mov, mkv <br>
Music: mp3, wav, flac, aac <br>
Archives: zip, rar, 7z, tar, gz <br>
Executables: exe, msi, bat <br>
Programming: py, java, c, cpp, h, html, css, js <br>
Others: Any other file types <br>

Project Structure
ui.py: Main GUI code that integrates chatbot and file organizer functionalities.
brain.py: Logic for chatbot interaction using the LLAMA3 AI model, handling conversation history.
webscout.py: Not included here but assumed to be a module for the LLAMA3 AI interface.
Dependencies
PyQt5: For creating the main GUI.
Tkinter: For the file organizer GUI.
pyttsx3: For text-to-speech functionality.
SpeechRecognition: For capturing and processing voice input.
rich: For improved console output during development.
LLAMA3: Assumed to be a custom or third-party AI model interface used in brain.py.
Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Make sure to follow the existing code style and include documentation for any new features.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Thanks to the developers of PyQt5, Tkinter, pyttsx3, SpeechRecognition, and other libraries used in this project.
The LLAMA3 AI model used for chatbot responses.
