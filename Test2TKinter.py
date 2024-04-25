import tkinter as tk
from tkinter import ttk

def populate_listbox(data):
    for item in data:
        listbox.insert("", "end", values=item)

sample_data = [("John", "Doe", 25),
               ("Jane", "Smith", 30),
               ("Bob", "Johnson", 22),]

root = tk.Tk()
root.title("Hello!")
columns = ("First Name", "Last Name", "Age")

listbox = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    listbox.heading(col, text=col)
    listbox.column(col, width=100)

populate_listbox(sample_data)

listbox.pack(pady=10)

root.mainloop()


import tkinter
#print('tkinter version:', tkinter.__version__)
print('tk version:', tkinter.TkVersion)
print('tcl version:', tkinter.TclVersion)
import tkinter.ttk as ttk
print('ttk version:', ttk.__version__)
