from deep_translator import GoogleTranslator

def translate_text(text, source_lang='auto', target_lang='vi'):
    """
    Hàm dịch văn bản từ ngôn ngữ bất kỳ (hoặc tự động phát hiện) sang Tiếng Việt.
    """
    try:
        if not text.strip():
            return ""
            
        # Khởi tạo bộ dịch sang tiếng Việt ('vi')
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        return f"[Lỗi dịch: {str(e)}]"