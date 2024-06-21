import os
import pandas as pd
import datetime as dt
import yfinance as yf
import tkinter as tk
from tkinter import filedialog, ttk, PanedWindow
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


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

root = tk.Tk()
root.title("Stock Data Analyzer")
root.geometry('1200x600')

# Paned Window (for Data Table and Plot)
# Creates a sliding door that moves horizontally, 
# splitting the room into two sections. 
# You can then adjust the door's position to make one section larger and the other smaller.
paned_window = PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

# Data Table
data_table = ttk.Treeview(paned_window)
data_table.pack(expand=True, fill=tk.BOTH)
paned_window.add(data_table)

# Matplotlib Plot
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig)
plot_widget = canvas.get_tk_widget()
plot_widget.pack(fill=tk.BOTH, expand=True)
paned_window.add(plot_widget)

#%%
# Plot Update Function
# The update_plot function is essential for refreshing the chart. 
# It allows us to redraw the plot with new data or when the user selects different columns 
# or time granularities.

def update_plot(df, column='High'):  # Make column adjustable
    """Updates the plot with data from the given DataFrame."""
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(df['Date'],df[column]) 
    ax.set_title('Price')
    ax.set_xlabel('Date')
    ax.set_ylabel(column)
    canvas.draw()

#%%
# Data Loading and Display Function

def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")])
    if file_path:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        # Convert Date Column from String to Datetime
        df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')

        # Clear previous Table
        for i in data_table.get_children():
            data_table.delete(i)

        # Set up new Table
        data_table["column"] = list(df.columns)
        data_table["show"] = "headings"
        for column in data_table["column"]:
            data_table.heading(column, text=column)
            data_table.column(column, anchor='center')

        df_rows = df.map(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x).to_numpy().tolist()
        for row in df_rows:
            data_table.insert("", "end", values=row)
        
        update_plot(df)

#%%
# File Loading Button
file_load_button = tk.Button(root, text="Load Data", command=load_data)
file_load_button.pack(pady=5)

#%%
root.mainloop()