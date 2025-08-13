import requests
from infer_rvc_python import BaseLoader

# ضع هنا رابط ngrok الذي يعطيك كولاب
COLAB_TTS_URL = "https://a64ed00b7857.ngrok-free.app/tts"

def get_audio_from_colab(text, output_path="robotic.wav"):
    r = requests.post(COLAB_TTS_URL, json={"text": text})
    if r.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(r.content)
        print(f"✅ تم استلام الصوت من كولاب وحفظه في {output_path}")
    else:
        raise Exception(f"❌ خطأ {r.status_code}: {r.text}")

def convert_with_rvc(input_path, model_path, index_path, tag="donald-trump"):
    converter = BaseLoader(only_cpu=False)
    converter.apply_conf(
        tag=tag,
        file_model=model_path,
        pitch_algo="rmvpe",
        pitch_lvl=0,
        file_index=index_path,
        index_influence=0.75,
        respiration_median_filtering=3,
        envelope_ratio=0.25,
        consonant_breath_protection=0.33
    )
    results = converter(audio_files=input_path, overwrite=True, parallel_workers=1)
    print(f"✅ تم تحويل الصوت وحفظه في {results[0]}")
    converter.unload_models()
    return results[0]

if __name__ == "__main__":
    with open("documentary_intro.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("❌ لا يوجد نص في 'documentary_intro.txt'")
    else:
        robotic_wav = "robotic.wav"
        model_path = r"C:\Users\TOSHIBA\PycharmProjects\Amk\Donald-Trump_e135_s6480.pth"
        index_path = r"C:\Users\TOSHIBA\PycharmProjects\Amk\added_IVF1408_Flat_nprobe_1_Donald-Trump_v2.index"

        # ✅ إرسال النص إلى كولاب واستقبال الصوت
        get_audio_from_colab(text, robotic_wav)

        # 🔹 تشغيل RVC
        final_audio = convert_with_rvc(robotic_wav, model_path, index_path, tag="donald-trump")
