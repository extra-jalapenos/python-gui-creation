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

# Main Paned Window (Vertical, for all 3 sections)
main_paned_window = PanedWindow(root, orient=tk.VERTICAL)
main_paned_window.pack(fill=tk.BOTH, expand=True)

# Top Paned Window (Horizontal, for Data Table and Plot)
top_paned_window = PanedWindow(main_paned_window, orient=tk.HORIZONTAL)

# Data Table
data_table = ttk.Treeview(top_paned_window)
data_table.pack(expand=True, fill=tk.BOTH)
top_paned_window.add(data_table)

# Matplotlib Plot
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig)
plot_widget = canvas.get_tk_widget()
plot_widget.pack(fill=tk.BOTH, expand=True)
top_paned_window.add(plot_widget)

main_paned_window.add(top_paned_window)

# Statistics Table (New Pane)
stat_table = ttk.Treeview(main_paned_window)  # Create a new Treeview for statistics
stat_table.pack(expand=True, fill=tk.BOTH)
main_paned_window.add(stat_table)  # Add statistics pane to the main pane

#%%
# Plot Update Function

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
# Statistics Calculation and Display Function

def load_statistics():
    if os.path.exists("stock_data.xlsx"):
        df = pd.read_excel("stock_data.xlsx").drop('Date',axis=1).describe()
        df = df.reset_index()
        df.rename(columns={"index": ""}, inplace=True)

        # Clear previous Table
        for i in stat_table.get_children():
            stat_table.delete(i)

        # Set up new Table
        stat_table["column"] = list(df.columns)
        stat_table["show"] = "headings"
        for column in stat_table["column"]:
            stat_table.heading(column, text=column)
            stat_table.column(column, anchor='center')

        # Insert data into treeview
        df_rows = df.map(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x).to_numpy().tolist()
        for row in df_rows:
            stat_table.insert("", "end", values=row)

#%%

# Create a Frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# File Loading Button
file_load_button = tk.Button(button_frame, text="Load Data", command=load_data)
file_load_button.pack(side=tk.LEFT, padx=5)

# Statistics Loading Button
stat_load_button = tk.Button(button_frame, text="Load Statistics", command=load_statistics)
stat_load_button.pack(side=tk.LEFT, padx=5)

# The buttons are arranged horizontally within the button_frame by using the pack layout manager.  
# side=tk.LEFT indicates each button is placed to the immediate right of the previous one, 
# starting from the left side of the frame.

#%%
root.mainloop()