import tkinter as tk
from tkinter import scrolledtext
from connector import Connector
from datetime import datetime

class Gui:
    def __init__(self):
        self.light_theme = {
            "bg": "#ffffff",
            "fg": "#000000",
            "entry_bg": "#f0f0f0",
            "history_bg": "#f5f5f5"
        }

        self.dark_theme = {
            "bg": "#2e2e2e",
            "fg": "#ffffff",
            "entry_bg": "#4d4d4d",
            "history_bg": "#3c3c3c"
        }

        self.current_theme = self.light_theme  # alapértelmezett
        self.title_labels = []
        self.history_labels = []

        self.connector = Connector()
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.geometry("460x550")

        # Layout: oszlop és sor méretezés engedélyezése
        self.root.grid_columnconfigure(0, weight=1)
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)

        self.create_vars()
        self.create_frames()
        self.create_labels()
        self.create_input()
        self.create_buttons()
        self.create_scrolltext()
        self.create_search_history_label()
        self.root.bind("<Return>", lambda event: self.get_weather_by_city())
        self.root.mainloop()

    def update_display(self, data):
        self.city_label.config(text=f"{data['name']} - {data['desc'].capitalize()}")
        self.temp_label.config(text=f"Hőmérséklet: {data['temperature']}°C (érzet: {data['feels_like']}°C)")
        self.wind_label.config(text=f"Szél: {data['wind']} m/s")
        self.time_label.config(text=f"Helyi idő: {data['local_time']}")
        self.sun_label.config(text=f"Napkelte: {data['sunrise']} | Napnyugta: {data['sunset']}")
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {data['name']} - {data['temperature']}°C, {data['desc']}\n"
        self.history_box.insert(tk.END, entry)
        self.history_box.see(tk.END)

    def create_vars(self):
        self.city_var = tk.StringVar()

    def create_frames(self):
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.grid(row=1, column=0, pady=10, sticky="ew")
        self.data_frame = tk.Frame(self.root)
        self.data_frame.grid(row=2, column=0, pady=10, sticky="nsew")
        self.data_frame.grid_columnconfigure(0, weight=1)
        self.frame_history = tk.Frame(self.root)
        self.frame_history.grid(row=3, column=0, pady=10, sticky="nsew")
        self.frame_history.grid_rowconfigure(1, weight=1)
        self.frame_history.grid_columnconfigure(0, weight=1)

    def create_labels(self):
        self.create_rainbow_title()

        self.city_label = tk.Label(self.data_frame, text="", font=("Helvetica", 16, "bold"))
        self.city_label.grid(row=0, column=0, pady=2, sticky="w")

        self.temp_label = tk.Label(self.data_frame, text="", font=("Helvetica", 14))
        self.temp_label.grid(row=1, column=0, pady=2, sticky="w")

        self.wind_label = tk.Label(self.data_frame, text="", font=("Helvetica", 14))
        self.wind_label.grid(row=2, column=0, pady=2, sticky="w")

        self.time_label = tk.Label(self.data_frame, text="", font=("Helvetica", 14))
        self.time_label.grid(row=3, column=0, pady=2, sticky="w")

        self.sun_label = tk.Label(self.data_frame, text="", font=("Helvetica", 14))
        self.sun_label.grid(row=4, column=0, pady=2, sticky="w")

        self.create_search_history_label()

    def create_input(self):
        self.entry = tk.Entry(self.entry_frame, textvariable=self.city_var, width=20, font=("Helvetica", 14), justify="center")
        self.entry.grid(row=0, column=0, padx=5, ipady=6, pady=(0, 5), sticky="n")
        self.entry_frame.grid_columnconfigure(0, weight=1)


    def create_buttons(self):
        button_frame = tk.Frame(self.entry_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=(5, 0))

        self.search_button = tk.Button(
            button_frame, text="Search", font=("Helvetica", 12, "bold"),
            command=self.get_weather_by_city, padx=10, pady=5, relief="ridge", borderwidth=2
        )
        self.search_button.pack(side="left", padx=5)

        self.my_location_search_button = tk.Button(
            button_frame, text="My Location", font=("Helvetica", 12, "bold"),
            command=self.get_weather_by_location, padx=10, pady=5, relief="ridge", borderwidth=2
        )
        self.my_location_search_button.pack(side="left", padx=5)

        self.theme_button = tk.Button(self.root, text="Toggle theme", command=self.switch_theme)
        self.theme_button.grid(row=4, column=0, pady=10)


    def create_scrolltext(self):
        self.history_box = scrolledtext.ScrolledText(
            self.frame_history,
            width=45,
            height=6,
            font=("Courier", 10),
            bg=self.current_theme["history_bg"]
        )
        self.history_box.grid(row=1, column=0, pady=10, sticky="nsew")

    def switch_theme(self):
        if self.current_theme == self.light_theme:
            self.current_theme = self.dark_theme
        else:
            self.current_theme = self.light_theme

        widgets = [
            self.root, self.entry_frame, self.data_frame, self.frame_history,
            self.city_label, self.temp_label, self.wind_label,
            self.time_label, self.sun_label,
        ]

        for w in widgets:
            try:
                w.configure(bg=self.current_theme["bg"], fg=self.current_theme["fg"])
            except tk.TclError:
                w.configure(bg=self.current_theme["bg"])


        self.entry.configure(bg=self.current_theme["entry_bg"], fg=self.current_theme["fg"])
        self.history_box.configure(bg=self.current_theme["history_bg"], fg=self.current_theme["fg"])

        button_bg = "#3399ff" if self.current_theme == self.dark_theme else self.current_theme["entry_bg"]
        button_fg = "#ffffff" if self.current_theme == self.dark_theme else self.current_theme["fg"]
        self.search_button.configure(bg=button_bg, fg=button_fg, activebackground="#66b2ff")
        self.my_location_search_button.configure(bg=button_bg, fg=button_fg, activebackground="#66b2ff")
        self.theme_button.configure(bg=button_bg, fg=button_fg, activebackground="#66b2ff")

        for label in self.title_labels + self.history_labels:
            label.configure(bg=self.current_theme["bg"])


    def get_weather_by_location(self):
        data = self.connector.response()
        if data:
            self.update_display(data)

    def get_weather_by_city(self):
        city = self.city_var.get().strip()
        if city:
            data = self.connector.response(city)
            if data:
                self.update_display(data)

    def create_rainbow_title(self):
        colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
        text = "Weather App"
        frame = tk.Frame(self.root, bg=self.current_theme["bg"])
        frame.grid(row=0, column=0, pady=10)

        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            label = tk.Label(frame, text=char, font=("Helvetica", 22, "bold"), fg=color, bg=self.current_theme["bg"])
            self.title_labels.append(label)
            label.pack(side="left")
    def create_search_history_label(self):
        colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
        text = "Search History:"
        frame = tk.Frame(self.frame_history, bg=self.current_theme["bg"])
        frame.grid(row=0, column=0, pady=5)

        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            label = tk.Label(frame, text=char, font=("Helvetica", 14, "bold"), fg=color, bg=self.current_theme["bg"])
            self.history_labels.append(label)
            label.pack(side="left")


Gui()