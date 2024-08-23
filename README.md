# Generative AI Diagnostic Assistant

## Overview

The Generative AI Diagnostic Assistant is a Python application designed to aid in lung cancer diagnosis using Google's Gemini 1.5 model. The application provides a user-friendly interface built with PyQt5, where users can answer a series of diagnostic questions. The responses are processed and analyzed using a generative AI model to generate insights.

## Features

- **User Interface**: Modern, dark-themed GUI with PyQt5.
- **Questionnaire**: Series of diagnostic questions for comprehensive data collection.
- **Generative AI**: Utilizes the Gemini 1.5 model to generate diagnostic insights based on user responses and predefined rules.
- **Configuration**: Supports dynamic API key configuration and custom diagnostic rules.

## Requirements

- Python 3.x
- PyQt5
- Google Generative AI (palm)
- Configuration file: `config.ini`
- Rules file: `rules.txt`

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/paramchauhan101/Cancer-Diagnosis-with-Generative-AI-Gemini-and-Python.git
    cd Cancer-Diagnosis-with-Generative-AI-Gemini-and-Python
    ```

2. **Install Dependencies**

    Ensure you have `pip` installed, then run:

    ```bash
    pip install PyQt5 google-generativeai
    ```

3. **Set Up Configuration**

    Create a `config.ini` file in the project directory with the following content:

    ```ini
    [API]
    gemini_api_key = YOUR_API_KEY_HERE
    ```

4. **Create Rules File**

    Create a `rules.txt` file in the project directory with your diagnostic rules.

## Usage

1. Run the application:

    ```bash
    python your_script_name.py
    ```

2. The application will prompt you to answer a series of questions. Provide responses and click "Submit Response" to proceed.

3. After answering all questions, click "Generate Diagnosis" to receive the generated diagnostic insights.

## Future and Benefits of AI in Diagnostics

- **Improved Accuracy**: AI models can analyze vast amounts of data quickly and accurately, enhancing diagnostic precision.
- **Early Detection**: AI can identify patterns and anomalies that may be missed by human eyes, leading to earlier disease detection.
- **Personalized Treatment**: By integrating AI with patient data, more personalized and effective treatment plans can be developed.
- **Cost Efficiency**: Automating diagnostic processes can reduce healthcare costs and free up medical professionals for more critical tasks.
