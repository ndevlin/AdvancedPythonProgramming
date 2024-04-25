'''
Nathan Devlin
TKinter
April 24th
'''


import tkinter as tk
from tkinter import ttk
import pandas as pd

def display_dataframe(df):
    root = tk.Tk()
    root.title("DataFrame Display")

    # Create the tab control
    tab_control = ttk.Notebook(root)

    # Create the tabs
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)

    # Add the tabs to the tab control
    tab_control.add(tab1, text='DataFrame')
    tab_control.add(tab2, text='Headers')
    tab_control.add(tab3, text='Indices')

    # Pack the tab control
    tab_control.pack(expand=1, fill='both')

    # Function to create a table in a tab
    def create_table(tab, rows, cols):
        for r in range(rows):
            for c in range(cols):
                cell = ttk.Label(tab, text=df.iat[r, c] if r < df.shape[0] and c < df.shape[1] else "")
                cell.grid(row=r, column=c)

    # Create the tables
    create_table(tab1, df.shape[0], df.shape[1])  # DataFrame
    create_table(tab2, 1, df.shape[1])  # Headers
    create_table(tab3, df.shape[0], 1)  # Indices

    root.mainloop()

# Test the function
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

display_dataframe(df)