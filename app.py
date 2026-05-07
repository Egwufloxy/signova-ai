from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
import shutil
import os

app = FastAPI()

# ✅ Enable CORS (so frontend can connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# SIGN MAPPING (MVP LOGIC)
# -----------------------------
sign_dictionary = {
    "hello": "hello.mp4",
    "help": "help.mp4",
    "pain": "pain.mp4",
    "wait": "wait.mp4",
    "thank": "thank_you.mp4",
    "emergency": "emergency.mp4"
}

# -----------------------------
# HEALTH CHECK ROUTE
# -----------------------------
@app.get("/")
def home():
    return {"message": "Signova AI is running"}

# -----------------------------
# SPEECH → SIGN ENDPOINT
# -----------------------------
@app.post("/speech-to-sign")
async def speech_to_sign(audio: UploadFile = File(...)):

    # Save uploaded audio temporarily
    file_path = "temp.wav"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data).lower()

    except Exception as e:
        os.remove(file_path)
        return {"error": str(e)}

    # Match text to sign video
    matched_sign = None

    for key in sign_dictionary:
        if key in text:
            matched_sign = sign_dictionary[key]
            break

    # cleanup
    os.remove(file_path)

    return {
        "recognized_text": text,
        "sign_video": matched_sign
    }