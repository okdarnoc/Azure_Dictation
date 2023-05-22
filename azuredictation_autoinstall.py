import subprocess
import importlib

def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.call(['pip', 'install', package])
    finally:
        globals()[package] = importlib.import_module(package)

install_and_import('os')
install_and_import('time')
install_and_import('tkinter')
install_and_import('json')
install_and_import('azure.cognitiveservices.speech')


import os
import time
import tkinter as tk
from tkinter import filedialog
import json
import azure.cognitiveservices.speech as speechsdk

# Set up config file path
config_file_path = "config.json"

# Define functions to prompt user for configuration and save/load configuration from file
def save_config(subscription_key, region, language):
    config = {"subscription_key": subscription_key, "region": region, "language": language}
    with open(config_file_path, "w") as f:
        json.dump(config, f)

def load_config():
    try:
        with open(config_file_path, "r") as f:
            config = json.load(f)
            subscription_key = config["subscription_key"]
            region = config["region"]
            language = config["language"]
            return subscription_key, region, language
    except FileNotFoundError:
        return None

def prompt_config():
    print("Would you like to create a new configuration or load an existing one?")
    while True:
        choice = input("Enter 'new' or 'load': ")
        if choice == "new":
            subscription_key = input("Enter your speech subscription key: ")
            region = input("Enter your speech region: ")
            language = input("Enter the language of the audio input file: ")
            save_config(subscription_key, region, language)
            break
        elif choice == "load":
            config = load_config()
            if config is not None:
                subscription_key, region, language = config
                break
            else:
                print("Configuration file not found.")
        else:
            print("Invalid choice.")
    
    return subscription_key, region, language

# Prompt user for configuration
subscription_key, region, language = prompt_config()

# Prompt user to select audio input file
root = tk.Tk()
root.withdraw()
input_file_path = filedialog.askopenfilename(title="Select audio input file", filetypes=(("WAV files", "*.wav"), ("MP3 files", "*.mp3"), ("All files", "*.*")))

# Set up output file path
input_file_name = os.path.basename(input_file_path)
output_file_name = os.path.splitext(input_file_name)[0] + ".txt"

# Set up speech recognition config and audio config
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
speech_config.speech_recognition_language = language
audio_config = speechsdk.audio.AudioConfig(filename=input_file_path)

# Create speech recognizer object and define event handlers
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
done = [False]

def stop_cb(evt):
    print('CLOSING on {}'.format(evt))
    speech_recognizer.stop_continuous_recognition()
    done[0] = True

speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))

def recognized_handler(evt):
    print('RECOGNIZED: {}'.format(evt))
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        with open(output_file_name, 'a', encoding='utf-8') as output_file:
            output_file.write(evt.result.text + '\n')

speech_recognizer.recognized.connect(recognized_handler)

speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))

def canceled_handler(evt):
    print('CANCELED: {}'.format(evt))
    if evt.reason == speechsdk.CancellationReason.Error:
        print('Error details: {}'.format(evt.error_details))
    if evt.reason == speechsdk.CancellationReason.EndOfStream:
        stop_cb(None)

speech_recognizer.canceled.connect(canceled_handler)

speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

speech_recognizer.start_continuous_recognition()

while not done[0]:
    time.sleep(0.5)

