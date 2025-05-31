from fastapi import FastAPI
from backend.routers import brain_of_the_assistant, voice_of_doctor, voice_of_patient

app = FastAPI()

# Include routers
app.include_router(brain_of_the_assistant.router, prefix="/brain_of_the_assistant", tags=["Brain"])
app.include_router(voice_of_doctor.router, prefix="/voice_of_doctor", tags=["Doctor"])
app.include_router(voice_of_patient.router, prefix="/voice_of_patient", tags=["Patients"])