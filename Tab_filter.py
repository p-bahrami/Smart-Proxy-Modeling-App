import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import cm
from matplotlib.colors import ListedColormap


class tab_filter(tk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data

        frame_1 = tk.LabelFrame(self, text="Inputs", labelanchor='n', height=170, width=310)
        frame_1.pack(padx=20, pady=(10, 5))

        label_1 = tk.Label(frame_1, text="nx:")
        label_1.place(x=17, y=2)

        self.entry_1 = tk.Entry(frame_1, textvariable=data.nx, width=7)
        self.entry_1.place(x=20, y=30)

        label_2 = tk.Label(frame_1, text="ny:")
        label_2.place(x=112, y=2)

        self.entry_2 = tk.Entry(frame_1, textvariable=data.ny, width=7)
        self.entry_2.place(x=115, y=30)

        label_3 = tk.Label(frame_1, text="nz:")
        label_3.place(x=207, y=2)

        self.entry_3 = tk.Entry(frame_1, textvariable=data.nz, width=7)
        self.entry_3.place(x=210, y=30)

        rb_1 = tk.Radiobutton(frame_1, text="Filter grids by characteristics", variable=self.data.rb_filter, value=1, command=self.hide_show2)
        rb_1.place(x=10, y=70)

        rb_2 = tk.Radiobutton(frame_1, text="Filter grids by PVT regions", variable=self.data.rb_filter, value=2, command=self.hide_show2)
        rb_2.place(x=10, y=95)

        rb_3 = tk.Radiobutton(frame_1, text="Filter grids by layers", variable=self.data.rb_filter, value=3, command=self.hide_show2)
        rb_3.place(x=10, y=120)

        self.frame_2 = tk.LabelFrame(self, text="Filtering", labelanchor='n', height=265, width=310)
        self.frame_3 = tk.LabelFrame(self, text="Filtering", labelanchor='n', height=265, width=310)
        self.frame_4 = tk.LabelFrame(self, text="Filtering", labelanchor='n', height=265, width=310)

        label_4 = tk.Label(self.frame_2, text="Desired Feature:")
        label_4.place(x=17, y=10)

        button_1 = tk.Button(self.frame_2, text="Import", command=self.opentext, width=10)
        button_1.place(x=150, y=10)

        # to automate the slider accuracy based on entering the decimal places
        def auto1():
            try:
                N = decimal[int(entry_4.get())]
                self.h_slider1.config(resolution=N)
                self.h_slider2.config(resolution=N)
                # call again after 100 ms
                self.after(100, auto1)
            except tk.TclError:
                self.after(100, auto1)
            except ValueError:
                self.after(100, auto1)
            except KeyError:
                self.after(100, auto1)

        decimal = {0: 1, 1: 0.1, 2: 0.01, 3: 0.001, 4: 0.0001, 5: 0.00001}

        label_5 = tk.Label(self.frame_2, text="L-Range of Feature:        Decimal Places:")
        label_5.place(x=17, y=50)

        entry_4 = tk.Entry(self.frame_2, textvariable=data.Dec, width=3)
        entry_4.place(x=235, y=50)

        self.h_slider1 = tk.Scale(self.frame_2, from_=0, to=450, orient="horizontal", length=240, resolution=1, state="disabled")
        self.h_slider1.place(x=17, y=70)

        label_6 = tk.Label(self.frame_2, text="H-Range of Feature:")
        label_6.place(x=17, y=130)

        self.h_slider2 = tk.Scale(self.frame_2, from_=0, to=450, orient="horizontal", length=240, resolution=1, state="disabled")
        self.h_slider2.place(x=17, y=150)

        # this keyword should be after the widget that are introduced inside the auto1() function
        auto1()

        self.button_2 = tk.Button(self.frame_2, text="Filter", command=self.filter, width=10)
        self.button_2.place(x=40, y=210)

        self.button_3 = tk.Button(self.frame_2, text="Default", width=10)
        self.button_3.place(x=150, y=210)

        self.frame_5 = tk.LabelFrame(self, height=80, width=310)
        self.frame_5.pack()

        label_7 = tk.Label(self.frame_5, text="Initial number of grids:")
        label_7.place(x=10, y=10)

        def auto2():
            global nt
            try:
                nt = data.nx.get() * data.ny.get() * data.nz.get()
                label_8.config(text=str(nt))
                # call again after 100 ms
                self.after(100, auto2)
            # this exception helps to avoid empty entry or getting string as entry
            except tk.TclError:
                self.after(100, auto2)

        label_8 = tk.Label(self.frame_5)
        label_8.place(x=190, y=10)

        auto2()

        label_9 = tk.Label(self.frame_5, text="Number of grids after filtering:")
        label_9.place(x=10, y=35)

        label_10 = tk.Label(self.frame_5, text="YYYY")
        label_10.place(x=190, y=35)

        # Trace change of Min and Max and call update_colormap as a callback
        c, canvas = None, None
        self.data.Min.trace("w", self.update_colormap)
        self.data.Max.trace("w", self.update_colormap)

    def opentext(self):
        global nums, nt
        my_file = filedialog.askopenfilenames(initialdir="/pycharm", title="Select your file",
                               filetype=(('text file', '*.txt'), ('GRDECL file', '*.GRDECL'), ('all files', '*.*')))
        for T in my_file:  # this line should be here when opening multiple files
            import re
            with open(T, 'r') as infile1:
                lines = infile1.readlines()
                B = [x for x in lines if not x.startswith('--')]
                C = " ".join(B)
                nums = []
                for n in re.findall(r'\d+\.\d+(?:e[+-]\d+|E[-+]\d+)?|\d+\*\d+\.\d+|\d+\*\d+|[0]\ |[0]\n', C):
                    split_by_ast = n.split("*")
                    if len(split_by_ast) == 1:
                        nums += [float(split_by_ast[0])]
                    else:
                        nums += [float(split_by_ast[1])] * int(split_by_ast[0])

            self.h_slider1.config(to=max(nums), state="normal")
            self.h_slider2.config(to=max(nums), state="normal")

    def plot(self, var1, var2, window):
        global c, canvas, ax, x1, y, newcmp
        var1, var2 = 1, 1
        all_time_steps = np.reshape(nums, (nt, len(nums) // nt), order='F')
        one_time_step = all_time_steps[:, (var1 - 1):var1]
        all_layers = one_time_step.reshape((self.data.nx.get() * self.data.ny.get(), self.data.nz.get()), order='F')
        one_layer = all_layers[:, (var2 - 1):var2]

        cross_section = one_layer.reshape((self.data.nx.get(), self.data.ny.get()), order='F')

        x1, y = np.mgrid[slice(0, self.data.nx.get() + 1, 1), slice(0, self.data.ny.get() + 1, 1)]

        self.figure = Figure(figsize=(7, 4.8))
        ax = self.figure.add_subplot(111)
        col_type = cm.get_cmap('rainbow', 256)
        newcolors = col_type(np.linspace(0, 1, 1000))
        white = np.array([1, 1, 1, 1])
        newcolors[:1, :] = white
        newcmp = ListedColormap(newcolors)

        c = ax.pcolormesh(x1, y, cross_section, cmap=newcmp, edgecolor='lightgrey', linewidth=0.003)
        ax.figure.colorbar(c)

        ax.set_title('My Title', fontweight="bold")
        ax.set_xlabel("Grids in X-direction", fontsize=12)
        ax.set_ylabel("Grids in Y-direction", fontsize=12)
        ax.invert_yaxis()

        self.canvas = FigureCanvasTkAgg(self.figure, window)

        self.canvas.draw()
        self.figure.patch.set_facecolor('#f0f0f0')
        toolbar = NavigationToolbar2Tk(self.canvas, self.top2)
        toolbar.place(x=10, y=0)
        self.canvas.get_tk_widget().place(x=10, y=20)

        # position of colorbar values that triggers by pressing "Plot"
        # the position of these are moved to plot() to trigger them after plotting
        self.label_13 = tk.Label(self.top2, text="Max")
        self.label_13.place(x=540, y=48)

        self.label_14 = tk.Label(self.top2, text="Min")
        self.label_14.place(x=540, y=458)

        self.entry_5 = tk.Entry(self.top2, textvariable=self.data.Max, width=3)   # to keep the entry showing on convas root should be "self"
        self.entry_5.place(x=570, y=50)

        self.entry_6 = tk.Entry(self.top2, textvariable=self.data.Min, width=3)
        self.entry_6.place(x=570, y=460)

    def open(self):
        # get the location of top left corner of root window
        xcord = self.winfo_x()
        ycord = self.winfo_y()
        self.top2 = tk.Toplevel()
        # set the size of top window and the location of that
        self.top2.geometry(f'{630}x{620}+{xcord + 665}+{ycord + 107}')
        # self.top2.resizable(False, False)

        label_11 = tk.Label(self.top2, text="Desired Timestep:")
        label_11.place(x=17, y=517)

        self.h_slider3 = tk.Scale(self.top2, from_=1, to=(len(nums) / nt), orient="horizontal", length=300, variable=self.data.timestep)
        self.h_slider3.place(x=135, y=500)

        label_12 = tk.Label(self.top2, text="Desired Layer:")
        label_12.place(x=35, y=567)

        self.h_slider4 = tk.Scale(self.top2, from_=1, to=self.data.nz.get(), orient="horizontal", length=300, variable=self.data.Slayer)
        self.h_slider4.place(x=135, y=550)

        self.h_slider3['command'] = self.update
        self.h_slider4['command'] = self.update

        self.plot(self.data.timestep.get(), self.data.Slayer.get(), self.top2)

    def update(self, *args):
        var1 = self.data.timestep.get()
        var2 = self.data.Slayer.get()
        all_time_steps = np.reshape(nums, (nt, len(nums) // nt), order='F')
        one_time_step = all_time_steps[:, (var1 - 1):var1]
        all_layers = one_time_step.reshape((self.data.nx.get() * self.data.ny.get(), self.data.nz.get()), order='F')
        one_layer = all_layers[:, (var2 - 1):var2]
        cross_section = one_layer.reshape((self.data.nx.get(), self.data.ny.get()), order='F')

        ax.pcolormesh(x1, y, cross_section, cmap=newcmp, edgecolor='lightgrey', linewidth=0.003)
        self.canvas.draw()

    def filter(self):
        global c, canvas
        self.figure.clear()

        feature = np.array(nums[0:nt])
        feature[feature < self.h_slider1.get()] = 0
        feature[feature > self.h_slider2.get()] = 0
        # active_grids = np.where(Feature != 0)[0]

        x, y = np.mgrid[slice(0, self.data.nx.get() + 1, 1), slice(0, self.data.ny.get() + 1, 1)]
        z = self.layer(feature)  # call the function layer()

        ax = self.figure.add_subplot(111)

        col_type = cm.get_cmap('rainbow', 256)
        newcolors = col_type(np.linspace(0, 1, 1000))
        white = np.array([1, 1, 1, 1])
        newcolors[:1, :] = white
        newcmp = ListedColormap(newcolors)

        c = ax.pcolormesh(x, y, z, cmap=newcmp, edgecolor='lightgrey', linewidth=0.003)
        ax.figure.colorbar(c)

        ax.set_title('My Title', fontweight="bold")
        ax.set_xlabel("Grids in X-direction", fontsize=12)
        ax.set_ylabel("Grids in Y-direction", fontsize=12)
        ax.invert_yaxis()

        self.figure.canvas.draw()

    # this function is for updating the color bar based on the entry values
    def update_colormap(self, *args, **kwargs):
        if c is not None:
            try:
                # Get vmin and vmax
                vmax, vmin = self.entry_5.get(), self.entry_6.get()
            except ValueError:
                # Could not convert values to int, non integer value
                return
            if vmin > vmax:
                return
            # Set new limits
            c.set_clim(vmin, vmax)
            # Update plot
            self.canvas.flush_events()
            self.canvas.draw()

    # it is for switching between the radiobutton of augmented points and optional points in the opened window.
    def hide_show2(self):
        if self.data.rb_filter.get() == 1:
            self.frame_3.pack_forget()
            self.frame_4.pack_forget()
            self.frame_2.pack()
        elif self.data.rb_filter.get() == 2:
            self.frame_2.pack_forget()
            self.frame_4.pack_forget()
            self.frame_3.pack()

        elif self.data.rb_filter.get() == 3:
            self.frame_2.pack_forget()
            self.frame_3.pack_forget()
            self.frame_4.pack()

        self.frame_7 = tk.LabelFrame(self, height=80, width=310)
        #self.frame_7.pack()

        self.button2_P1 = tk.Button(self.frame_2, text="Plot", command=self.open, width=10)
        self.button2_P1.place(x=90, y=190)