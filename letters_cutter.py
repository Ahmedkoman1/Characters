import json

# حدد الأحرف / الفونيمات التي تريد تتبعها
# هذه قائمة مثال للأحرف التي لديك
target_letters = set(['a', 'e', 'l', 'm', 'o', 'u'])

def extract_target_letters(text, targets):
    # نص صغير للأحرف المختارة فقط
    filtered = [ch.lower() for ch in text if ch.lower() in targets]
    return filtered

def main():
    # قراءة النص النهائي من ChatGPT
    with open("documentary_intro.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # استخراج الأحرف المطلوبة
    phonemes = extract_target_letters(text, target_letters)

    # حفظ الأحرف في ملف JSON
    with open("phonemes.json", "w", encoding="utf-8") as f:
        json.dump(phonemes, f, ensure_ascii=False, indent=2)

    print(f"تم استخراج {len(phonemes)} حرف وحفظها في phonemes.json")

if __name__ == "__main__":
    main()
