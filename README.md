# Azure_Dictation
This program uses the Azure Cognitive Services Speech API to transcribe audio files into text. The program prompts the user to enter their speech subscription key, region, and language. The program then prompts the user to select an audio input file. The program then transcribes the audio file into text and saves the text to a file.

## Features

- Load or create a new configuration that stores the user's Speech Service subscription key, region, and the language of the audio file.
- Prompt the user to select an audio input file using a GUI file picker.
- Continuously recognize speech in the audio file and write the transcribed text to a text file.
- Handle various speech recognition events, such as recognizing, recognized, canceled, and session started/stopped.

## Prerequisites

- Python 3.6+
- Azure subscription
- Speech Service subscription key
- Region for the Speech Service
- Language of the audio file
- Tkinter for GUI file picker


## Getting Started
Clone this repository to your local machine or download the script file (script.py).

Obtain an Azure Cognitive Services subscription key and endpoint. You can create a free trial subscription on the Azure portal.

Create a configuration file (config.json) in the same directory as the script, with the following structure:


```
  "subscription_key": "YOUR_SUBSCRIPTION_KEY",
  "region": "YOUR_REGION",
  "language": "LANGUAGE_CODE"
```

Replace YOUR_SUBSCRIPTION_KEY with your Azure subscription key, YOUR_REGION with the region of your subscription, and LANGUAGE_CODE with the language code of the audio input file (e.g., "en-US" for English-US).

## Running the Script
- Open a terminal or command prompt.
- Navigate to the directory where the script is located.
- Run the script using the command: python script.py
- You will be prompted to create a new configuration or load an existing one. Enter either new or load.
- If you choose new, enter your speech subscription key, region, and language when prompted. The configuration will be saved to config.json.
- If you choose load, the configuration will be loaded from config.json if it exists; otherwise, an error will be displayed.
- A file dialog window will open. Select the audio input file (supported formats: WAV, MP3, or any other audio format).
- The script will start transcribing the audio in real-time and display recognition progress and results in the terminal.
- Once the transcription is complete, the recognized text will be saved to a text file with the same name as the input file but with a .txt extension.

## Additional Information
- If you need to change the configuration in the future, you can edit the config.json file manually or run the script again and choose the new option to overwrite the existing configuration.
- The script uses the speechsdk library from the azure-cognitiveservices-speech package to interact with the Azure Speech-to-Text API.
- Event handlers are defined to handle various events during the speech recognition process, such as recognizing partial and final results, session start and stop, and cancellation.
- The script utilizes the tkinter library to display a file dialog for selecting the audio input file.
- The recognized text is appended to the output file in real-time. If you run the script multiple times, the output file will contain the combined transcriptions of all the audio files processed.
- You can stop the script by closing the terminal or by pressing Ctrl+C.
- Please note that using the Azure Cognitive Services Speech-to-Text API may incur charges based on your Azure subscription and usage. Refer to the Azure pricing documentation for more details.
