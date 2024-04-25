from tkinter import *

fudlist = ["A", "B", "C"]

top = Tk()

listbox = Listbox(top, height = 10, width = 15, bg = "black", activestyle="dotbox", font="Helvetica", fg="yellow")

top.geometry("300x250")

label = Label(top, text = "Fast Food")

for i in range(len(fudlist)):
    listbox.insert(i, fudlist[i])

label.pack()
listbox.pack()


top.mainloop()
