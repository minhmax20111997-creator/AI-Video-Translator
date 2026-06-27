from faster_whisper import WhisperModel
import os

def transcribe_video(video_path, log_callback):
    """
    Hàm sử dụng Faster-Whisper để bóc băng giọng nói từ video thành văn bản.
    """
    if not video_path or not os.path.exists(video_path):
        log_callback("Lỗi: Không tìm thấy file video để xử lý!")
        return

    log_callback("🤖 AI đang khởi tạo mô hình Faster-Whisper (bản nhỏ)...")
    
    # Khởi tạo model Whisper chạy trên CPU
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    
    log_callback("⏳ AI đang lắng nghe và bóc băng video...")
    
    # Tiến hành dịch giọng nói thành chữ
    segments, info = model.transcribe(video_path, beam_size=5)
    
    log_callback(f"🌍 Phát hiện ngôn ngữ gốc: {info.language}")
    log_callback("--- NỘI DUNG AI NGHE ĐƯỢC ---")
    
    full_text = ""
    for segment in segments:
        start_min = int(segment.start // 60)
        start_sec = int(segment.start % 60)
        end_min = int(segment.end // 60)
        end_sec = int(segment.end % 60)
        
        time_stamp = f"[{start_min:02d}:{start_sec:02d} -> {end_min:02d}:{end_sec:02d}]"
        line = f"{time_stamp} {segment.text}"
        
        log_callback(line)
        full_text += segment.text + " "
        
    log_callback("--- HOÀN THÀNH BÓC BĂNG v0.3 ---")
    return full_text