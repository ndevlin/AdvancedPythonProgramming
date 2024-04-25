

import numpy as np

import pandas as pd

from tkinter import *


# tkinter datatable chart
def Chart(name, data):
    import pandas as pd
    #from pandastable import Table, TableModel
    window = Tk()
    window.title(name)
    window.geometry('800x600')
    frame = Frame(window)
    frame.pack(expand=True, fill=BOTH)
    #widget = Table(frame, dataframe=data, showtoolbar=False, showstatusbar=False)
    #widget.show()
    window.mainloop()
    
dfcsv = pd.read_csv("dwarfs.csv")
Chart("Dwarfs",dfcsv)
print(dfcsv)
#