import requests
from infer_rvc_python import BaseLoader
import torch
from fairseq.data.dictionary import Dictionary



torch.serialization.add_safe_globals([Dictionary])

COLAB_TTS_URL = "https://4999b15449d9.ngrok-free.app/tts"


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


import shutil

def convert_with_rvc(
    input_path: str,
    model_path: str,
    index_path: str,
    tag: str = "donald-trump",
    output_path: str = None
) -> str:
    """
    يحول ملف الصوت باستخدام RVC Model.

    Args:
        input_path (str): مسار ملف الصوت المدخل.
        model_path (str): مسار ملف نموذج RVC.
        index_path (str): مسار ملف الفهرس للنموذج.
        tag (str): الوسم أو اسم الشخصية المستهدفة.
        output_path (str): مسار حفظ الملف الناتج (اختياري).

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
    converter.unload_models()

    final_path = results[0]

    # إذا تم تحديد مسار مخصص للحفظ، انسخ الملف له
    if output_path:
        shutil.copy(final_path, output_path)
        final_path = output_path

    print(f"✅ تم تحويل الصوت وحفظه في {final_path}")
    return final_path
