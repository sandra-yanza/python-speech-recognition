import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.ttk import Combobox
import pyttsx3
import os
import pyaudio #used to use the mic
import wave #to use .WAV files
from playsound import playsound
from DbCode.db import DB, SpeechToAudio
from tkinter import messagebox


# Class with the business logic
class SpeechBussiness():
    def __init__(self):
        self.years:int = 0
    
    # Method to detect Speech with the Microphone and record the audio. It creates a WAV file.
    # This method receives the name of the file and the duration in seconds
    # pip install PyAudio: cross-platform audio input/output library. Used to detect audible events in python.
    # pip install Wave:  used to read and write wav files.
    def record_audio(self,filename,duration): 

        CHUNK = 1024 # audio size in bytes
        FORMAT = pyaudio.paInt16 # audio format
        CHANNELS = 1 # It only has 1 input channel, which is the microphone.
        RATE = 44100 # Number of samples (single data point representing the amplitude of an audio signal at a specific point in time.)

        audio = pyaudio.PyAudio()  # create a PyAudio instance for audio input and output
        self.message=tk.StringVar()
        self.message=""

        stream = audio.open(format=FORMAT, # abre el archivo para grabar los valores anteriores
                        channels=CHANNELS,
                        rate=RATE,
                        input=True, #este indica que se va a hacer un input con microfono
                        frames_per_buffer=CHUNK)

        print("Recording...")

        frames = [] # collection of samples, inicialmente vacia y se llena leyendo el stream

        # We are handling exceptions
        try:

            for i in range(0, int(RATE / CHUNK * int(duration))): #RATE / CHUNK = chunks number per second and * duration to have the total chunks per record
                data = stream.read(CHUNK)  # in each loop the value is taken and then added to the frame
                frames.append(data)

            print("Finished recording.")  #finish record

            stream.stop_stream() # the stream stops
            stream.close() # the stream is closed
            audio.terminate() # end the pyAudio

            root_directory = "./audios_recorded"  # Change this to your desired root directory
            filename_full = f"{root_directory}/{filename}.wav"
            print(filename_full)

            # We are saving the audio
            wf = wave.open(filename_full, 'wb') # We use the WAVE library to open the audio and in this case write binary
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            # the previous 3 set the audio values ​​using WAVE functions, all the set
            wf.writeframes(b''.join(frames)) # We use the frames that were included in the recording part and remain in the audio file
            # the 'b' is for converting to bytes before writing it to the audio
            wf.close() # the new wav file is closed
        
        # We are handling exceptions
        except Exception as e:
                self.message = str(e)
                print("Error in record_audio")

        return self.message
    

    # Method to play the audio file and convert the Speech to Text.
    # pip install playsound: used to play a sound file (. wav or . mp3) from a given file path.
    # pip install SpeechRecognition: used to convert speech to text in python using Google's Speech Recognition module.
    def audio_to_text(self,filename):
   
        root_directory = "./audios_recorded"  # Change this to your desired root directory
        filen = f"{root_directory}/{filename}"
        print("directory: " + filename)

        self.text_play=tk.StringVar()
        self.text_play="Could not play the audio"

        try:
            playsound(filen)
            print('playing sound using  playsound')
        except Exception as e:
            self.message = str(e)
            print("Error in playing sound using playsound: " + str(e))

        self.text_recognize=tk.StringVar()
        self.text_recognize="Could not recognize the audio"

        r = sr.Recognizer()

        with sr.AudioFile(filen) as source:
            audio_data = r.record(source)
            try:
                textFile = r.recognize_google(audio_data)
                print("Text file: " + textFile)
                self.text_recognize = textFile

            except sr.UnknownValueError as e:
                print("Could not recognize the audio")
                print(e)
                self.text_recognize="Error: Could not recognize the audio"
            
            except sr.RequestError as e:
                print(e)
                self.text_recognize="Error: Could not recognize the audio"

        # Saving the record in the database
        file_blob = self.convert_into_binary(filen)
        speechToAudio = SpeechToAudio(filename, file_blob, self.text_recognize)
        db_file = './SpeechRecognition/DbCode/audios.db'
        db = DB(db_file)
        db.insert(speechToAudio)

        return self.text_recognize
    
    # Method to convert the contents of a file to binary
    def convert_into_binary(self,file_path):
        with open(file_path, 'rb') as file:
            binary = file.read()
        return binary
    

    # Method to convert Text to Speech
    # pip install pyttsx3: used to convert text to speech
    def play_audio_text_speech(self,gender,speed,text): 

        print(gender)
        print(speed)
        print(text)
        e=pyttsx3.init()
        v = e.getProperty('voices')

        # Setting the property RATE: change the speed of the speech
        if (speed == 'Fast'):
            e.setProperty('rate', 300)
        elif (speed == 'Normal'):
            e.setProperty('rate', 150)
        else:
            e.setProperty('rate', 50)

        # Setting the property VOICE: change the voice of the engine, the default is the voice of a male.
        if (gender == 'Male'):
            e.setProperty('voice', v[0].id)
        else:
            e.setProperty('voice', v[1].id)

        # Setting the property VOLUME: change the volume of the sound.
        e.setProperty('volume', (100) / 100)
        e.say(text)
        e.runAndWait()

    # Method to generate a file and download
    def download_file_text_speech(self,gender,speed,text):
        e=pyttsx3.init()
        v = e.getProperty('voices')

        if (speed == 'Fast'):
            e.setProperty('rate', 300)
        elif (speed == 'Normal'):
            e.setProperty('rate', 150)
        else:
            e.setProperty('rate', 50)

        if (gender == 'Male'):
            e.setProperty('voice', v[0].id)
        else:
            e.setProperty('voice', v[1].id)
        e.setProperty('volume', (100) / 100)

        path=filedialog.askdirectory()
        os.chdir(path)
        e.save_to_file(text,'Audio_File.mp3')
        e.runAndWait()
        messagebox.showinfo("Download Audio", "File has been created!")

    def playAudio(self,filename):
        root_directory = "audios_recorded" 
        filen = f"{root_directory}/{filename}"
        print("directory: " + filen)

        self.text_play=tk.StringVar()
        self.text_play="Could not play the audio"

        try:
            playsound(filen)
            print('playing sound using  playsound')
        except Exception as e:
            self.message = str(e)
            print("Error in playing sound using playsound: " + str(e))




