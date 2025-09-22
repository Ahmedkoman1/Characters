from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from speechToText import speech_to_text
from chatgpt import generate_trump_response

from tts_rvc import get_audio_from_colab, convert_with_rvc

app = FastAPI()

# ✅ تفعيل CORS للسماح للفرونت بالوصول للملفات
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # أو ضع دومين الفرونت فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ مسار مطلق لمجلد الإخراج
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_audios")
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/process_audio/")
async def process_audio(file: UploadFile = File(...)):
    # 1️⃣ حفظ الملف مؤقتاً
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    try:
        # 2️⃣ تحويل الصوت إلى نص
        text = speech_to_text(temp_path)

        # 3️⃣ توليد رد ترامب
        trump_text = generate_trump_response(text)


        # 5️⃣ تحويل النص لصوت روبوتي
        robotic_wav = os.path.join(OUTPUT_DIR, "robotic.wav")
        get_audio_from_colab(trump_text, robotic_wav)

        # 6️⃣ تحويل الصوت لصوت ترامب
        final_audio = os.path.join(OUTPUT_DIR, "trump_voice.wav")
        convert_with_rvc(
            robotic_wav,
            r"C:\Users\TOSHIBA\PycharmProjects\Amk1\models_rvc\Donald-Trump\Donald-Trump_e135_s6480.pth",
            r"C:\Users\TOSHIBA\PycharmProjects\Amk1\models_rvc\Donald-Trump\added_IVF1408_Flat_nprobe_1_Donald-Trump_v2.index",
            tag="donald-trump",
            output_path=final_audio
        )

        # 7️⃣ رابط مباشر للصوت
        audio_filename = os.path.basename(final_audio)
        audio_url = f"http://127.0.0.1:8000/audio/{audio_filename}"

        return {
            "original_text": text,
            "trump_text": trump_text,
            "audio_url": audio_url
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# ✅ خدمة الملفات الناتجة مباشرة
app.mount("/audio", StaticFiles(directory=OUTPUT_DIR), name="audio")

# ✅ تأكيد التشغيل برابط مباشر للملف
@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav")
    return {"error": "File not found"}