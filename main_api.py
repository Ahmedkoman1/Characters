from fastapi import FastAPI, File, UploadFile
import os
import tempfile
from speechToText import speech_to_text
from chatgpt import generate_trump_response
from letters_cutter import extract_target_letters_from_text
from tts_rvc import get_audio_from_colab, convert_with_rvc
import platform

app = FastAPI()

def play_audio(file_path):
    print(f"\n🔊 تشغيل الصوت: {file_path}")
    system = platform.system()

    if system == "Windows":
        os.system(f'start "" "{file_path}"')
    elif system == "Darwin":  # macOS
        os.system(f"afplay \"{file_path}\"")
    elif system == "Linux":
        os.system(f"aplay \"{file_path}\"")
    else:
        print("❌ لا يمكن تشغيل الصوت على هذا النظام تلقائيًا.")

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

        # 4️⃣ استخراج الحروف
        letters = extract_target_letters_from_text(trump_text)

        # 5️⃣ تحويل النص لصوت روبوتي
        robotic_wav = "robotic.wav"
        get_audio_from_colab(trump_text, robotic_wav)

        # 6️⃣ تحويل الصوت لصوت ترامب
        final_audio = convert_with_rvc(
            robotic_wav,
            r"C:\Users\TOSHIBA\PycharmProjects\Amk\Donald-Trump_e135_s6480.pth",
            r"C:\Users\TOSHIBA\PycharmProjects\Amk\added_IVF1408_Flat_nprobe_1_Donald-Trump_v2.index",
            tag="donald-trump"
        )

        # 7️⃣ تشغيل الصوت النهائي
        play_audio(final_audio)

        return {
            "original_text": text,
            "trump_text": trump_text,
            "letters": letters,
            "final_audio_path": final_audio
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
