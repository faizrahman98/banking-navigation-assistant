import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write
import os
# import tempfile
from openai import OpenAI
import elevenlabs
from google.cloud import speech
import io



# Parameters for recording
duration = 5  # seconds
fs = 44100  # Sample rate
channels = 1  # Mono recording

# os.environ['OPENAI_API_KEY'] = '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'

elevenlabs.set_api_key("8d4a6f35ef4b20c35358cb8f47a17fc5")

def record_audio():
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    print("Finished recording.")
    return recording


def save_audio(audio, fs, filename="recording.wav"):
    # Convert to 16-bit data
    audio = np.int16(audio * 32767)
    write(filename, fs, audio)
    return filename

def transcribe_audio(file_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= '../config.json'
    # create client instance 
    client = speech.SpeechClient()

    #the path of your audio file
    file_name = file_path
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation=True,
        audio_channel_count=1,
        language_code="en-US",
    )

    # Sends the request to google to transcribe the audio
    response = client.recognize(request={"config": config, "audio": audio})
    # Reads the response
    trans_text = None
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
        trans_text = result.alternatives[0].transcript
    return "Transcript: {}".format(trans_text)





def generate_answer(prompt): 
    
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Imagine you are embedded inside a banking app built for the elderly. The app consists of 6 sections 0:Default 1:Balance, 2:Expenses, 3:Spending, 4:Credit , 5:Transactions. The first letter of the answer should be [0]-[5] based on the similarity of the prompt to any of the 5 sections. Dont mention the name of the section. Your task is to help them as they can't deal with the complexity of navigating the UI of the app. So answer precisely in less than 100 words and answer only banking related questions."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def text_speech(answer):
    voice = elevenlabs.Voice(
        voice_id = "ZQe5CZNOzWyzPSCn5a3c",
        settings = elevenlabs.VoiceSettings(
            stability = 0,
            similarity_boost = 0.75
        )
    )
 
    audio = elevenlabs.generate(
        text = answer,
        voice = voice
    )
 
    # elevenlabs.save(audio, "audio.mp3")
    return audio
