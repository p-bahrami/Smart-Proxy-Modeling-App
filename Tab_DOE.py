import tkinter as tk
from pyDOE import *
#import pandas as pd
from pandas.core.frame import DataFrame
from tkscrolledframe import ScrolledFrame
from tkinter import ttk
from tkinter import filedialog


class Tab_DOE(tk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data

        frame1 = tk.Frame(self, width=180)
        frame1.grid(row=0, column=0, padx=20, pady=3)

        self.frame2 = tk.Frame(self, width=180)
        self.frame2.grid(row=1, column=0)

        frame3 = tk.Frame(self, width=180)
        frame3.grid(row=2, column=0)

        label1 = tk.Label(frame1, text="Numeric parameters")
        label1.grid(row=0, column=0, pady=10)

        my_spinbox = tk.Spinbox(frame1, from_=2, to=15, textvariable=data.n_para)
        my_spinbox.grid(row=0, column=1, columnspan=3, sticky="w")

        label2 = tk.Label(frame1, text="(2 to 15)")
        label2.grid(row=0, column=2, padx=10)

        label3 = tk.Label(frame1, text="Name", width=17)
        label3.grid(row=1, column=0)

        label4 = tk.Label(frame1, text="Low", width=17)
        label4.grid(row=1, column=1)

        label5 = tk.Label(frame1, text="High", width=17)
        label5.grid(row=1, column=2)

        label_frame1 = tk.LabelFrame(self, text="Latin Hypercube Design", labelanchor='n')
        label_frame1.grid(row=3, column=0, pady=10)

        label6 = tk.Label(label_frame1, text="Seed:", width=32)
        label6.grid(row=0, column=0)

        entry1 = tk.Entry(label_frame1, textvariable=data.seed, width=15)
        entry1.grid(row=0, column=1, padx=10, pady=10)

        label7 = tk.Label(label_frame1, text="Initial No. sample points:", width=32)
        label7.grid(row=1, column=0)

        entry2 = tk.Entry(label_frame1, textvariable=data.n_points, width=15)
        entry2.grid(row=1, column=1, padx=10, pady=5)

        button1 = tk.Button(label_frame1, text="Run", command=self.LHS, width=10)
        button1.grid(row=2, column=0, columnspan=2, pady=10)

        self.row_list1 = []
        for i in range(2):
            entry_list1 = []
            for j in range(3):
                entryx = tk.Entry(self.frame2, width=15)
                entryx.grid(row=i + 1, column=j)
                entry_list1.append(entryx)  # Add entry to list
            self.row_list1.append(entry_list1)  # Add entry list to row

        self.bind_class("Entry", "<Down>", self.move_in_entries)
        self.bind_class("Entry", "<Up>", self.move_in_entries)
        self.bind_class("Entry", "<Right>", self.move_in_entries)
        self.bind_class("Entry", "<Left>", self.move_in_entries)

        self.data.n_para.trace('w', lambda *args: self.update1(self.frame2, self.row_list1, self.data.n_para.get(), 3))  # Trace changes in n_para

    # This function is for updating the number of rows
    def update1(self, frame, row_list, x, n_col):
        try:
            para = int(x)
        except ValueError:
            return  # Return without changes if ValueError occurs

        rows = len(row_list)
        diff = para - rows  # Compare old number of rows with entry value

        if diff == 0:
            return  # Return without changes

        elif diff > 0:  # Add rows of entries and remember them
            for row in range(rows + 1, rows + diff + 1):
                entry_list = []  # Local list for entries on this row
                for col in range(n_col):
                    e = tk.Entry(frame, width=15)
                    e.grid(row=row, column=col)
                    entry_list.append(e)  # Add entry to list
                row_list.append(entry_list)  # Add entry list to row

        elif diff < 0:  # Remove rows of entries and forget them
            for row in range(rows - 1, rows - 1 + diff, -1):
                for widget in row_list[row]:
                    widget.grid_forget()
                    widget.destroy()
                del row_list[-1]

    # This function is for moving Up/Down/Left/Right in entry grids
    def move_in_entries(self, event):
        entry = event.widget
        if event.keysym in ('Up', 'Down'):
            cols, rows = entry.master.grid_size()
            info = entry.grid_info()
            if event.keysym == 'Up':
                row = (info['row'] if info['row'] > 0 else rows) - 2     # if it was a fixed grid system, I need to change this "-2"
            else:
                row = (info['row']+0) % rows   # if it was a fixed grid system, I need to change this "0"
            self.row_list1[row][info['column']].focus()    # maybe adding a similar thing will do the navigation in the second entries##################################

        elif event.keysym == 'Left':
            entry.tk_focusPrev().focus()
        elif event.keysym == 'Right':
            entry.tk_focusNext().focus()
        return "break"

    def LHS(self):
        try:
            np.random.seed(int(self.data.seed.get()))
            self.initial_lhs_design = lhs(int(self.data.n_para.get()), samples=int(self.data.n_points.get()), criterion="corr")

        except ValueError:
            np.random.seed(int(self.data.seed.get())+1)
            self.initial_lhs_design = lhs(int(self.data.n_para.get()), samples=int(self.data.n_points.get()), criterion="corr")

        # ------------------------------------------------New Window----------------------------------------------------
        self.new_window = tk.Toplevel()
        self.new_window.geometry("400x640")
        # self.new_window.resizable(False, False)

        main_up = tk.LabelFrame(self.new_window, height=200, width=500, borderwidth=1, relief='solid')    # main upper frame
        main_up.pack(padx=10, pady=10)

        main_middle = tk.Frame(self.new_window, height=70, width=500)    # main middle frame
        main_middle.pack()
        main_middle.pack_propagate(False)  # don't shrink

        self.main_down1 = tk.LabelFrame(self.new_window, height=80, width=500, borderwidth=1, relief='solid')  # main lower frame for augmentation
        self.main_down2 = tk.LabelFrame(self.new_window, height=150, width=500, borderwidth=1, relief='solid')  # main lower frame for optional point
        self.main_down1.pack_propagate(False)

        # Objects in upper Frame
        mainx = tk.Frame(self.main_down1, height=80, width=490)  # for the entrybox
        mainx.pack()

        main1 = tk.Frame(self.main_down2, height=25, width=500)  # for the spinbox
        main2 = tk.Frame(self.main_down2, height=50, width=500)  # for the entries
        main3 = tk.Frame(self.main_down2, height=40, width=500)  # for the update button
        main1.pack()
        main2.pack()
        main3.pack()

        # Create a ScrolledFrame widget
        sf1 = ScrolledFrame(main_up, height=300, width=480)
        sf2 = ScrolledFrame(main2, height=100, width=440)
        sf1.pack()
        sf2.pack(padx=20)

        # Create a frame within the ScrolledFrame
        inner_frame1 = sf1.display_widget(tk.Frame)
        inner_frame2 = sf2.display_widget(tk.Frame)

        self.tree1 = ttk.Treeview(inner_frame1, height=self.data.n_points.get())
        self.tree1.pack()

        # Objects in middle frame


        button2 = tk.Button(main_middle, text="Export to csv.", command=self.ex)
        button2.pack()

        rb1 = tk.Radiobutton(main_middle, text="Add sample points (optimized algorithm)", variable=self.data.rb_DOE, value=1, command=self.hide_show)
        rb1.pack(anchor="w", padx=(10, 0))

        rb2 = tk.Radiobutton(main_middle, text="Add optional sample points", variable=self.data.rb_DOE, value=2, command=self.hide_show)
        rb2.pack(anchor="w", padx=(10, 0))

        # Objects in lower frame for augmentation case
        label8 = tk.Label(mainx, text="No. additional sample points")
        label8.grid(row=0, column=0, padx=10, pady=10)

        self.entryxx = tk.Entry(mainx, textvariable=self.data.n_augmented)
        self.entryxx.grid(row=0, column=1)

        self.button3 = tk.Button(mainx, text="Update", command=self.augmentation_lhs)
        self.button3.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # Objects in lower frame for optional points case
        label9 = tk.Label(main1, text="No. additional sample points")
        label9.pack(side="left", padx=10, pady=10)

        my_spinbox2 = tk.Spinbox(main1, from_=0, to=10, textvariable=self.data.n_optional)
        my_spinbox2.pack(side="right", pady=(10, 10))

        # this function is for the time we want to generate entries in the opened new window
        self.row_list2 = []
        self.data.n_optional.trace('w', lambda *args: self.update1(inner_frame2, self.row_list2, self.data.n_optional.get(), self.data.n_para.get()))  # Trace changes in n_para

        self.button4 = tk.Button(main3, text="Update", command=self.update_optional)
        self.button4.pack(pady=(10, 10))

        # Bind the arrow keys and scroll wheel
        sf1.bind_scroll_wheel(main_up)
        sf1.bind_scroll_wheel(self.tree1)
        sf2.bind_scroll_wheel(main2)     ##### I have to see later how to make the scroll work over the entries

        # To create the data list for the treeview (non-normalized)
        row_numbers = np.transpose(np.arange(1, self.data.n_points.get()+1))
        col1, self.col2, self.col3 = ["No."], [], []
        for entry in self.row_list1:
            a, b, c2 = entry[0].get(), entry[1].get(), entry[2].get()
            col1.append(a)
            self.col2.append(b)
            self.col3.append(c2)

        # For normalization of the sample points
        low = [float(x) for x in self.col2]
        high = [float(x) for x in self.col3]
        diff = list(np.array(high) - np.array(low))
        self.new_list1 = [row_numbers]
        for i in range(0, self.data.n_para.get()):
            t = low[i] + self.initial_lhs_design[:, i]*diff[i]
            self.new_list1.append(list(t))
        new_list1_tr = np.transpose(np.array(self.new_list1))
        new_list1_tr = (np.round(new_list1_tr, 3)).astype(object)
        # I used astype(object) and below line to have a mix array of integers and floats
        new_list1_tr[:, 0] = new_list1_tr[:, 0].astype(int)

        self.col_headers = []
        self.tree1['columns'] = tuple(col1)
        self.tree1.column("#0", width=0, stretch=False)
        for i in range(0, self.data.n_para.get()+1):
            # format our columns
            self.tree1.column(tuple(col1)[i], width=100, minwidth=80, anchor='center')
            # Create headings
            self.tree1.heading(tuple(col1)[i], text=col1[i])
            # col_headers will be used later in headers of the saved csv file
            self.col_headers.append(tuple(col1)[i])

        # show the entries in the treeView table
        self.count = 0
        for i in range(0, self.data.n_points.get()):
            self.tree1.insert(parent='', index='end', iid=str(self.count), values=tuple(new_list1_tr[i]))
            self.count += 1

        # Disable the underlying window
        self.new_window.grab_set()
        self.new_window.mainloop()

    # it is for switching between the radiobuttons of augmented points and optional points in the opened window.
    def hide_show(self):
        if self.data.rb_DOE.get() == 0:
            self.main_down2.pack_forget()
        elif self.data.rb_DOE.get() == 1:
            self.main_down2.pack_forget()
            self.data.n_augmented.set(0)
            self.main_down1.pack(padx=10, pady=10)
        elif self.data.rb_DOE.get() == 2:
            self.main_down1.pack_forget()
            self.data.n_optional.set(0)
            self.main_down2.pack(padx=10, pady=10)

    # Save the TreeView table to csv format
    def ex(self):
        table_row = []
        # get the values (except the headers)
        for parent1 in self.tree1.get_children():
            row = self.tree1.item(parent1)["values"]
            table_row.append(row)
        df = DataFrame(columns=[self.col_headers], data=table_row)
        export = filedialog.asksaveasfilename(title="Save as:", filetype=[("csv file(*.csv)", "*.csv")], defaultextension=[("csv file(*.csv)", "*.csv")])
        df.to_csv(export, index=False)

    # it is for getting the numbers from the treeview
    def extraction(self):
        global L3
        L = []
        for line in self.tree1.get_children():
            for value in self.tree1.item(line)['values']:
                L.append(value)
        L2 = np.array(L).reshape(int(len(L)/(self.data.n_para.get()+1)), self.data.n_para.get()+1)[:, 1:self.data.n_para.get()+1]
        # convert a list of string to a list of numbers
        L3 = np.array([list(map(float, i)) for i in L2])
        return L3

    def augmentation_lhs(self):

        def rank(arr):
            # equivalent to "order()" in R
            E1 = sorted(range(len(list(arr))), key=lambda k: arr[k])
            E2 = [x + 1 for x in E1]
            return E2

        def opt_aug(var_initial_lhs, var_m, var_mult):
            np.random.seed(int(self.data.seed.get()))
            n_col = var_initial_lhs.shape[1]
            n_row = var_initial_lhs.shape[0]

            col_vec = rank(np.random.random(n_col))
            row_vec = rank(np.random.random(n_row + var_m))

            B = np.zeros((n_row + var_m, n_col))
            for j in col_vec:
                new_row = 0
                for i in row_vec:
                    if any(((i - 1) / (n_row + var_m) <= var_initial_lhs[:, j - 1]) & (var_initial_lhs[:, j - 1] <= (i / (n_row + var_m)))) == False:
                        new_row = new_row + 1
                        B[new_row - 1, j - 1] = np.random.uniform(((i - 1) / (n_row + var_m)), (i / (n_row + var_m)))

            lhs_design = np.concatenate((var_initial_lhs, np.zeros((var_m, n_col))), axis=0)

            for k in range(1, var_m + 1):
                P = np.zeros((var_m * var_mult, n_col))
                PP = np.zeros((var_m * var_mult, n_col))

                for i in range(0, n_col):
                    L1 = B[:, i]
                    P[:, i] = np.random.randint(low=1, high=(len(L1[L1 != 0]) + 1,), size=var_m * var_mult)

                P = P.astype(int)

                for i in range(0, n_col):
                    for j in range(0, var_m * var_mult):
                        PP[j, i] = B[P[j, i] - 1, i]

                dist1 = 0
                max_dist = 2.2250738585072014e-308
                for i in range(0, var_m * var_mult - k + 1):
                    dist1 = np.zeros((1, (n_row + k - 1)))

                    for j in range(0, n_row + k - 1):
                        vec = PP[i, :] - lhs_design[j, :]
                        dist1[:, j] = np.dot(vec, vec)

                    if np.sum(dist1) > max_dist:
                        max_dist = np.sum(dist1)
                        max_row = i + 1

                lhs_design[n_row + k - 1, :] = PP[max_row - 1, :]

                for i in range(0, n_col):
                    L2 = B[:, i]

                    for j in range(0, len(L2[L2 != 0])):
                        if PP[max_row - 1, i] == B[j, i]:
                            B[j, i] = 0

                for i in range(0, n_col):
                    L3 = B[:, i]
                    if len(L3[L3 != 0]) == 0:
                        continue
                    u = len(L3[L3 != 0])
                    B[0:u, i] = L3[L3 != 0]
                    B[u:var_m, i] = 0

            return lhs_design

        # For non-normalization of the sample points extracted from treeview table
        values_extracted1 = self.extraction()
        low = [float(x) for x in self.col2]
        high = [float(x) for x in self.col3]
        diff = list(np.array(high) - np.array(low))
        non_norm = (values_extracted1 - low) / diff
        # Augment new sample points
        new_lhs2 = opt_aug(non_norm, self.data.n_augmented.get(), 100)

        # For normalization of the updated sample points
        self.new_list3 = []
        for i in range(0, self.data.n_para.get()):
            t = low[i] + new_lhs2[:, i] * diff[i]
            self.new_list3.append(list(t))
        new_list3_tr = np.round(np.transpose(np.array(self.new_list3)), 3)

        row_numbers_new = (np.transpose(np.arange(1, new_list3_tr.shape[0] + 1))).reshape(new_list3_tr.shape[0], 1)

        final_list1 = np.concatenate([row_numbers_new, new_list3_tr], axis=1).astype(object)
        final_list1[:, 0] = final_list1[:, 0].astype(int)

        # delete the values in the treeview
        for item in self.tree1.get_children():
            self.tree1.delete(item)

        # set the new height for the treeview table
        self.tree1.config(height=new_list3_tr.shape[0])

        # show the updated list in the treeView table
        count = 0
        for i in range(0, new_list3_tr.shape[0]):
            self.tree1.insert(parent='', index='end', iid=str(count), values=tuple(final_list1[i]))
            count += 1

    # get the optional numbers from entries in new_window and update it in treeview
    def update_optional(self):
        values_extracted = self.extraction()

        self.new_list2 = []
        for entry1 in self.row_list2:
            for i in range(0, self.data.n_para.get()):
                d = entry1[i].get()
                self.new_list2.append(d)
        self.new_list2_reshaped = np.array(self.new_list2).reshape((self.data.n_optional.get(), self.data.n_para.get()), order='C')

        # convert a list of string to a list of numbers
        self.new_list2_updated = np.array([list(map(float, i)) for i in self.new_list2_reshaped])

        added_list = np.concatenate([values_extracted, self.new_list2_updated], axis=0)
        row_numbers_new = (np.transpose(np.arange(1, added_list.shape[0] + 1))).reshape(added_list.shape[0], 1)

        final_list = np.concatenate([row_numbers_new, added_list], axis=1).astype(object)
        final_list[:, 0] = final_list[:, 0].astype(int)

        # delete the values in the treeview
        for item in self.tree1.get_children():
            self.tree1.delete(item)

        # set the new height for the treeview table
        self.tree1.config(height=added_list.shape[0])

        # show the updated list in the treeView table
        count = 0
        for i in range(0, added_list.shape[0]):
            self.tree1.insert(parent='', index='end', iid=str(count), values=tuple(final_list[i]))
            count += 1
    # --------------------------------------------------------------------------------------------------------------



