import tkinter as tk
from file_handler import FileHandler
import sys
import os


class ExcelProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('פעימה יצ"א - הודעות אוטומטיות לבעלי כלים')
        self.root.geometry("550x330")
        self.file_handler = FileHandler(root)
        self.file_handler.create_widgets()


if __name__ == "__main__":
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")

    root = tk.Tk()
    app = ExcelProcessorApp(root)
    root.mainloop()
