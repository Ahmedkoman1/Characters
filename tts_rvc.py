import requests
from infer_rvc_python import BaseLoader

# رابط ngrok الخاص بكولاب TTS
COLAB_TTS_URL = "https://fc78dca20999.ngrok-free.app/tts"


def get_audio_from_colab(text: str, output_path: str = "robotic.wav") -> str:
    """
    يرسل النص إلى كولاب TTS ويستقبل ملف الصوت الناتج.

    Args:
        text (str): النص الذي سيتم تحويله لصوت.
        output_path (str): مسار حفظ ملف الصوت الناتج.

    Returns:
        str: مسار ملف الصوت الناتج.
    """
    if not text.strip():
        raise ValueError("❌ النص المدخل فارغ، لا يمكن توليد الصوت.")

    r = requests.post(COLAB_TTS_URL, json={"text": text})
    if r.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(r.content)
        print(f"✅ تم استلام الصوت من كولاب وحفظه في {output_path}")
        return output_path
    else:
        raise Exception(f"❌ خطأ {r.status_code}: {r.text}")


def convert_with_rvc(input_path: str, model_path: str, index_path: str, tag: str = "donald-trump") -> str:
    """
    يحول ملف الصوت باستخدام RVC Model.

    Args:
        input_path (str): مسار ملف الصوت المدخل.
        model_path (str): مسار ملف نموذج RVC.
        index_path (str): مسار ملف الفهرس للنموذج.
        tag (str): الوسم أو اسم الشخصية المستهدفة.

    Returns:
        str: مسار ملف الصوت النهائي بعد التحويل.
    """
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
