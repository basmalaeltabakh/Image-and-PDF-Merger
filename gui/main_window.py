import tkinter as tk
from tkinterdnd2 import TkinterDnD
from tkinter import PhotoImage
from .components import ImageToPdfConverter

class MainApplication:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("Image & PDF Merger")
        self.root.geometry("900x600")
        icon = PhotoImage(file="pdf-file.png")
        self.root.iconphoto(False, icon)
        self.converter = ImageToPdfConverter(self.root)
        
    def run(self):
        self.converter.pack(fill='both', expand=True)
        self.root.mainloop()


