import tkinter as tk
from tkinter import ttk
from app import FlashcardApp
"""
This program allows you to run the FlashcardApp
created in file 'app.py'
"""

if __name__ == '__main__':
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()