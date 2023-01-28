import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import pandas as pd
from openpyxl import Workbook

def select_file(filepath, df):
    # Open a file dialog to select the Excel file
    
    # Read the Excel file using pandas
    
    # Group the data by 'Date(UTC)' and aggregate the other columns
    df = df.groupby('Date(UTC)').agg({'Symbol': 'first', 'Side': 'first', 'Quantity': 'sum', 'Amount': 'sum', 'Fee': 'sum', 'Fee Coin': 'first', 'Realized Profit': 'sum', 'Quote Asset': 'first'}).reset_index()
    # Add a new column 'Price' calculated from 'Amount' and 'Quantity'
    df['Price'] = df['Amount'] / df['Quantity']
    # Create a new workbook and add a worksheet
    # Print the dataframe
    df.rename(columns={'Date(UTC)':'DateUTC+7'}, inplace=True)
    df = df[['DateUTC+7', 'Symbol', 'Price', 'Side', 'Quantity', 'Amount', 'Fee', 'Fee Coin', 'Realized Profit', 'Quote Asset']]
    df['DateUTC+7'] = pd.to_datetime(df['DateUTC+7'], utc=True) + pd.Timedelta(hours=7)
    # Create a new frame to hold the treeview and the buttons
    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)
    global tree 
    tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
    
    # add the columns to the treeview
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    # add the data to the treeview
    for i, row in df.iterrows():
        tree.insert('', 'end', values=list(row), iid=i)

    tree.bind("<ButtonRelease-1>", on_select)
    
    # set the treeview to fill the entire frame
    tree.grid(row=0, column=0, columnspan=len(df.columns), sticky='nsew')
    print(df)

def on_select(event):
    selected_item = tree.identify_row(event.y)
    col = tree.identify_column(event.x)
    col_num = int(col.replace("#", ""))
    value = tree.item(selected_item, "values")[col_num-1]
    print("Selected value:", value)


root = tk.Tk()
root.title("Excel File Selector")
try:
    filepath = "C:/Users/flukg/Downloads/Export Trade History.xlsx"
    df = pd.read_excel(filepath)
    select_file(filepath, df)
except:
    print()
    filepath = filedialog.askopenfilename()
    df = pd.read_excel(filepath)
    select_button = tk.Button(root, text="Select Excel File", command=select_file(filepath, df))
    select_button.pack()
root.mainloop()