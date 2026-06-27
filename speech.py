from faster_whisper import WhisperModel
import os
from translator import translate_text
# Nhập hàm tạo giọng nói gTTS từ file tts.py
from tts import text_to_speech_async

def transcribe_video(video_path, log_callback):
    if not video_path or not os.path.exists(video_path):
        log_callback("Lỗi: Không tìm thấy file video để xử lý!")
        return

    log_callback("🤖 AI đang khởi tạo mô hình Faster-Whisper...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    
    log_callback("⏳ AI đang bóc băng, dịch thuật và tạo giọng nói v0.5...")
    segments, info = model.transcribe(video_path, beam_size=5)
    
    log_callback(f"🌍 Phát hiện ngôn ngữ gốc: {info.language}")
    log_callback("--- TIẾN TRÌNH XỬ LÝ AI (v0.5) ---")
    
    # Tạo thư mục temp chứa file mp3
    os.makedirs("temp", exist_ok=True)
    
    count = 0
    full_translated_text = ""
    for segment in segments:
        count += 1
        start_min = int(segment.start // 60)
        start_sec = int(segment.start % 60)
        end_min = int(segment.end // 60)
        end_sec = int(segment.end % 60)
        time_stamp = f"[{start_min:02d}:{start_sec:02d} -> {end_min:02d}:{end_sec:02d}]"
        
        original_text = segment.text
        vietnamese_text = translate_text(original_text, source_lang='auto', target_lang='vi')
        
        mp3_filename = f"temp/audio_{count}.mp3"
        
        # Gọi trực tiếp hàm gTTS chạy đồng bộ, không cần qua vòng lặp loop.run_until_complete phức tạp nữa
        tts_success = text_to_speech_async(vietnamese_text, mp3_filename)
        
        status_tts = "🔊 Đã tạo giọng nói" if tts_success else "❌ Lỗi tạo giọng"
        line = f"{time_stamp} ({status_tts})\n   Gốc: {original_text}\n   Dịch: {vietnamese_text}"
        log_callback(line)
        
        full_translated_text += vietnamese_text + " "
        
    log_callback("--- HOÀN THÀNH TẠO GIỌNG NÓI v0.5 ---")
    return full_translated_text