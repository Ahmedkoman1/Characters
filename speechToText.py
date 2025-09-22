import shutil
import tempfile
import requests
import os

# رابط Colab (تأكد إنه شغال ومحدث دائماً)
API_URL = "https://fa143f28c4e7.ngrok-free.app/transcribe"

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
            try:
                response = requests.post(API_URL, files=files, timeout=30)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"[❌] فشل الاتصال بـ Colab API: {e}")
                return ""

        print("Response status code:", response.status_code)
        print("Response headers:", response.headers)
        print("Response text:", response.text)

        try:
            data = response.json()
            text = data.get("text", "")
        except Exception:
            print("⚠️ الرد من Colab ليس JSON صالح.")
            text = ""

        if text:
            print(f"[📝] تم استلام النص من Colab: {text}")
        else:
            print("⚠️ لم يتم استخراج أي نص من الرد.")

        return text

    finally:
        # حذف الملف المؤقت
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
