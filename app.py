import whisper
import pyaudio
import wave
import os
import tempfile

model = whisper.load_model("medium")  # يمكنك تغييره لـ 'small' أو 'medium'

# إعدادات التسجيل
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5  # مدة التسجيل

def record_audio(file_path):
    audio = pyaudio.PyAudio()

    print("🎙️ تسجيل جاري... تحدث الآن")

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("✅ تم تسجيل الصوت، جاري التحويل إلى نص...")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def transcribe_audio(path):
    result = model.transcribe(path)
    print("📝 النص المكتشف:")
    print(result["text"])


if __name__ == "__main__":
    input("اضغط Enter لبدء التسجيل وتحويل الصوت إلى نص...")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        audio_path = tmpfile.name

    record_audio(audio_path)
    transcribe_audio(audio_path)

    os.remove(audio_path)
