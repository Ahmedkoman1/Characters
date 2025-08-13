import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import requests
import os

# إعدادات التسجيل
SAMPLE_RATE = 16000
CHANNELS = 1

# رابط API الخاص بـ Colab
API_URL = "https://3d69498ffd2b.ngrok-free.app/transcribe"  # غيّره إذا كان Colab على رابط آخر

def record_audio():
    print("🎤 الاستماع جارٍ... الرجاء التحدث")
    recording = []
    silence_threshold = 0.01
    silence_duration = 1.0  # ثانية من الصمت لإنهاء التسجيل
    silent_chunks = 0
    chunk_size = int(0.5 * SAMPLE_RATE)

    speaking_started = False  # لبدء التسجيل فقط بعد اكتشاف صوت

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="float32") as stream:
        while True:
            chunk, _ = stream.read(chunk_size)
            volume = np.abs(chunk).mean()

            if volume > silence_threshold:
                speaking_started = True
                recording.append(chunk)
                silent_chunks = 0
            else:
                if speaking_started:
                    silent_chunks += 1
                    recording.append(chunk)
                    if silent_chunks * (chunk_size / SAMPLE_RATE) > silence_duration:
                        break

    if not speaking_started:
        print("لم يتم اكتشاف كلام، يرجى المحاولة مجددًا.")
        return None

    audio_data = np.concatenate(recording, axis=0)
    return audio_data

def save_temp_wav(audio_data):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, SAMPLE_RATE, (audio_data * 32767).astype(np.int16))
    return temp_file.name

def send_to_colab(file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(API_URL, files=files)
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        return f"[خطأ] {response.status_code}: {response.text}"

if __name__ == "__main__":
    try:
        audio_data = record_audio()
        if audio_data is not None:
            wav_path = save_temp_wav(audio_data)
            print("⏳ جاري الإرسال إلى Colab...")
            text = send_to_colab(wav_path)
            print(f"[📝] {text}")

            # حفظ النص في ملف ثابت باسم transcribed_text.txt
            with open("transcribed_text.txt", "w", encoding="utf-8") as txt_file:
                txt_file.write(text)
            print("✅ تم حفظ النص في الملف: transcribed_text.txt")

            os.remove(wav_path)
        else:
            print("🚫 لم يتم تسجيل أي صوت.")
    except KeyboardInterrupt:
        print("\n🚪 تم الإنهاء.")
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")
