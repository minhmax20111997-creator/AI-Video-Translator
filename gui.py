import tkinter as tk
from tkinter import filedialog, ttk
import os
from datetime import datetime
import threading
# Nhập hàm xử lý AI từ file speech.py của bạn
from speech import transcribe_video

class VideoTranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Video Translator v0.3")
        self.root.geometry("600x500")
        self.root.configure(bg="#f8f9fa")
        
        self.video_path = ""
        self.create_widgets()
        self.log_message("Ứng dụng khởi động thành công (v0.3). Sẵn sàng kết nối AI!")

    def create_widgets(self):
        lbl_title = tk.Label(self.root, text="AI VIDEO TRANSLATOR", font=("Arial", 16, "bold"), fg="#1e293b", bg="#f8f9fa")
        lbl_title.pack(pady=15)

        # --- KHUNG QUẢN LÝ FILE ---
        file_frame = tk.LabelFrame(self.root, text=" 📂 Quản lý File ", font=("Arial", 10, "bold"), padx=15, pady=15, bg="#ffffff", fg="#475569")
        file_frame.pack(fill="x", padx=20, pady=5)
        
        self.btn_select = tk.Button(file_frame, text="Chọn Video", command=self.select_video, bg="#2563eb", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5, bd=0, cursor="hand2")
        self.btn_select.pack(side="left", padx=5)
        
        self.lbl_file_name = tk.Label(file_frame, text="Chưa chọn video nào...", fg="#94a3b8", font=("Arial", 10, "italic"), bg="#ffffff")
        self.lbl_file_name.pack(side="left", padx=15)
        
        # --- NÚT BẮT ĐẦU DỊCH (Kích hoạt luồng chạy AI) ---
        self.btn_start = tk.Button(self.root, text="▶ Bắt đầu dịch", command=self.start_translation_thread, state="disabled", bg="#94a3b8", fg="white", font=("Arial", 12, "bold"), pady=8, bd=0)
        self.btn_start.pack(fill="x", padx=20, pady=10)

        # --- THANH TIẾN TRÌNH ---
        progress_frame = tk.Frame(self.root, bg="#f8f9fa")
        progress_frame.pack(fill="x", padx=20, pady=5)
        
        lbl_progress = tk.Label(progress_frame, text="Tiến trình:", font=("Arial", 10), bg="#f8f9fa", fg="#64748b")
        lbl_progress.pack(side="left", padx=5)
        
        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", mode="indeterminate")
        self.progress.pack(side="left", fill="x", expand=True, padx=5)
        
        # --- KHUNG NHẬT KÝ ---
        log_frame = tk.LabelFrame(self.root, text=" 📜 Nhật ký hoạt động ", font=("Arial", 10, "bold"), padx=10, pady=10, bg="#ffffff", fg="#475569")
        log_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.txt_log = tk.Text(log_frame, state="disabled", wrap="word", bg="#f1f5f9", fg="#334155", font=("Consolas", 10), bd=0)
        self.txt_log.pack(fill="both", expand=True)

    def select_video(self):
        file_types = [("Video Files", "*.mp4 *.avi *.mkv"), ("All Files", "*.*")]
        selected_file = filedialog.askopenfilename(title="Chọn video để dịch", filetypes=file_types)
        
        if selected_file:
            self.video_path = selected_file
            file_name = os.path.basename(selected_file)
            self.lbl_file_name.config(text=file_name, fg="#0f172a", font=("Arial", 10, "bold"))
            self.btn_start.config(state="normal", bg="#16a34a", cursor="hand2")
            self.log_message(f"Đã chọn file thành công: {file_name}")
        else:
            self.log_message("Hành động bị hủy: Người dùng không chọn file.")

    def start_translation_thread(self):
        # Chuyển trạng thái nút bấm và chạy thanh tiến trình chạy liên tục
        self.btn_start.config(state="disabled", bg="#94a3b8")
        self.btn_select.config(state="disabled", bg="#94a3b8")
        self.progress.start(10)
        
        # Tạo luồng chạy ngầm để gọi sang speech.py xử lý AI
        thread = threading.Thread(target=self.run_ai_processing)
        thread.daemon = True
        thread.start()

    def run_ai_processing(self):
        try:
            # Gọi hàm bóc băng từ file speech.py
            transcribe_video(self.video_path, self.log_message)
        except Exception as e:
            self.log_message(f"Lỗi hệ thống khi chạy AI: {str(e)}")
        finally:
            # Sau khi xong, dừng thanh tiến trình và khôi phục các nút bấm
            self.progress.stop()
            self.btn_select.config(state="normal", bg="#2563eb")
            self.btn_start.config(state="normal", bg="#16a34a")

    def log_message(self, message):
        current_time = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{current_time}] {message}\n"
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, formatted_message)
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

def create_app(root):
    return VideoTranslatorGUI(root)