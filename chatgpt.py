from openai import OpenAI
from langdetect import detect
import time

# 🔹 إعداد عميل OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# 🔹 1. أخذ فكرة الفيديو من ملف whisper
with open("transcribed_text.txt", "r", encoding="utf-8") as f:
    topic = f.read().strip()

# 🔹 2. تحديد اللغة
language = detect(topic)
print(f"📌 اللغة المتوقعة تلقائيًا: {language} ✅ متابعة تلقائية.")

# 🔹 3. تحويل كود اللغة إلى اسم لغة
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
    # أضف لغات أخرى عند الحاجة
}

language_name = language_map.get(language, "English")  # الافتراضي إنجليزي

# 🔹 حفظ اللغة في ملف للمراحل التالية
with open("detected_lang.txt", "w", encoding="utf-8") as f:
    f.write(language)

# 🔹 4. إعداد البرومبت باستخدام لغة المستخدم
initial_prompt = f"""
You are now speaking as Donald J. Trump. Respond in his distinctive speaking style: confident, bold, sometimes repetitive, rich in catchphrases — but also appropriate to the context.

⛔ Do not go off-topic. Do not introduce yourself unless specifically asked.

✅ If the user greets you (e.g., "hello", "how are you"), reply naturally and briefly as Trump would in real life — warm, short, and direct.

✅ If the user asks a question, answer it directly with Trump's tone, but adjust the length based on the complexity of the input:
- For simple questions, respond briefly.
- For deeper or complex prompts, expand as needed using Trump's characteristic way of speaking.

🚫 Never say things like: "Here's your answer", "I will now write", "Let me tell you", unless it's part of the answer itself.

Respond only to the following input as Trump:

{topic}

Always respond in this language: {language_name}.

"""

# 🔹 5. إرسال الطلب مع التحكم في max_tokens
def get_response(prompt):
    retries = 3
    delay = 5

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
                return response.choices[0].message.content
            else:
                print("❌ فشل توليد النص، لا يوجد محتوى.")
                return None

        except Exception as e:
            print(f"⚠️ خطأ في الاتصال: {e}")
            if attempt < retries - 1:
                print(f"⏳ سيتم إعادة المحاولة بعد {delay} ثانية...")
                time.sleep(delay)
            else:
                print("❌ فشل بعد عدة محاولات.")
                return None

# 🔹 6. تنفيذ وإنشاء الملف
initial_text = get_response(initial_prompt)

if initial_text:
    with open("documentary_intro.txt", "w", encoding="utf-8") as file:
        file.write(initial_text)
    print("🎉 تم إنشاء مقدمة السكريبت وحُفظت في documentary_intro.txt")
else:
    print("❌ لم يتم توليد النص.")
