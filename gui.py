import yfinance as yf
import pandas as pd
import datetime as dt
import tkinter as tk
from tkinter import filedialog, ttk
import os

def fetch_data(ticker, start_date, end_date):
	try:
		data = yf.download(ticker, start_date, end_date)
		data = data.reset_index()
		data.to_excel("stock_data.xlsx")
		return data
	except:
		print("error fetching data")
		return None


if not os.path.exists("stock_data.xlsx"):
	data = fetch_data("AAPL", dt.datetime(2023,1,1), dt.datetime.now())
	print(data)
else:
	data = pd.read_excel("stock_data.xlsx")

# GUI setup
root = tk.Tk()
root.title("Stock Data Analyzer")
root.geometry("1200x600")

data_table = ttk.Treeview(root)
data_table.pack(pady=20, expand=True, fill= tk.BOTH)

def load_data():
	file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")])
	if file_path:
		if file_path.endswith(".csv"):
			df = pd.read_csv(file_path)
		else:
			df = pd.read_excel(file_path)

		for i in data_table.get_children():
			data_table.delete(i)

		data_table["column"] = list(df.columns)
		data_table["show"] = "headings"

		for column in data_table["column"]:
			data_table.heading(column, text=column) # add heading

		df_rows = df.to_numpy().tolist()
		for row in df_rows:
			data_table.insert("", "end", values=row)

# file load button
file_load_button = tk.Button(root, text="Load data", command=load_data)
file_load_button.pack(pady=5)

root.mainloop()
