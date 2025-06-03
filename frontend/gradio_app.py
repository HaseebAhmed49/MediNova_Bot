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

# Login function
def login(username, password):
    print(f"Attempting to log in with username: {username} and password: {password}")
    response = requests.post("http://localhost:8000/auth/login", data={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json().get("access_token")
        return f"Login successful! Token: {token}"
    else:
        return f"Error: {response.json().get('detail', 'Login failed')}"

# Register function
def register(username, password):
    response = requests.post(f"{API_BASE_URL}/auth/register", data={"username": username, "password": password})
    if response.status_code == 200:
        return "Registration successful!"
    else:
        return f"Error: {response.json().get('detail', 'Registration failed')}"

def gradio_transcribe(audio_filepath, stt_model, GROQ_API_KEY):
    response = requests.get(f"{API_BASE_URL}/voice_of_patient/transcribe_audio",
        params={
            "stt_model": stt_model,
            "audio_filepath": audio_filepath,
            "GROQ_API_KEY": GROQ_API_KEY
        }
    )
    return response.text

def analyze_image(query, model, image_path):
    if image_path is None:
        return "Please upload an image."

    # Step 1: Send image to /encode_image
    res = requests.get(f"{API_BASE_URL}/brain_of_the_assistant/encode_image", 
        params={
            "image_path": image_path
        }
    )

    if res.status_code != 200:
        return f"Error encoding image: {res.text}"

    encoded_image = res.json()["encoded_image"]

    # Step 2: Send query, model, and encoded image to /analyze_image_with_query
    res2 = requests.get(
        f"{API_BASE_URL}/brain_of_the_assistant/analyze_image_with_query",
        params={"query": query, "model": model, "encoded_image": encoded_image}
    )

    if res2.status_code == 200:
        return res2.json()["response"]
    else:
        return f"Error analyzing image: {res2.text}"

def call_elevenlabs_tts(input_text):
    output_filepath = "output.mp3"  # Local save location

    response = requests.get(f"{API_BASE_URL}/voice_of_doctor/text_to_speech_elevenlabs", params={
        "input_text": input_text,
        "output_filepath": output_filepath
        }
    )

    if response.status_code == 200:
        return output_filepath
    else:
        return f"Error: {response.text}"

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = gradio_transcribe(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
        )    
    doctor_response = analyze_image(
        query=system_prompt+speech_to_text_output, 
        image_path=image_filepath, 
        model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    voice_of_doctor = call_elevenlabs_tts(input_text=doctor_response)
    return speech_to_text_output, doctor_response, voice_of_doctor
    # return speech_to_text_output, doctor_response

# Create the interfaces
login_interface = gr.Interface(
    fn=login,
    inputs=[
        gr.Textbox(label="Username"),
        gr.Textbox(label="Password", type="password")  # Corrected password input
    ],
    outputs=[
        gr.Textbox(label="Login Status")
    ],
    title="Login"
)

register_interface = gr.Interface(
    fn=register,
    inputs=[
        gr.Textbox(label="Username"),
        gr.Textbox(label="Password", type="password")  # Corrected password input
    ],
    outputs=[
        gr.Textbox(label="Registration Status")
    ],
    title="Register"
)

main_interface = gr.Interface(
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

# Combine interfaces into a tabbed layout
app = gr.TabbedInterface(
    interface_list=[login_interface, register_interface, main_interface],
    tab_names=["Login", "Register", "AI Doctor"]
)

app.launch(debug=True)