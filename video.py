# Cập nhật cú pháp import mới nhất của MoviePy (Bỏ .editor)
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
import os

def merge_audio_to_video(video_path, output_path, log_callback):
    """
    Hàm lấy các file audio lẻ trong thư mục temp, 
    lập lịch chèn đè lên video gốc theo đúng dòng thời gian.
    """
    try:
        if not os.path.exists(video_path):
            log_callback("❌ Lỗi: Không tìm thấy file video gốc để lồng tiếng!")
            return False
            
        log_callback("🎬 AI bắt đầu quá trình lồng tiếng và render video...")
        
        # Tải video gốc
        video_clip = VideoFileClip(video_path)
        
        # Tìm tất cả file audio trong thư mục temp
        audio_files = sorted([f for f in os.listdir("temp") if f.startswith("audio_") and f.endswith(".mp3")],
                             key=lambda x: int(x.split("_")[1].split(".")[0]))
                             
        if not audio_files:
            log_callback("❌ Lỗi: Không tìm thấy các file âm thanh tạm thời trong thư mục temp!")
            return False
            
        clips_audio = []
        current_time = 0.0
        
        for file in audio_files:
            audio_f_path = os.path.join("temp", file)
            audio_clip = AudioFileClip(audio_f_path)
            
            # Đặt mốc thời gian bắt đầu nói cho đoạn audio này
            audio_clip = audio_clip.with_start(current_time) # MoviePy mới dùng with_start thay cho set_start
            clips_audio.append(audio_clip)
            
            # Câu tiếp theo sẽ nói ngay sau khi câu trước kết thúc (hoặc tăng tịnh tiến)
            current_time += audio_clip.duration + 0.5 
            
        # Trộn đống audio AI vào làm một luồng âm thanh tổng hợp
        final_audio = CompositeAudioClip(clips_audio)
        
        # Gắn luồng âm thanh mới này vào video gốc
        final_video = video_clip.with_audio(final_audio) # MoviePy mới dùng with_audio thay cho set_audio
        
        # Đảm bảo thư mục output tồn tại
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Tiến hành xuất bản (Render) Video
        log_callback("⏳ Đang xuất video (Render) thành phẩm. Vui lòng đợi...")
        final_video.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac"
        )
        
        # Đóng giải phóng bộ nhớ
        video_clip.close()
        final_video.close()
        
        log_callback(f"🎉 THÀNH CÔNG! Video lồng tiếng đã lưu tại: {output_path}")
        return True
        
    except Exception as e:
        log_callback(f"❌ Lỗi hệ thống khi lồng tiếng: {str(e)}")
        return False