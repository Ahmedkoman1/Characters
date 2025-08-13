from openai import OpenAI
from langdetect import detect
import time

# إعداد عميل OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# خريطة تحويل كود اللغة إلى اسم لغة
language_map = {
    "ar": "Arabic",
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "tr": "Turkish",
    "pt": "Portuguese",
    "ru": "Russian"
    # أضف لغات أخرى إذا لزم الأمر
}

def generate_trump_response(user_text: str, save_path: str = "documentary_intro.txt") -> str:
    """
    يأخذ النص المستخرج من الصوت، يكتشف اللغة،
    يرسل النص إلى ChatGPT بصوت ترامب، ويحفظ الناتج في ملف.
    """
    if not user_text.strip():
        raise ValueError("❌ النص المدخل فارغ.")

    # 1. تحديد اللغة
    language = detect(user_text)
    print(f"📌 اللغة المتوقعة تلقائيًا: {language} ✅ متابعة تلقائية.")

    language_name = language_map.get(language, "English")

    # 2. حفظ اللغة في ملف
    with open("detected_lang.txt", "w", encoding="utf-8") as f:
        f.write(language)

    # 3. إنشاء البرومبت
    prompt = f"""
    You are now speaking as Donald J. Trump. Respond in his distinctive speaking style: confident, bold, sometimes repetitive, rich in catchphrases — but also appropriate to the context.

    ⛔ Do not go off-topic. Do not introduce yourself unless specifically asked.

    ✅ If the user greets you (e.g., "hello", "how are you"), reply naturally and briefly as Trump would in real life — warm, short, and direct.

    ✅ If the user asks a question, answer it directly with Trump's tone, but adjust the length based on the complexity of the input:
    - For simple questions, respond briefly.
    - For deeper or complex prompts, expand as needed using Trump's characteristic way of speaking.

    🚫 Never say things like: "Here's your answer", "I will now write", "Let me tell you", unless it's part of the answer itself.

    Respond only to the following input as Trump:

    {user_text}

    Always respond in this language: {language_name}.
    """

    # 4. إرسال الطلب مع إعادة المحاولة
    retries = 3
    delay = 5
    final_response = None

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                extra_headers={
                    "HTTP-Referer": "https://yourwebsite.com",
                    "X-Title": "AhmedDocumentaries"
                }
            )

            if response.choices and response.choices[0].message.content:
                final_response = response.choices[0].message.content
                break
            else:
                print("❌ فشل توليد النص، لا يوجد محتوى.")
        except Exception as e:
            print(f"⚠️ خطأ في الاتصال: {e}")
            if attempt < retries - 1:
                print(f"⏳ سيتم إعادة المحاولة بعد {delay} ثانية...")
                time.sleep(delay)

    if not final_response:
        raise Exception("❌ فشل في توليد النص بعد عدة محاولات.")

    # 5. حفظ النص
    with open(save_path, "w", encoding="utf-8") as file:
        file.write(final_response)

    print(f"🎉 تم إنشاء النص وحفظه في {save_path}")
    return final_response
