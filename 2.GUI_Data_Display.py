import os
import pandas as pd
import datetime as dt
import yfinance as yf
import tkinter as tk
from tkinter import filedialog, ttk


#%%

def fetch_data(ticker, start_date, end_date):
    """Fetches stock data from Yahoo Finance and saves it to an Excel file."""
    try:
        data = yf.download(ticker, start_date, end_date)
        data.reset_index(inplace=True)
        data.to_excel("stock_data.xlsx", index=False)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Check if stock_data.xlsx exists
if not os.path.exists("stock_data.xlsx"):
    initial_data = fetch_data('AAPL', dt.datetime(2023, 1, 1), dt.datetime.now())
else:
    # If it exists, read it into the DataFrame
    initial_data = pd.read_excel("stock_data.xlsx")
    
#%%
# GUI Setup

# This line creates the main window for our application. 
# Think of the root as the blank canvas where we'll add all other GUI elements. 
# Its like a root of tree, which anchors all other parts
root = tk.Tk()
root.title("Stock Data Analyzer")
root.geometry('1200x600')


# This creates the table to display our stock data, 
# making it expandable to fit any new data we load, and 
# adding some space above for visual clarity.
# The Treeview is basically a widget in Tkinter which is primarily used for displaying hierarchical data 
# (like a tree with parent-child relationships). However, you can also use it to display 
# non-hierarchical, tabular data.

data_table = ttk.Treeview(root)
data_table.pack(pady=20, expand=True, fill=tk.BOTH) 
# The pack method is used to organise the widgets in the parent widget. It determines how they are placed.
# tk.Both means take up all available space within its container, both horizontally and vertically.

#%%
# Data Loading and Display Function

def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")])
    if file_path:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # This line clears out all the rows in our data table to 
        # prepare it for displaying fresh information.
        for i in data_table.get_children():
            data_table.delete(i)


        # Set up new Table
        data_table["column"] = list(df.columns)
        
        
        # By default (show='tree'), the Treeview would try to display both the hierarchical structure 
        # (which doesn't exist in your data) and the column headings.
        # Setting show="headings" tells the Treeview to ignore any 
        # tree structure and because the data is in tabular format.
        data_table["show"] = "headings"
        
        
        for column in data_table["column"]:
            data_table.heading(column, text=column) # Shows the headings
            
            # Adjusting column headers and cell content alignment to center
            #------------------------------------------------1111111111111111------------------------------------------------------
            data_table.column(column, anchor='center')

        # Insert data into treeview
        # ----------------------------------------------------2222222222222222-----------------------------------
        # df_rows = df.to_numpy().tolist()
        # for row in df_rows:
        #     data_table.insert("", "end", values=row)

        #-----------------------------------------------------3333333333333333-----------------------------------
        # The line applies a custom function to each cell in the DataFrame, formatting numeric values to 
        # two decimal places while leaving other data types untouched. The resulting 
        # formatted DataFrame is then converted into a NumPy array and subsequently into 
        # a list of lists, with each inner list representing a row of data. 
        # The code then iterates over these rows, inserting each one into the 
        # Treeview widget, effectively populating the table with the formatted stock information.
        
        df_rows = df.map(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x).to_numpy().tolist()
        for row in df_rows:
            data_table.insert("", "end", values=row)

#%%
# File Loading Button
file_load_button = tk.Button(root, text="Load Data", command=load_data)
file_load_button.pack(pady=5)

#%%
# This line starts the main loop of our application. 
# It keeps the window open, responds to user interactions, and keeps our interface running smoothly.
root.mainloop()