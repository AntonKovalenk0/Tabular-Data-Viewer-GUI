import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import pyreadstat

FOLDER_PATH = "test_for_data_associate/files"

class File:
    def __init__(self, path):
        self.path = path
        self.extension = os.path.splitext(path)[1].lower()
        self.name = os.path.basename(path)

    def read_data(self):
        try:
            if self.extension == '.sas7bdat':
                return pd.read_sas(self.path)
            elif self.extension == '.xpt':
                df, _ = pyreadstat.read_xport(self.path)
                return df
            elif self.extension in '.xlsx':
                return pd.read_excel(self.path)
            elif self.extension == '.csv':
                return pd.read_csv(self.path, sep="$")
            else:
                raise ValueError(f"File format isn't supported: {self.extension}")
        except Exception as error:
            messagebox.showerror("Error", str(error))
            return None

class Folder:
    def __init__(self, path):
        self.path = path
        self.all_files = self.get_files()
            
    def get_files(self):
        supported_extensions = ['.sas7bdat', '.xpt', '.xlsx', '.csv']
        return [
            File(os.path.join(self.path, f)) 
            for f in os.listdir(self.path) 
            if os.path.splitext(f)[1].lower() in supported_extensions
        ]

class DataViewer:
    def __init__(self, root, folder_path):
        self.root = root
        self.root.title("Table Data Viewer")
        self.root.geometry("1500x1000")

        new_folder = Folder(folder_path)
        self.current_files = new_folder.all_files
        
        self.file_list()
        self.data_frame()

    def file_list(self):
        self.file_list_frame = tk.Frame(self.root)
        self.file_list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.file_listbox = tk.Listbox(self.file_list_frame, width=30)
        self.file_listbox.pack(side=tk.TOP, fill=tk.Y)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        for file in self.current_files:
             self.file_listbox.insert(tk.END, file.name)
        
        self.sheet_listbox_frame = tk.Frame(self.file_list_frame)
        self.sheet_listbox = None

    def data_frame(self):
        self.tree_scrollbar = ttk.Scrollbar(self.root, orient="vertical")
        self.tree_scrollbar.pack(side=tk.RIGHT, fill='y')
        
        self.tree = ttk.Treeview(self.root, yscrollcommand=self.tree_scrollbar.set)
        self.tree.pack(side=tk.RIGHT, expand=True, fill='both', padx=10, pady=10)
        self.tree_scrollbar.config(command=self.tree.yview)
        
    def on_file_select(self, event):
        if self.file_listbox.curselection():
            index = self.file_listbox.curselection()[0]
            selected_file = self.current_files[index]
            
            if self.sheet_listbox:
                self.sheet_listbox.destroy()
                self.sheet_listbox = None
            
            if selected_file.extension == '.xlsx':
                excel_file = pd.ExcelFile(selected_file.path)
                
                self.sheet_listbox = tk.Listbox(self.sheet_listbox_frame, width=30)
                self.sheet_listbox.pack(side=tk.TOP, fill=tk.Y)
                self.sheet_listbox_frame.pack(side=tk.TOP, fill=tk.X)
                
                for sheet_name in excel_file.sheet_names:
                    self.sheet_listbox.insert(tk.END, sheet_name)
                
                self.sheet_listbox.bind('<<ListboxSelect>>', lambda event, ef=excel_file: self.on_sheet_select(event, ef))
            else:
                self.sheet_listbox_frame.pack_forget()
                self.display_file(selected_file)

    def on_sheet_select(self, event, excel_file):
        if self.sheet_listbox.curselection():
            sheet_name = self.sheet_listbox.get(self.sheet_listbox.curselection())
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            self.display_data(df)

    def display_file(self, file):
        df = file.read_data()
        self.display_data(df)

    def display_data(self, df):
        if df is not None:
            for i in self.tree.get_children():
                self.tree.delete(i)

            self.tree["columns"] = list(df.columns)
            self.tree["show"] = "headings"

            for column in df.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=100)

            for _, row in df.iterrows():
                self.tree.insert("", "end", values=list(row))

def main():
    root = tk.Tk()
    _ = DataViewer(root, FOLDER_PATH)
    root.mainloop()

if __name__ == "__main__":
    main()