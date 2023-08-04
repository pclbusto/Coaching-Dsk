import tkinter as tk
from tkinter import ttk

main_window = tk.Tk()
main_window.title("Vista de árbol en Tkinter")
treeview = ttk.Treeview(columns=("size", "lastmod"))
treeview.insert(
    "",
    tk.END,
    text="README.txt",
    values=("850 bytes", "18:30")
)
treeview.pack()
main_window.mainloop()