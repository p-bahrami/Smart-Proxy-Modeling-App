import tkinter as tk


class Data:
    def __init__(self):
        # Variables for tab_DOE
        self.n_para = tk.IntVar()
        self.n_points = tk.IntVar()
        self.seed = tk.IntVar()
        self.n_optional = tk.IntVar()
        self.n_augmented = tk.IntVar()
        self.rb_DOE = tk.IntVar()
        # Variables for tab_filter
        self.nx = tk.IntVar()
        self.ny = tk.IntVar()
        self.nz = tk.IntVar()
        self.timestep = tk.IntVar()
        self.Slayer = tk.IntVar()
        self.Dec = tk.IntVar()
        self.Max = tk.DoubleVar()
        self.Min = tk.DoubleVar()
        self.rb_filter = tk.IntVar()