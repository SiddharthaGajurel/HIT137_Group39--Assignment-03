import tkinter as tk
from gui import AIApp

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AIApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Application failed to start: {str(e)}")
