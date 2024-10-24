# PoC: Audio Replacement with AI-Generated Voice

## Project Overview
This Proof of Concept (PoC) demonstrates the replacement of audio in a video file with an AI-generated voice. The process involves transcribing the original audio, correcting the transcript using GPT-4, and generating corrected voice using Google Text-to-Speech (TTS).

## Key Features
- **Audio Transcription**: Transcribes the existing audio track in a video.
- **Text Correction**: Enhances the accuracy of the transcribed text using GPT-4.
- **AI Voice Generation**: Uses Google TTS Journey voice model to generate the corrected voice.
- **Seamless Audio Replacement**: Replaces the original audio with the generated voice in the video.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.x
- Required Python libraries (install using the instructions below)
- Google Cloud credentials for accessing the Text-to-Speech API
- OpenAI API key for GPT-4 access

## Installation

1. Clone the repository
   git clone <repository-url>
   cd <repository-folder>

2. Install dependencies: Run the following command to install the necessary Python libraries.
    pip install -r requirements.txt


## Usage
    To run the PoC, execute the following command:
        python main.py --input_video <path-to-input-video> --output_video <path-to-output-video>

## Example 
    python main.py --input_video sample_video.mp4 --output_video output_video.mp4
