from fastapi import FastAPI, File, UploadFile
import shutil
import tempfile
import requests
import os

app = FastAPI()

API_URL = "https://86421fa4dfea.ngrok-free.app/transcribe"  # رابط Colab

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

    with open(temp_file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(API_URL, files=files)

    os.remove(temp_file_path)

    print("Response status code:", response.status_code)
    print("Response headers:", response.headers)
    print("Response text:", response.text)

    if response.status_code == 200:
        text = response.json().get("text", "")
        print(f"[📝] تم استلام النص من Colab: {text}")
        return {"text": text}
    else:
        return {"error": f"خطأ {response.status_code}: {response.text}"}
