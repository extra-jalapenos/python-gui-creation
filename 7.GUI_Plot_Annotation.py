import os
import pandas as pd
import datetime as dt
import yfinance as yf
import tkinter as tk
from tkinter import filedialog, ttk, PanedWindow
from matplotlib.figure import Figure
import matplotlib.dates as mdates
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

file_path = None
    
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
data_table.pack(expand=True, fill='both')
top_paned_window.add(data_table)

# Matplotlib Plot
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
plot_widget = canvas.get_tk_widget()
plot_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
top_paned_window.add(plot_widget)

main_paned_window.add(top_paned_window)

# Statistics Table (New Pane)
stat_table = ttk.Treeview(main_paned_window)  # Create a new Treeview for statistics
stat_table.pack(expand=True, fill='both')
main_paned_window.add(stat_table)  # Add statistics pane to the main pane

#%%
# Plot Update Function

def update_plot(df, resample_rule='D', columns=['High']):
    """Updates the plot with data from the given DataFrame and resampling rule."""
    
    # Resample data based on the selected rule
    if resample_rule == 'D':
        resampled_df = df
    else:   
        df.index = df['Date']
        df = df.drop(['Date'],axis=1)
        resampled_df = df.resample(resample_rule).mean().reset_index()
        resampled_df['Date'] = pd.to_datetime(resampled_df['Date'])

    fig.clear()
    ax = fig.add_subplot(111)
    for column in columns:  # Plot each selected column
        ax.plot(resampled_df['Date'], resampled_df[column], label=column)
        
    ax.set_title(f'Prices ({resample_rule} Granularity)')
    ax.set_xlabel('Date')
    ax.legend()
    
    # --- CURSOR INTERACTION ---
    
    # This code creates an initially hidden text box (annot) that will be used to 
    # display information when the user hovers over the plot. 
    # The text box is positioned slightly offset from the data point being hovered over.
    ### Is initially empty and hidden.
    ### Will appear 20 pixels to the left and 20 pixels above the data point being hovered over.
    ### textcoords="offset points": This tells Matplotlib to interpret the xytext argument 
        # as an offset from the data point in units of points (not data coordinates). 
        # This means the annotation will always be a fixed distance away from the data point, 
        # regardless of how the plot is zoomed or panned.
    ### Has a rounded rectangular white background box to make the text more readable against the plot.
    annot = ax.annotate("", xy=(0,0), xytext=(-20, 20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"))
    annot.set_visible(False)


    # This function update_annot positions an annotation box at the specified (x, y) 
    # coordinates and sets its text content to a formatted string displaying the 
    # corresponding date and numerical value.
    def update_annot(x, y):
        """Updates the annotation text with date and value."""
        annot.xy = (x, y)
        # Format x as date and y to 2 decimal places
        # Matplotlib internally represents dates as floating-point numbers, 
        # where each integer value represents a day and fractional values represent parts of a day.
        # This numerical representation is often the number of days that have 
        # passed since a specific reference point, which is usually January 1st, 1970
        text = f"Date: {mdates.num2date(x).strftime('%Y-%m-%d')}\nValue: {y:.2f}"
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)
    
    
    # This function hover controls the visibility of an annotation box (annot) 
    # when the mouse hovers over the plot (ax). It updates the annotation with 
    # the current data point's coordinates if the cursor is inside the plot area, 
    # otherwise it hides the annotation.

    def hover(event):
        """Shows/hides the annotation based on cursor position."""
        # This line gets the current visibility status (True or False) of the annotation 
        # and stores it in the variable vis.
        vis = annot.get_visible() # 
        if event.inaxes == ax:
            update_annot(event.xdata, event.ydata)
            annot.set_visible(True)
            fig.canvas.draw_idle()  # For an efficient and smooth plot update
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()
    
    # This line connects the hover function to the Matplotlib plot's "mouse movement" 
    # event, triggering it whenever the mouse moves over the plot area.
    fig.canvas.mpl_connect("motion_notify_event", hover)
    
    canvas.draw()

#%%
# Data Loading and Display Function

def load_data():
    global file_path
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
    global file_path
    if os.path.exists(file_path):
        df = pd.read_excel(file_path).drop('Date',axis=1).describe()
        df = df.reset_index()
        df.rename(columns={"index": ""}, inplace=True)

        # Clear previous treeview
        for i in stat_table.get_children():
            stat_table.delete(i)

        # Set up new treeview
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
# Resampling Function

def select_granularity():
    global file_path
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        
        # Get selected columns from the Listbox
        selected_columns = [column_listbox.get(i) for i in column_listbox.curselection()]
        if not selected_columns:
            selected_columns = ['High']  # Default if nothing selected
        
        update_plot(df, selected_granularity.get(), selected_columns)
        

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

# List Option Buttons (for granularity)
selected_granularity = tk.StringVar(value='D')  # Default to daily
ttk.Label(button_frame, text="Select Granularity:").pack(side=tk.LEFT, padx=5)  # Label for the options
ttk.Radiobutton(button_frame, text="Daily", variable=selected_granularity, value='D', command=lambda: select_granularity()).pack(anchor=tk.W,side=tk.LEFT, padx=5)
ttk.Radiobutton(button_frame, text="Weekly", variable=selected_granularity, value='W', command=lambda: select_granularity()).pack(anchor=tk.W,side=tk.LEFT, padx=5)
ttk.Radiobutton(button_frame, text="Monthly", variable=selected_granularity, value='M', command=lambda: select_granularity()).pack(anchor=tk.W,side=tk.LEFT, padx=5)

# Listbox for Selecting Columns
ttk.Label(button_frame, text="Select Columns to Plot:").pack(side=tk.LEFT, padx=5)
column_listbox = tk.Listbox(button_frame, selectmode=tk.MULTIPLE)
column_listbox.pack(side=tk.LEFT, padx=5, pady=5)
column_listbox.bind("<<ListboxSelect>>", lambda event: select_granularity())

# Add items to the Listbox
for column in ['Open', 'High', 'Low', 'Close']:
    column_listbox.insert(tk.END, column)

#%%
root.mainloop()