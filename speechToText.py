import shutil
import tempfile
import requests
import os

# رابط Colab
API_URL = "https://bd1926ea16ea.ngrok-free.app/transcribe"

def speech_to_text(file_path: str) -> str:
    """
    يأخذ مسار ملف صوتي، يرسله إلى Colab، ويعيد النص الناتج.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ لم يتم العثور على الملف: {file_path}")

    # إنشاء ملف مؤقت بنفس الامتداد
    suffix = os.path.splitext(file_path)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        with open(file_path, "rb") as src:
            shutil.copyfileobj(src, temp_file)
        temp_file_path = temp_file.name

    try:
        # إرسال الملف إلى Colab
        with open(temp_file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(API_URL, files=files)

        print("Response status code:", response.status_code)
        print("Response headers:", response.headers)
        print("Response text:", response.text)

        if response.status_code == 200:
            text = response.json().get("text", "")
            print(f"[📝] تم استلام النص من Colab: {text}")
            return text
        else:
            raise Exception(f"خطأ {response.status_code}: {response.text}")

    finally:
        # حذف الملف المؤقت
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
