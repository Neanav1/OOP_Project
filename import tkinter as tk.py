import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tkinter Notebook Example")
frame = ttk.Frame(root, padding = 300)
frame.grid()
label = ttk.Label(frame, text="Hello, Tkinter!")
label.grid()
button = ttk.Button(frame, text="Click Me")
button.grid()


root.mainloop()
