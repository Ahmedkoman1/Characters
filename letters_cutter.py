import json

# قائمة الحروف المستهدفة
TARGET_LETTERS = set(['a', 'e', 'l', 'm', 'o', 'u'])


def extract_target_letters_from_text(text: str, targets: set = TARGET_LETTERS,
                                     save_path: str = "phonemes.json") -> list:
    """
    تستقبل نص، وتستخرج منه الأحرف المستهدفة، وتحفظها في ملف JSON.

    Args:
        text (str): النص الذي سيتم استخراج الحروف منه.
        targets (set): مجموعة الحروف المستهدفة (افتراضيًا TARGET_LETTERS).
        save_path (str): مسار حفظ ملف JSON الناتج.

    Returns:
        list: قائمة الحروف المستخرجة.
    """
    if not text.strip():
        raise ValueError("❌ النص المدخل فارغ.")

    # استخراج الأحرف المستهدفة فقط
    phonemes = [ch.lower() for ch in text if ch.lower() in targets]

    # حفظ النتيجة في ملف JSON
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(phonemes, f, ensure_ascii=False, indent=2)

    print(f"✅ تم استخراج {len(phonemes)} حرف وحفظها في {save_path}")
    return phonemes
