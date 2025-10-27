from tkinter import font as tkfont
import tkinter as tk
from garage import next_garage_car, previous_garage_car, type_garage_car
from points import type_points
from utility_functions import load_data, store_data, type_text
from auth import type_text
from shop import type_car, next_car, previous_car, buy_car, type_upgrade,next_upgrade, previous_upgrade, buy_upgrade


def show_secondary_menu(user_path:str, username:str):
    root_secondary_menu = tk.Tk()
    root_secondary_menu.title("CryptoRacers")
    root_secondary_menu.resizable(False, False)

    width = 800
    height = 600

    screen_width = root_secondary_menu.winfo_screenwidth()
    screen_height = root_secondary_menu.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root_secondary_menu.geometry(f"{width}x{height}+{x}+{y}")
    root_secondary_menu.configure(bg="#191919")

    title_font = tkfont.Font(family="Impact", size=70, weight="bold")
    label_font = tkfont.Font(family="Consolas", size=17, weight="bold")
    tk.Label(root_secondary_menu, text=username, fg="white", bg="#191919", font=title_font).pack(pady=(10, 0))

    tk.Button(
            root_secondary_menu,
            text="VER PUNTOS",
            command=lambda: [root_secondary_menu.destroy(), show_points_menu(user_path, username)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=("Consolas", 14, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(50, 0))
    
    tk.Button(
            root_secondary_menu,
            text="TIENDA",
            command=lambda: [root_secondary_menu.destroy(), show_initial_shop_menu(user_path, username)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=("Consolas", 14, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(50, 0))
    
    tk.Button(
            root_secondary_menu,
            text="GARAJE",
            command=lambda: [root_secondary_menu.destroy(), show_garage_menu(user_path, username)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=("Consolas", 14, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))
    
    tk.Button(
            root_secondary_menu,
            text="PROPONER CARRERA",
            command=lambda: [root_secondary_menu.destroy()],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=("Consolas", 14, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(50, 0))
    tk.Button(
            root_secondary_menu,
            text="INICIAR CARRERA",
            command=lambda: [root_secondary_menu.destroy()],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=("Consolas", 14, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(50, 0))
    
    foot_font = tkfont.Font(family="Impact", size=20)
    tk.Label(root_secondary_menu, text="夜の峠を制覇せよ  -  Domina la noche", fg="#ffffff", bg="#111", font = foot_font).pack(pady=(70, 0))

    root_secondary_menu.mainloop()

def show_initial_shop_menu(user_path:str, user_name:str):

    root_initial_shop_menu = tk.Tk()
    root_initial_shop_menu.title("CryptoRacers")
    root_initial_shop_menu.resizable(False, False)

    width = 800
    height = 600

    screen_width = root_initial_shop_menu.winfo_screenwidth()
    screen_height = root_initial_shop_menu.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root_initial_shop_menu.geometry(f"{width}x{height}+{x}+{y}")
    root_initial_shop_menu.configure(bg="#191919")

    title_font = tkfont.Font(family="Impact", size=70, weight="bold")
    label_font = tkfont.Font(family="Consolas", size=17, weight="bold")
    tk.Label(root_initial_shop_menu, text=user_name, fg="white", bg="#191919", font=title_font).pack(pady=(10, 0))

    tk.Button(
            root_initial_shop_menu,
            text="COCHES",
            command=lambda: [root_initial_shop_menu.destroy(), show_cars_shop_menu(user_path, user_name)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=("Consolas", 14, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(50, 0))
    
    tk.Button(
            root_initial_shop_menu,
            text="MEJORAS",
            command=lambda: [root_initial_shop_menu.destroy(), show_upgrades_shop_menu(user_path, user_name)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=("Consolas", 14, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))
    tk.Button(
            root_initial_shop_menu,
            text="ATRÁS",
            command=lambda: [root_initial_shop_menu.destroy(), show_secondary_menu(user_path, user_name)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=("Consolas", 14, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))

    root_initial_shop_menu.mainloop()

def show_cars_shop_menu(user_path:str, user_name:str):
    car_data = load_data("Shop_info/cars_shop.json")

    root_cars_shop_menu = tk.Tk()
    root_cars_shop_menu.title("Cars Shop CryptoRacers")
    root_cars_shop_menu.resizable(False, False)

    # Tamaño y centrado
    width = 800
    height = 600
    screen_width = root_cars_shop_menu.winfo_screenwidth()
    screen_height = root_cars_shop_menu.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root_cars_shop_menu.geometry(f"{width}x{height}+{x}+{y}")
    root_cars_shop_menu.configure(bg="#191919")

    # --- Estilo general ---
    title_font = tkfont.Font(family="Impact", size=70, weight="bold")
    label_font = tkfont.Font(family="Consolas", size=17, weight="bold")
    button_font = tkfont.Font(family="Consolas", size=12, weight="bold")
    # --- Título estilo "CryptoRacers" ---
    tk.Label(root_cars_shop_menu, text=user_name, fg="white", bg="#191919", font=title_font).pack(pady=(10, 0))

    tk.Button(
            root_cars_shop_menu,
            text="SIGUIENTE COCHE",
            command=lambda: [next_car(car_data, terminal)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))
    
    tk.Button(
            root_cars_shop_menu,
            text="ANTERIOR COCHE",
            command=lambda: [previous_car(car_data, terminal)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))
    tk.Button(
            root_cars_shop_menu,
            text="COMPRAR",
            command=lambda: [buy_car(car_data, user_path, terminal)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))
    tk.Button(
            root_cars_shop_menu,
            text="ATRÁS",
            command=lambda: [root_cars_shop_menu.destroy(), show_initial_shop_menu(user_path, user_name)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))

    # --- Área tipo terminal ---
    terminal = tk.Text(root_cars_shop_menu, width=70, bg="#0e0e0e", fg="#29FFF4",
                       insertbackground="white", font=("Consolas", 11), relief="flat")
    terminal.pack(pady=(0, 20))
    type_car(car_data, terminal)

    root_cars_shop_menu.mainloop()

def show_upgrades_shop_menu(user_path:str, user_name:str):
    upgrades_data = load_data("Shop_info/upgrades_shop.json")

    root_upgrades_shop_menu = tk.Tk()
    root_upgrades_shop_menu.title("Cars Shop CryptoRacers")
    root_upgrades_shop_menu.resizable(False, False)

    # Tamaño y centrado
    width = 800
    height = 600
    screen_width = root_upgrades_shop_menu.winfo_screenwidth()
    screen_height = root_upgrades_shop_menu.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root_upgrades_shop_menu.geometry(f"{width}x{height}+{x}+{y}")
    root_upgrades_shop_menu.configure(bg="#191919")

    # --- Estilo general ---
    title_font = tkfont.Font(family="Impact", size=70, weight="bold")
    label_font = tkfont.Font(family="Consolas", size=17, weight="bold")
    button_font = tkfont.Font(family="Consolas", size=12, weight="bold")
    # --- Título estilo "CryptoRacers" ---
    tk.Label(root_upgrades_shop_menu, text=user_name, fg="white", bg="#191919", font=title_font).pack(pady=(10, 0))

    tk.Button(
            root_upgrades_shop_menu,
            text="SIGUIENTE MEJORA",
            command=lambda: [next_upgrade(upgrades_data, terminal)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(0, 0))
    
    tk.Button(
            root_upgrades_shop_menu,
            text="ANTERIOR MEJORA",
            command=lambda: [previous_upgrade(upgrades_data, terminal)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))
    car_upgrade_entry = tk.Entry(root_upgrades_shop_menu, font=("Consolas", 12), justify="center", bg="#2c2c2c", fg="white", insertbackground="white", relief="flat", width=30)
    car_upgrade_entry.pack(pady=(0, 0))
    tk.Button(
            root_upgrades_shop_menu,
            text="COMPRAR",
            command=lambda: [buy_upgrade(upgrades_data, terminal, user_path, car_upgrade_entry.get())],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))
    tk.Button(
            root_upgrades_shop_menu,
            text="ATRÁS",
            command=lambda: [root_upgrades_shop_menu.destroy(), show_initial_shop_menu(user_path, user_name)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))

    # --- Área tipo terminal ---
    terminal = tk.Text(root_upgrades_shop_menu, width=70, bg="#0e0e0e", fg="#29FFF4",
                       insertbackground="white", font=("Consolas", 11), relief="flat")
    terminal.pack(pady=(0, 20))
    type_upgrade(upgrades_data, terminal)

    root_upgrades_shop_menu.mainloop()

def show_points_menu(user_path:str, user_name:str):
    root_points_menu = tk.Tk()
    root_points_menu.title("Cars Shop CryptoRacers")
    root_points_menu.resizable(False, False)

    # Tamaño y centrado
    width = 800
    height = 600
    screen_width = root_points_menu.winfo_screenwidth()
    screen_height = root_points_menu.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root_points_menu.geometry(f"{width}x{height}+{x}+{y}")
    root_points_menu.configure(bg="#191919")

    # --- Estilo general ---
    title_font = tkfont.Font(family="Impact", size=70, weight="bold")
    label_font = tkfont.Font(family="Consolas", size=17, weight="bold")
    button_font = tkfont.Font(family="Consolas", size=12, weight="bold")
    # --- Título estilo "CryptoRacers" ---
    tk.Label(root_points_menu, text=user_name, fg="white", bg="#191919", font=title_font).pack(pady=(10, 0))

    tk.Button(
            root_points_menu,
            text="ATRÁS",
            command=lambda: [root_points_menu.destroy(), show_secondary_menu(user_path, user_name)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))

    # --- Área tipo terminal ---
    terminal = tk.Text(root_points_menu, width=70, bg="#0e0e0e", fg="#29FFF4",
                       insertbackground="white", font=("Consolas", 11), relief="flat")
    terminal.pack(pady=(0, 20))
    type_points(user_path, terminal)

    root_points_menu.mainloop()

def show_garage_menu(user_path:str, user_name:str):

    root_garage_menu = tk.Tk()
    root_garage_menu.title("Cars Shop CryptoRacers")
    root_garage_menu.resizable(False, False)

    # Tamaño y centrado
    width = 800
    height = 600
    screen_width = root_garage_menu.winfo_screenwidth()
    screen_height = root_garage_menu.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root_garage_menu.geometry(f"{width}x{height}+{x}+{y}")
    root_garage_menu.configure(bg="#191919")

    # --- Estilo general ---
    title_font = tkfont.Font(family="Impact", size=70, weight="bold")
    label_font = tkfont.Font(family="Consolas", size=17, weight="bold")
    button_font = tkfont.Font(family="Consolas", size=12, weight="bold")
    # --- Título estilo "CryptoRacers" ---
    tk.Label(root_garage_menu, text=user_name, fg="white", bg="#191919", font=title_font).pack(pady=(10, 0))

    tk.Button(
            root_garage_menu,
            text="SIGUIENTE COCHE",
            command=lambda: [next_garage_car(user_path, terminal)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))
    
    tk.Button(
            root_garage_menu,
            text="ANTERIOR COCHE",
            command=lambda: [previous_garage_car(user_path, terminal)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))

    tk.Button(
            root_garage_menu,
            text="ATRÁS",
            command=lambda: [root_garage_menu.destroy(), show_secondary_menu(user_path, user_name)],
            fg="white",
            bg="#ac3333",
            activebackground="#bd6c6c",
            activeforeground="white",
            font=button_font,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=(20, 0))

    # --- Área tipo terminal ---
    terminal = tk.Text(root_garage_menu, width=70, bg="#0e0e0e", fg="#29FFF4",
                       insertbackground="white", font=("Consolas", 11), relief="flat")
    terminal.pack(pady=(0, 20))
    type_garage_car(user_path, terminal)

    root_garage_menu.mainloop()