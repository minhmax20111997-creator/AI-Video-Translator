from faster_whisper import WhisperModel
import os
# Nhập hàm dịch từ file translator.py vào đây
from translator import translate_text

def transcribe_video(video_path, log_callback):
    if not video_path or not os.path.exists(video_path):
        log_callback("Lỗi: Không tìm thấy file video để xử lý!")
        return

    log_callback("🤖 AI đang khởi tạo mô hình Faster-Whisper...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    
    log_callback("⏳ AI đang lắng nghe và tiến hành dịch thuật v0.4...")
    segments, info = model.transcribe(video_path, beam_size=5)
    
    log_callback(f"🌍 Phát hiện ngôn ngữ gốc: {info.language}")
    log_callback("--- NỘI DUNG AI DỊCH ĐƯỢC (v0.4) ---")
    
    full_translated_text = ""
    for segment in segments:
        start_min = int(segment.start // 60)
        start_sec = int(segment.start % 60)
        end_min = int(segment.end // 60)
        end_sec = int(segment.end % 60)
        time_stamp = f"[{start_min:02d}:{start_sec:02d} -> {end_min:02d}:{end_sec:02d}]"
        
        # Câu gốc AI nghe được (Ví dụ: Tiếng Trung)
        original_text = segment.text
        
        # Tiến hành dịch sang Tiếng Việt bằng hàm của translator.py
        vietnamese_text = translate_text(original_text, source_lang='auto', target_lang='vi')
        
        # Hiển thị cả câu gốc và câu dịch lên màn hình Nhật ký hoạt động
        line = f"{time_stamp}\n   Gốc: {original_text}\n   Dịch: {vietnamese_text}"
        log_callback(line)
        
        full_translated_text += vietnamese_text + " "
        
    log_callback("--- HOÀN THÀNH DỊCH THUẬT v0.4 ---")
    return full_translated_text