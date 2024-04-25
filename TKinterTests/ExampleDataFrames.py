import pandas as pd
import numpy as np
from tkinter import *
import matplotlib.pyplot as plt


from pyvirtualdisplay import Display


display = Display(visible=0, size=(800, 600))
display.start()

# Now you can create your Tkinter window
window = Tk()


print([print(hex(c),chr(c)) for c in range(32,255)])

# indices
dwarfHeader = ["Dwarf","Distance(AU)","Period(years)"]
print("\ndwarfHeader: \n",dwarfHeader)

dwarfIndex = ['dwarf0','dwarf1','dwarf2','dwarf3','dwarf4','dwarf5','dwarf6','dwarf7','dwarf8']
print("\ndwarfHeader: \n",dwarfIndex)

# pdseries list data
dwarfDetail = [
pd.array(["Ceres",2.77,4.61]),
pd.Series(["Pluto",39.5,247.69]),
pd.Series(["Haumea",43.19,283.84]),
pd.Series(["Makemake",45.48,306.17]),
pd.Series(["Eris",67.84,558.77]),
pd.Series(["Orcus",39.22,245.62]),
pd.Series(["Ixion",39.70,250.18]),
pd.Series(["Quaoar",43.12,287.97]),
pd.Series(["Sedna",488.98,10812.82],index=dwarfHeader) ]
print("\ndwarfDetail: \n",dwarfDetail)

# create dataframe from pdseries list
dfdwarfs = pd.DataFrame(data=dwarfDetail)
print("\ndfdwarfs: \n",dfdwarfs)
dfdwarfs = pd.DataFrame(data=dwarfDetail,index=dwarfIndex)
print("\ndfdwarfs[]: \n",dfdwarfs[0:])

# print using iloc (index location)
print("\ndfdwarfs[row][col] indexing\n")
for r in range(len(dfdwarfs)):
    for c in range(len(dfdwarfs.iloc[r])):
        print('row'+str(r)+' col'+str(c)+':'+str(dfdwarfs.iloc[r][c]))

# print using slicing
print("\nslice\n",dfdwarfs[0:len(dfdwarfs)])

# get the data for [Eris]
print("\nEris data\n")
eris = 4
print(dfdwarfs[0][eris])
print(dfdwarfs[1][eris])
print(dfdwarfs[2][eris])

# dframe -> dictionary
dwarfdic = dfdwarfs.to_dict()
print("\ndictionary\n",dwarfdic)

# dframe -> html
dwarfhtml = dfdwarfs.to_html()
print("\nhtml\n",dwarfhtml)

# dframe -> numpy
dwarfnpy = dfdwarfs.to_numpy()
print("\nnumpy\n",dwarfnpy)

print("\ncsvwithaverage************************")
dfcsv = pd.read_csv("Dwarfs.csv",delimiter=',')
print(dfcsv)
print('Average Distance: '+str(dfcsv['Distance(AU)'].mean()))
print('Average Period:   '+str(dfcsv['Period(years)'].mean()))

# matplotlib
dfplot = pd.DataFrame(dfcsv)
dfplot.plot()
plt.show()

# tkinter datatable chart
def Chart(name, data):
    import pandas as pd
    from pandastable import Table, TableModel
    window = Tk()
    window.title(name)
    window.geometry('800x600')
    frame = Frame(window)
    frame.pack(expand=True, fill=BOTH)
    widget = Table(frame, dataframe=data, showtoolbar=False, showstatusbar=False)
    widget.show()
    window.mainloop()
    
dfcsv = pd.read_csv("Dwarfs.csv")
Chart("Dwarfs",dfcsv)
print(dfcsv)
#