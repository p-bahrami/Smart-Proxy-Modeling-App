from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

root = Tk()

# make your interface fullscreen
root.state('zoomed')

label_frame1 = LabelFrame(root, text="PLOT", labelanchor='n')
label_frame1.pack()

figure, ax = plt.subplots(1, 3, figsize=(20, 15))

canvas = FigureCanvasTkAgg(figure, label_frame1)
#canvas.draw()
canvas.get_tk_widget().pack()


root.mainloop()
