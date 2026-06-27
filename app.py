import tkinter as tk
from gui import create_app

if __name__ == "__main__":
    root = tk.Tk()
    app = create_app(root)
    root.mainloop()
