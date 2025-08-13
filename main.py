import platform
import os
import simpleaudio as sa



def run_script(script_name):
    print(f"\n🚀 تشغيل: {script_name}")
    exit_code = os.system(f"python {script_name}")
    if exit_code != 0:
        print(f"❌ حدث خطأ أثناء تشغيل {script_name}")
        exit(1)

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

def wait_for_user():
    input("🟢 اضغط Enter لبدء التسجيل... (أو Ctrl+C للخروج)")

def main():
    print("🎬 أهلاً بك في مشروع تحويل الصوت إلى فيديو بصوت دونالد ترامب")

    try:
        while True:
            wait_for_user()

            # 1. تسجيل وتحويل الصوت إلى نص
            run_script("speechToText.py")

            # 2. تمرير النص إلى GPT (النص يحفظ في documentary_intro.txt)
            run_script("chatgpt.py")
            run_script("letters_cutter.py")

            # 3. تحويل النص إلى صوت دونالد ترامب باستخدام RVC
            run_script("tts_rvc.py")

            # 4. إعداد المسارات النهائية
            final_audio_path = r"C:\Users\TOSHIBA\PycharmProjects\Amk\robotic.wav"
            source_image = r"C:\Users\TOSHIBA\PycharmProjects\Amk\trump.jpg"
            output_dir = "results"

            if os.path.exists(final_audio_path):
                # تشغيل الصوت
                play_audio(final_audio_path)

                # توليد الفيديو
            else:
                print("❌ لم يتم العثور على ملف الصوت النهائي!")

            print("\n=======================================\n")

    except KeyboardInterrupt:
        print("\n❗ تم إيقاف البرنامج بواسطة المستخدم. إلى اللقاء!")

if __name__ == "__main__":
    main()