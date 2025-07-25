from fastapi import APIRouter
import os
import base64
from groq import Groq

router = APIRouter()

#Step1: Setup GROQ API key
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

#Step2: Convert image to required format

@router.get("/encode_image")
def encode_image(image_path):   
    image_file=open(image_path, "rb")
    encoded = base64.b64encode(image_file.read()).decode('utf-8')
    return {"encoded_image": encoded}

#Step3: Setup Multimodal LLM 

query="Is there something wrong with my face?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"
#model="llama-3.2-90b-vision-preview" #Deprecated

@router.get("/analyze_image_with_query")
def analyze_image_with_query(query, model, encoded_image):
    client=Groq()  
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )
    return {"response": chat_completion.choices[0].message.content}