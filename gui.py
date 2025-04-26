import tkinter as tk
from tkinter import scrolledtext
from connector import Connector

class Gui:
    def __init__(self):
        self.connector = Connector()
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.geometry("460x550")
        self.create_vars()
        self.create_frames()
        self.create_labels()
        self.create_input()
        self.create_buttons()
        self.create_scrolltext()

        self.root.bind("<Return>", lambda event: self.connector.response(self.city_var.get()))

        self.root.mainloop()

    def create_vars(self):
        self.city_var = tk.StringVar()

    def create_frames(self):
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.grid(row=1,column=0,pady=10)
        self.data_frame = tk.Frame(self.root)
        self.data_frame.grid(row=2,column=0,pady=10)
        self.frame_history = tk.Frame(self.root)
        self.frame_history.grid(row=3,column=0,pady=10)
    def create_labels(self):
        self.title = tk.Label(self.root, text="Weather App", font=("Helvetica", 18, "bold"))
        self.title.grid(row=0,column=0,pady=5)
        self.data_label = tk.Label(self.data_frame, text="TODO", font=("Helvetica", 18, "bold"))
        self.data_label.grid(row=0,column=0,pady=5)
        self.updated_time_label = tk.Label(self.data_frame, text="Last Updated")
        self.updated_time_label.grid(row=1,column=0,pady=5)
        self.search_history = tk.Label(self.frame_history, text="Search History:", font=("Helvetica", 10, "bold"))
        self.search_history.grid(row=0,column=0,pady=5)

    def create_input(self):
        self.entry = tk.Entry(self.entry_frame, textvariable=self.city_var)
        self.entry.grid(row=0,column=0,padx=5)

    def create_buttons(self):
        self.search_button = tk.Button(self.entry_frame, text="Search", command=lambda: self.connector.response(self.city_var.get()))
        self.search_button.grid(row=0,column=1,padx=5)

        self.my_location_search_button = tk.Button(self.entry_frame, text="My Location")
        self.my_location_search_button.grid(row=0,column=2,padx=5)

        self.theme_button = tk.Button(self.root, text="Toggle theme", command=lambda: self.switch_theme())
        self.theme_button.grid(row=4,column=0)

    def create_scrolltext(self):
        self.history_box = scrolledtext.ScrolledText(self.frame_history, width=45, height=6, font=("Courier", 10), bg="#f5f5f5")
        self.history_box.grid(row=1,column=0,pady=10)
    
    def switch_theme(self):
        if self.data_label.cget("text") == "TODO":
            self.data_label.config(text="Not todo")
        else:
            self.data_label.config(text="TODO")
Gui()