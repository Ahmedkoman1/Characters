import torch
import whisperx
import json
import os
import subprocess
import re

# -----------------------
# إعداد المسارات والملفات
# -----------------------
AUDIO_PATH = r"C:\Users\TOSHIBA\PycharmProjects\Amk1\generated_audios\trump_voice.wav"
TEXT_FILE = r"C:\Users\TOSHIBA\PycharmProjects\Amk1\documentary_intro.txt"

with open(TEXT_FILE, "r", encoding="utf-8") as f:
    TEXT = f.read().strip()

# -----------------------
# إعداد اللغة والنموذج
# -----------------------
LANG_CODE = "en"      # رمز اللغة للـ WhisperX (مثل: en, ar, fr)
ESPEAK_LANG = "en-us" # رمز اللغة لـ eSpeak-NG (مثل: en-us, fr, ar)
MODEL_SIZE = "small"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# مسار espeak-ng.exe وبياناته
ESPEAK_PATH = r"C:\Program Files\eSpeak_NG\espeak-ng.exe"
ESPEAK_DATA_PATH = r"C:\Program Files\eSpeak_NG\espeak-ng-data"
os.environ["PHONEMIZER_ESPEAK_PATH"] = ESPEAK_PATH
os.environ["ESPEAK_DATA_PATH"] = ESPEAK_DATA_PATH

# -----------------------
# دوال المساعدة
# -----------------------
def whisperx_transcribe_and_align(audio_path, model_size, device, language="en"):
    compute_type = "float16" if device == "cuda" else "float32"
    model = whisperx.load_model(model_size, device, language=language, compute_type=compute_type)
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio)
    model_a, metadata = whisperx.load_align_model(language_code=language, device=device)
    result_aligned = whisperx.align(result["segments"], model_a, metadata, audio, device)
    return result_aligned

def get_word_timestamps_from_whisperx(result):
    words = []
    for seg in result["segments"]:
        for w in seg["words"]:
            words.append({
                "word": w["word"],
                "start": w["start"],
                "end": w["end"]
            })
    return words

def phonemize_word_with_espeak(word, lang=ESPEAK_LANG):
    """
    استخدام eSpeak-NG للحصول على فونيمات كلمة واحدة بلغة محددة.
    """
    try:
        output = subprocess.check_output(
            [ESPEAK_PATH, "-q", "-x", f"-v{lang}", word],
            stderr=subprocess.DEVNULL,
            encoding="utf-8"
        )
        phonemes = output.strip().split()
        return phonemes
    except Exception as e:
        print(f"Error phonemizing {word}: {e}")
        return []

def split_phonemes(phoneme_str):
    """
    تقسيم فونيم مركب إلى فونيمات دقيقة.
    مثال: "h@l'oU" -> ['h', '@', 'l', 'oU']
    """
    phonemes = re.findall(r"[a-zA-Z]+[:@3]*|'[a-zA-Z]+", phoneme_str)
    return phonemes

def phonemize_words(words, espeak_lang=ESPEAK_LANG):
    """
    إنشاء JSON دقيق لكل فونيم فردي مع التوقيت.
    """
    results = []
    vowels = "aeiouAEIOU@3:"

    for w in words:
        phonemes_raw = phonemize_word_with_espeak(w["word"], lang=espeak_lang)
        if not phonemes_raw:
            continue

        # تقسيم كل فونيم مركب إلى فونيمات فردية
        phonemes = []
        for p in phonemes_raw:
            phonemes.extend(split_phonemes(p))

        total_duration = w["end"] - w["start"]
        weights = [1.5 if any(v in p for v in vowels) else 1.0 for p in phonemes]
        weight_sum = sum(weights)

        start_time = w["start"]
        for i, p in enumerate(phonemes):
            dur = total_duration * (weights[i] / weight_sum)
            if dur >= 0.01:
                results.append({
                    "phoneme": p,
                    "word": w["word"],
                    "start": round(start_time, 3),
                    "end": round(start_time + dur, 3)
                })
            start_time += dur
    return results

# -----------------------
# الكود الرئيسي
# -----------------------
def main():
    print("🚀 بدء المعالجة...")
    result = whisperx_transcribe_and_align(AUDIO_PATH, MODEL_SIZE, DEVICE, language=LANG_CODE)
    words = get_word_timestamps_from_whisperx(result)

    # استبدال الكلمات بالنص الأصلي
    manual_words = TEXT.split()
    for i, w in enumerate(words):
        if i < len(manual_words):
            w["word"] = manual_words[i]

    phoneme_timings = phonemize_words(words, espeak_lang=ESPEAK_LANG)

    with open("phoneme_timing.json", "w", encoding="utf-8") as f:
        json.dump(phoneme_timings, f, ensure_ascii=False, indent=2)

    print("✅ تم الحفظ في phoneme_timing.json")

if __name__ == "__main__":
    main()
