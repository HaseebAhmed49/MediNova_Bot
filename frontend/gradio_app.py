#VoiceBot UI with Gradio
import os
import requests
import gradio as gr


API_BASE_URL = "http://localhost:8000"  # Replace with your actual backend URL if deployed

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def gradio_transcribe(audio_filepath, stt_model, GROQ_API_KEY):
    response = requests.get(
        "http://localhost:8000/transcribe_audio",
        params={
            "stt_model": stt_model,
            "audio_filepath": audio_filepath.name,
            "GROQ_API_KEY": GROQ_API_KEY
        }
    )
    return response.text

def analyze_image(query, model, image):
    if image is None:
        return "Please upload an image."

    # Step 1: Send image to /encode_image
    with open(image.name, "rb") as f:
        files = {"image": f}
        res = requests.post(f"{API_BASE_URL}/encode_image", files=files)

    if res.status_code != 200:
        return f"Error encoding image: {res.text}"

    encoded_image = res.json()["encoded_image"]

    # Step 2: Send query, model, and encoded image to /analyze_image_with_query
    res2 = requests.post(
        f"{API_BASE_URL}/analyze_image_with_query",
        json={"query": query, "model": model, "encoded_image": encoded_image}
    )

    if res2.status_code == 200:
        return res2.json()["response"]
    else:
        return f"Error analyzing image: {res2.text}"

FASTAPI_URL = "http://localhost:8000/text_to_speech_elevenlabs"
def call_elevenlabs_tts(input_text):
    output_filepath = "output.mp3"  # Local save location

    payload = {
        "input_text": input_text,
        "output_filepath": output_filepath
    }

    response = requests.post(FASTAPI_URL, params=payload)

    if response.status_code == 200:
        return output_filepath
    else:
        return f"Error: {response.text}"

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = gradio_transcribe(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image(query=system_prompt+speech_to_text_output, image=image_filepath, model="meta-llama/llama-4-scout-17b-16e-instruct")
    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = call_elevenlabs_tts(input_text=doctor_response) 

    return speech_to_text_output, doctor_response, voice_of_doctor


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)

#http://127.0.0.1:7860