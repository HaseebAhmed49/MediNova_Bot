from fastapi import APIRouter
import os
from gtts import gTTS
import subprocess
import platform
import elevenlabs
from elevenlabs.client import ElevenLabs

router = APIRouter()
ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

def play_audio(output_filepath: str):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

@router.post("/text_to_speech_gtts")
def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    play_audio(output_filepath)
    return {"status": "success", "method": "gTTS"}

@router.post("/text_to_speech_elevenlabs")
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        output_format="mp3_22050_32",
        text= input_text,
        model_id="eleven_turbo_v2_5",
        )
    elevenlabs.save(audio, output_filepath)
    play_audio(output_filepath)
    return {"status": "success", "method": "ElevenLabs"}