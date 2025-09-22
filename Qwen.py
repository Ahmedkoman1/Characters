import time
from langdetect import detect
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ================================
# مسار النموذج المحلي
MODEL_PATH = Path(r"/path/to/Qwen2.5-7B-Instruct")  # عدّل المسار حسب مكان النموذج على السيرفر

# ================================
# تحميل التوكنيزر والموديل
tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH), local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True,
    device_map="auto",
    torch_dtype=torch.float16
)

# ================================
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
}

# ================================
def generate_trump_response_local(user_text: str, save_path: str = "documentary_intro.txt", max_tokens: int = 500) -> str:
    """
    توليد نص بأسلوب ترامب باستخدام Qwen2.5-7B-Instruct محليًا.
    نفس خصائص الفانكشن الأصلية: كشف اللغة، حفظ الناتج، استخدام برومبت محدد.
    """
    if not user_text.strip():
        raise ValueError("❌ النص المدخل فارغ.")

    # 1️⃣ كشف اللغة
    language = detect(user_text)
    print(f"📌 اللغة المتوقعة تلقائيًا: {language} ✅ متابعة تلقائية.")
    language_name = language_map.get(language, "English")

    # 2️⃣ حفظ اللغة في ملف
    with open("detected_lang.txt", "w", encoding="utf-8") as f:
        f.write(language)

    # 3️⃣ إنشاء البرومبت بأسلوب ترامب
    prompt = f"""
    You are now speaking as Donald J. Trump. Respond in his distinctive speaking style: confident, bold, sometimes repetitive, rich in catchphrases — but also appropriate to the context.

    ⛔ Do not go off-topic. Do not introduce yourself unless specifically asked.

    ✅ If the user greets you (e.g., "hello", "how are you"), reply naturally and briefly as Trump would in real life — warm, short, and direct.

    ✅ If the user asks a question, answer it directly with Trump's tone, but adjust the length based on the complexity of the input:
    - For simple questions, respond briefly.
    - For deeper or complex prompts, expand as needed using Trump's characteristic way of speaking.

    Respond only to the following input as Trump:

    {user_text}

    Always respond in this language: {language_name}.
    """

    # 4️⃣ توليد النص محليًا مع إعادة المحاولة إذا حصل خطأ
    retries = 3
    delay = 5
    final_response = None

    for attempt in range(retries):
        try:
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=0.7
            )
            final_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            break
        except Exception as e:
            print(f"⚠️ خطأ في توليد النص: {e}")
            if attempt < retries - 1:
                print(f"⏳ إعادة المحاولة بعد {delay} ثانية...")
                time.sleep(delay)

    if not final_response:
        raise Exception("❌ فشل في توليد النص بعد عدة محاولات.")

    # 5️⃣ حفظ النص في ملف
    with open(save_path, "w", encoding="utf-8") as file:
        file.write(final_response)

    print(f"🎉 تم إنشاء النص وحفظه في {save_path}")
    return final_response

# ================================
# مثال استخدام
if __name__ == "__main__":
    prompt = "Hello, who are you?"
    response = generate_trump_response_local(prompt)
    print("Prompt:", prompt)
    print("Response:", response)
