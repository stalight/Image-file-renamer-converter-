import os
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import sys


def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, directory)


def rename_files():
    path = path_entry.get()
    from_ext = from_var.get()
    to_ext = to_var.get()
    data["path"] = path
    data["filetype"] = from_ext
    data["filetype2"] = to_ext
    if not path or not from_ext or not to_ext:
        messagebox.showerror("Error", "All fields must be filled")
        return

    normalized_path = os.path.normpath(path)
    for root, dirs, files in os.walk(normalized_path):
        for file in files:
            if file.endswith(from_ext):
                new_filename = file.rsplit('.', 1)[0] + to_ext
                file_path = os.path.join(root, file)
                new_path = os.path.join(root, new_filename)
                try:
                    os.rename(file_path, new_path)
                    print(f"Renamed {file_path} to {new_filename}")
                except FileNotFoundError:
                    print(f"The file {file_path} does not exist")
                except PermissionError:
                    print(f"Permission denied to rename the file {file_path}")
                except Exception as e:
                    print(f"An error occurred: {e}")
    messagebox.showinfo("Success", "Files have been renamed")


def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_writable_path(relative_path):
    """ Get absolute path to writable resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(os.path.abspath("."), relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_name = "data.json"
json_file_path = get_resource_path(json_file_name)
json_writable_path = get_writable_path(json_file_name)

if os.path.exists(json_writable_path):
    # Open and read the JSON file
    with open(json_writable_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        print("JSON data read successfully:")
        print(data)
else:
    data = {"path": "", "filetype": "", "filetype2": ""}
    print(f"JSON file '{json_file_name}' does not exist in the directory '{current_directory}'")

default_path = data.get("path", "")
file1 = data.get("filetype", "")
file2 = data.get("filetype2", "")

# Create the main window
root = tk.Tk()
root.title("File Renamer")

# Create and place the widgets with minimal padding
tk.Label(root, text="Select Directory:").grid(row=0, column=0, padx=2, pady=2, sticky='w')
path_entry = tk.Entry(root, width=50)
path_entry.grid(row=0, column=1, padx=2, pady=2, sticky='w')
path_entry.insert(0, default_path)  # Set default value

tk.Button(root, text="Browse", command=select_directory).grid(row=0, column=2, padx=2, pady=2, sticky='w')

tk.Label(root, text="Settings will be automatically saved after you begin converting").grid(row=1, column=1)

tk.Label(root, text="From Extension:").grid(row=2, column=0, padx=2, pady=2, sticky='w')
from_var = tk.StringVar(root)
from_var.set(file1)  # Default value
from_menu = tk.OptionMenu(root, from_var, ".jfif", ".jpg", ".jpeg", ".png")
from_menu.grid(row=2, column=1, padx=2, pady=2, sticky='w')

tk.Label(root, text="-->").grid(row=2, column=2, padx=2, pady=2, sticky='e')

tk.Label(root, text="To Extension:").grid(row=2, column=3, padx=2, pady=2, sticky='w')
to_var = tk.StringVar(root)
to_var.set(file2)  # Default value
to_menu = tk.OptionMenu(root, to_var, ".png", ".jpg", ".jpeg", ".bmp", ".jfif")
to_menu.grid(row=2, column=4, padx=2, pady=2, sticky='w')

tk.Button(root, text="Rename Files", command=rename_files).grid(row=3, column=0, columnspan=5, pady=10)

# Run the application
root.mainloop()

print(data)
if os.path.exists(json_writable_path):
    # Write data to the JSON file
    with open(json_writable_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
        print("JSON data wrote successfully:")
        print(data)
else:
    print(f"JSON file '{json_file_name}' does not exist in the directory '{current_directory}'")
