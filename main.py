import tkinter as tk
from tkinter import ttk

from Data import Data
from Tab_DOE import Tab_DOE
from Tab_filter import tab_filter
from Tab_import import tab_import

# Title_Font = ("Helvetica", 14, "bold")
Title_Font = ("Helvetica", 12)
Label_Font = ("Helvetica", 10)
Button_Font = ("Helvetica", 12)


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Smart Proxy Modeling Software")
        #self.iconbitmap("LOGO.ico")

        # get the screen size of your computer
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Get the window position from the top dynamically as well as position from left or right as follows
        position_top = int(screen_height / 2 - 600 / 2)
        position_right = int(screen_width / 2 - 400 / 2 - 300)
        # this is the line that will center your window
        self.geometry(f'{400}x{600}+{position_right}+{position_top}')

        self.minsize(400, 600)
        self.maxsize(400, 600)

        self.my_notebook = ttk.Notebook(self)
        self.my_notebook.pack(fill="both", expand=True)

        self.app_data = {}
        self.app_data = Data()
        self.frames = {}
        self.data = Data()

        dic_tabs = {Tab_DOE: "Design of Experiments", tab_filter: "Filtering", tab_import: "Importing"}
        for a1, a2 in dic_tabs.items():
            tab = a1(self.my_notebook, self.app_data)
            self.my_notebook.add(tab, text=a2)

        # self.frames[PageOne].button3_P1.config(command=self.go_to_page_two)
        # self.show_frame(PageOne)

        # Adding Menu bars
        def our_command():
            pass

        self.my_menu = tk.Menu(self)
        self.config(menu=self.my_menu)

        self.file_menu = tk.Menu(self.my_menu, activeborderwidth=2, tearoff="off")
        self.my_menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='New', command=our_command)
        self.file_menu.add_command(label='Save', command=our_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.quit)

        self.about_menu = tk.Menu(self, activeborderwidth=2, tearoff="off")
        self.my_menu.add_cascade(label='About Us', menu=self.about_menu)
        self.about_menu.add_command(label='Software Info', command=our_command)

    def go_to_page_two(self):
        self.show_frame(tab_import)

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()


app = SampleApp()
app.mainloop()