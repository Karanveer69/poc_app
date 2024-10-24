import streamlit as st
import moviepy.editor as mp
import openai
import requests
import json
from google.cloud import speech, texttospeech
from io import BytesIO
import os

def extract_audio_from_video(video_file):
    video = mp.VideoFileClip(video_file)
    audio_path = "extracted_audio.wav"
    video.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_file_path):
    client = speech.SpeechClient()
    with open(audio_file_path, 'rb') as audio_file:
        audio_content = audio_file.read()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )
    response = client.recognize(config=config, audio=audio)
    transcription = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcription

def correct_transcription(transcription):
    openai.api_key = os.getenv("22ec84421ec24230a3638d1b51e3a7d")  # Replace with your OpenAI API key from .env
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Correct this text for grammatical errors and remove fillers."},
            {"role": "user", "content": transcription}
        ]
    )
    corrected_text = response['choices'][0]['message']['content']
    return corrected_text

def text_to_speech(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-JennyNeural"  # Journey voice model or any available voice
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    output_path = "corrected_audio.mp3"
    with open(output_path, 'wb') as out:
        out.write(response.audio_content)
    return output_path

def replace_audio_in_video(video_path, new_audio_path):
    video = mp.VideoFileClip(video_path)
    audio = mp.AudioFileClip(new_audio_path)
    final_video = video.set_audio(audio)
    output_video_path = "final_video_with_new_audio.mp4"
    final_video.write_videofile(output_video_path)
    return output_video_path

def main():
    st.title("Replace Video Audio with AI Generated Voice")

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
    if uploaded_file:
        video_path = os.path.join("temp_video.mp4")
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())
        
        st.video(uploaded_file)
        
        
        audio_path = extract_audio_from_video(video_path)
        st.write("Audio extracted from video.")
        
        
        transcription = transcribe_audio(audio_path)
        st.write(f"Transcription: {transcription}")
        
        
        corrected_text = correct_transcription(transcription)
        st.write(f"Corrected Transcription: {corrected_text}")
        
        
        corrected_audio_path = text_to_speech(corrected_text)
        st.write(f"Corrected Audio generated at: {corrected_audio_path}")
        
        
        final_video_path = replace_audio_in_video(video_path, corrected_audio_path)
        st.write(f"Final video saved at: {final_video_path}")
        st.video(final_video_path)

if __name__ == "__main__":
    main()
