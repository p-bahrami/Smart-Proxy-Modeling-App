import tkinter as tk


class tab_import(tk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data