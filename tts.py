from gtts import gTTS
import os

def text_to_speech_async(text, output_mp3_path):
    """
    Hàm chuyển đổi văn bản Tiếng Việt thành file âm thanh sử dụng Google TTS.
    Giữ nguyên tên hàm là 'text_to_speech_async' để không phải sửa file speech.py.
    """
    try:
        if not text.strip():
            return False
            
        # Đảm bảo thư mục temp tồn tại
        os.makedirs(os.path.dirname(output_mp3_path), exist_ok=True)
        
        # Gọi thư viện Google dịch chữ thành giọng nói (ngôn ngữ Tiếng Việt 'vi')
        tts = gTTS(text=text, lang='vi', slow=False)
        
        # Lưu trực tiếp thành file mp3
        tts.save(output_mp3_path)
        return True
    except Exception as e:
        print(f"[Lỗi hệ thống Google TTS]: {str(e)}")
        return False