#VoiceBot UI with Gradio
import os
import requests
import gradio as gr


API_BASE_URL = "http://localhost:8000"  # Replace with your actual backend URL if deployed

# Global variable to store the token
user_token = None

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

# Login function
def login(username, password):
    global user_token
    response = requests.post(f"{API_BASE_URL}/auth/login", data={"username": username, "password": password})
    if response.status_code == 200:
        user_token = response.json().get("access_token")
        return "Login successful! You can now access the AI Doctor tab.", gr.update(visible=True)
    else:
        return f"Error: {response.json().get('detail', 'Login failed')}", gr.update(visible=False)

# Logout function
def logout():
    global user_token
    user_token = None
    return (
        gr.update(visible=False),  # Hide logout button
        gr.update(value=""),       # Clear login username
        gr.update(value=""),       # Clear login password
        gr.update(value="You have been logged out successfully. Please login again to access AI Doctor."),  # Login status
        gr.update(selected="login_tab")  # Switch to login tab
    )

# Register function
def register(username, password):
    response = requests.post(f"{API_BASE_URL}/auth/register", data={"username": username, "password": password})
    if response.status_code == 200:
        return "Registration successful! Please login to access AI Doctor."
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
    
def access_denied():
    speech_to_text_output = "Access Denied"
    doctor_response = "Apologies, I cant suggest you. Please register or login into the software. You need to log in to access AI Doctor."
    voice_of_doctor = call_elevenlabs_tts(input_text=doctor_response)
    return speech_to_text_output, doctor_response, voice_of_doctor

def process_inputs(audio_filepath, image_filepath):
    if not user_token:
        return access_denied()

    # Add token to headers for authenticated requests
    headers = {"Authorization": f"Bearer {user_token}"}
    response = requests.get(f"{API_BASE_URL}/auth/ai_doctor", headers=headers)
    if response.status_code == 200:
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
    else:
        return access_denied()

# Create the Gradio Blocks interface for better control
with gr.Blocks(title="AI Doctor Application") as app:
    # Header with title and logout button
    with gr.Row():
        with gr.Column(scale=4):
            gr.Markdown("# AI Doctor Application")
        with gr.Column(scale=1, min_width=120):
            logout_btn = gr.Button("Logout", variant="secondary", visible=False, size="sm")
    
    with gr.Tabs() as tabs:
        with gr.Tab("Login", id="login_tab"):
            gr.Markdown("## Login to Access AI Doctor")
            with gr.Column():
                login_username = gr.Textbox(label="Username", placeholder="Enter your username")
                login_password = gr.Textbox(label="Password", type="password", placeholder="Enter your password")
                login_btn = gr.Button("Login", variant="primary")
                login_status = gr.Textbox(label="Login Status", interactive=False)
        
        with gr.Tab("Register", id="register_tab"):
            gr.Markdown("## Register New Account")
            with gr.Column():
                reg_username = gr.Textbox(label="Username", placeholder="Choose a username")
                reg_password = gr.Textbox(label="Password", type="password", placeholder="Choose a password")
                register_btn = gr.Button("Register", variant="primary")
                register_status = gr.Textbox(label="Registration Status", interactive=False)
        
        with gr.Tab("AI Doctor", id="doctor_tab"):
            gr.Markdown("## AI Doctor with Vision and Voice")
            
            # Check login status for AI Doctor tab
            with gr.Column():
                login_check = gr.Markdown("*Please login first to use this feature*")
            
            with gr.Row():
                with gr.Column():
                    audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record Your Voice")
                    image_input = gr.Image(type="filepath", label="Upload Medical Image")
                    process_btn = gr.Button("Analyze", variant="primary", size="lg")
                
                with gr.Column():
                    speech_output = gr.Textbox(label="Speech to Text", lines=3)
                    doctor_output = gr.Textbox(label="Doctor's Response", lines=5)
                    audio_output = gr.Audio(label="Doctor's Voice Response")
    
    # Event handlers
    login_btn.click(
        fn=login,
        inputs=[login_username, login_password],
        outputs=[login_status, logout_btn]
    )
    
    logout_btn.click(
        fn=logout,
        inputs=[],
        outputs=[logout_btn, login_username, login_password, login_status, tabs]
    )
    
    register_btn.click(
        fn=register,
        inputs=[reg_username, reg_password],
        outputs=[register_status]
    )
    
    process_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[speech_output, doctor_output, audio_output]
    )

if __name__ == "__main__":
    print("Starting Gradio app...")
    app.launch(debug=True)