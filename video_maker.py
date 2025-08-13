import subprocess
import sys
import os

def generate_video_with_sadtalker(audio_path, image_path, output_dir, working_dir):
    print(f"\n🎥 بدء توليد الفيديو باستخدام SadTalker...")

    command = [
        sys.executable, "inference.py",
        "--driven_audio", audio_path,
        "--source_image", image_path,
        "--enhancer", "gfpgan",
        "--result_dir", output_dir,
        "--preprocess", "extfull"
    ]

    try:
        subprocess.run(command, cwd=working_dir, check=True)
        print(f"✅ تم إنشاء الفيديو في المجلد: {output_dir}")
    except subprocess.CalledProcessError:
        print("❌ حدث خطأ أثناء توليد الفيديو من SadTalker.")

# تشغيل مباشر إذا تم تنفيذ الملف لوحده (اختياري)
if __name__ == "__main__":
    audio_path = r"C:\Users\TOSHIBA\PycharmProjects\Amk\robotic.wav"
    image_path = r"C:\Users\TOSHIBA\PycharmProjects\Amk\trump.jpg"
    output_dir = "results"
    working_dir = r"C:\Users\TOSHIBA\PycharmProjects\Amk\SadTalker"

    if os.path.exists(audio_path) and os.path.exists(image_path):
        generate_video_with_sadtalker(audio_path, image_path, output_dir, working_dir)
    else:
        print("❌ تأكد من وجود ملفات الصوت والصورة.")
