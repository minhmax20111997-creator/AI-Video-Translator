import tkinter as tk
from tkinter import filedialog, ttk
import os
from datetime import datetime

class VideoTranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Video Translator v0.2")
        self.root.geometry("600x500")
        self.root.configure(bg="#f8f9fa")
        
        self.video_path = ""
        self.create_widgets()
        self.log_message("Ứng dụng khởi động thành công (v0.2).")

    def create_widgets(self):
        lbl_title = tk.Label(self.root, text="AI VIDEO TRANSLATOR", font=("Arial", 16, "bold"), fg="#1e293b", bg="#f8f9fa")
        lbl_title.pack(pady=15)

        file_frame = tk.LabelFrame(self.root, text=" 📂 Quản lý File ", font=("Arial", 10, "bold"), padx=15, pady=15, bg="#ffffff", fg="#475569")
        file_frame.pack(fill="x", padx=20, pady=5)
        
        self.btn_select = tk.Button(file_frame, text="Chọn Video", command=self.select_video, bg="#2563eb", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5, bd=0, cursor="hand2")
        self.btn_select.pack(side="left", padx=5)
        
        self.lbl_file_name = tk.Label(file_frame, text="Chưa chọn video nào...", fg="#94a3b8", font=("Arial", 10, "italic"), bg="#ffffff")
        self.lbl_file_name.pack(side="left", padx=15)
        
        self.btn_start = tk.Button(self.root, text="▶ Bắt đầu dịch", state="disabled", bg="#94a3b8", fg="white", font=("Arial", 12, "bold"), pady=8, bd=0)
        self.btn_start.pack(fill="x", padx=20, pady=10)

        progress_frame = tk.Frame(self.root, bg="#f8f9fa")
        progress_frame.pack(fill="x", padx=20, pady=5)
        
        lbl_progress = tk.Label(progress_frame, text="Tiến trình:", font=("Arial", 10), bg="#f8f9fa", fg="#64748b")
        lbl_progress.pack(side="left", padx=5)
        
        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.progress.pack(side="left", fill="x", expand=True, padx=5)
        
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
            self.log_message(f"Đường dẫn: {selected_file}")
        else:
            self.log_message("Hành động bị hủy: Người dùng không chọn file.")

    def log_message(self, message):
        current_time = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{current_time}] {message}\n"
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, formatted_message)
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

def create_app(root):
    return VideoTranslatorGUI(root)