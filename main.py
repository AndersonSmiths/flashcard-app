import tkinter as tk
from tkinter import ttk
from app import FlashcardApp
from ttkbootstrap import Style
"""
This program allows you to run the FlashcardApp
created in file 'app.py'
"""

if __name__ == '__main__':
    root = tk.Tk()
    style = Style(theme='darkly')
    app = FlashcardApp(root)
    root.mainloop()