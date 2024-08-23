import sys
import google.generativeai as palm
import configparser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QLineEdit, QPushButton, QTextEdit, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class PalmApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Generative AI Diagnostic Assistant')
        self.setGeometry(100, 100, 800, 600)

        # Set up the central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Set the background color and gradient
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #e0e0e0;
                font-family: Arial;
            }
            QLabel {
                color: #e0e0e0; /* Default text color */
            }
            QLabel.question {
                color: #ffffff; /* White text color for questions */
                font-weight: bold;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #ff5722;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff7043;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                color: #e0e0e0;
            }
            QMessageBox {
                background-color: #121212;
                color: #e0e0e0;
            }
        """)

        # Title Label
        self.title_label = QLabel('Generative AI Diagnostic Assistant')
        self.title_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Input layout for patient responses
        input_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)

        # Label for displaying questions
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("QLabel {color: #ffffff; font-weight: bold;}")
        input_layout.addWidget(self.question_label)

        # Text field for user input
        self.response_input = QLineEdit()
        self.response_input.setPlaceholderText('Enter response to the question here...')
        self.response_input.setMinimumHeight(40)
        input_layout.addWidget(self.response_input)

        # Button to submit response
        self.submit_button = QPushButton('Submit Response')
        self.submit_button.clicked.connect(self.submit_response)
        input_layout.addWidget(self.submit_button)

        # Button to finalize and generate results
        self.generate_button = QPushButton('Generate Diagnosis')
        self.generate_button.clicked.connect(self.generate_diagnosis)
        input_layout.addWidget(self.generate_button)

        # Response output
        self.response_output = QTextEdit()
        self.response_output.setReadOnly(True)
        main_layout.addWidget(self.response_output)

        # Status Label
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Read configuration and set up API key
        self.setup_api_key()

        # Load rules
        self.rules = self.load_rules()

        # Initialize a list to store responses
        self.responses = []

        # Initialize current question index
        self.current_question_index = 0
        self.questions = [
            "What are the patient's primary symptoms?",
            "How long has the patient been experiencing these symptoms?",
            "Does the patient have a history of smoking?",
            "Have you experienced any symptoms like coughing up blood (hemoptysis) or changes in the color of your sputum?",
            "Has the patient experienced shortness of breath or chest pain?",
            "Are there any known environmental exposures or occupational hazards?",
            "Does the patient have any existing respiratory or other chronic conditions?",
            "Has the patient experienced any recent weight loss?",
            "Do you have any current or past history of lung diseases such as chronic bronchitis or emphysema?",
            "Do you have any other symptoms like fatigue, fever, or night sweats?",
            "What diagnostic tests have been performed so far?"
        ]

        # Display the first question
        self.display_next_question()

    def setup_api_key(self):
        # Read configuration file
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Retrieve API key from the config file
        self.api_key = config.get('API', 'gemini_api_key', fallback=None)
        
        if not self.api_key:
            self.show_message("Error", "API key is missing from the configuration file.", QMessageBox.Critical)
        else:
            # Configure the API key for the palm library
            palm.configure(api_key=self.api_key)

    def load_rules(self):
        try:
            with open('rules.txt', 'r') as file:
                rules = file.read().strip()
            return rules
        except FileNotFoundError:
            self.show_message("Error", "The rules.txt file is missing.", QMessageBox.Critical)
            return ""

    def display_next_question(self):
        if self.current_question_index < len(self.questions):
            self.question_label.setText(self.questions[self.current_question_index])
        else:
            self.question_label.setText("All questions answered. Click 'Generate Diagnosis' to proceed.")

    def submit_response(self):
        response = self.response_input.text()
        if response:
            self.responses.append(response)
            self.response_input.clear()
            self.current_question_index += 1

            # If there are more questions, display the next one
            self.display_next_question()
        else:
            self.show_message("Input Error", "Please enter a response before submitting.", QMessageBox.Warning)

    def generate_diagnosis(self):
        if len(self.responses) < len(self.questions):
            self.show_message("Incomplete", "Please answer all questions before generating the diagnosis.", QMessageBox.Warning)
            return
        
        # Combine the rules with the responses
        responses_summary = "\n".join(f"{q} {a}" for q, a in zip(self.questions, self.responses))
        combined_prompt = f"{self.rules}\n\nPatient Responses:\n{responses_summary}"

        # Initialize the generative model
        model = palm.GenerativeModel('gemini-1.5-flash')
        
        # Generate content using the model
        try:
            response = model.generate_content(combined_prompt)
            
            # Extract and display the generated text
            candidates = response.candidates
            if candidates:
                content = candidates[0].content.parts[0].text
                self.response_output.setText(content)
            else:
                self.response_output.setText("No content generated.")
        
        except Exception as e:
            self.show_message("Generation Error", f"An error occurred: {e}", QMessageBox.Critical)

    def show_message(self, title, message, icon):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("QMessageBox {background-color: #121212; color: #e0e0e0;}")
        msg_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PalmApp()
    window.show()
    sys.exit(app.exec_())
