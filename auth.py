# auth.py
import os
import hashlib
import base64
from time import sleep
import tkinter as tk
from tkinter import font as tkfont
from utility_functions import load_data, store_data, type_text
import re
from main_program import show_secondary_menu

DEFAULT_ITERATIONS = 200_000
USERS_FILE = "Passwords/users.json"
PEPPER = "practica_crypto_racers"

#### SHOW WINDOWS ####
def show_initial_window():
    root_initial = tk.Tk()
    root_initial.title("CryptoRacers")
    root_initial.resizable(False, False)

    width = 800
    height = 600

    screen_width = root_initial.winfo_screenwidth()
    screen_height = root_initial.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root_initial.geometry(f"{width}x{height}+{x}+{y}")
    root_initial.configure(bg="#191919")

    title_font = tkfont.Font(family="Impact", size=70, weight="bold")
    tk.Label(root_initial, text="CRYPTO", fg="white", bg="#191919", font=title_font).pack(pady=(10, 0))
    tk.Label(root_initial, text="RACERS", fg="#ff0000", bg="#191919", font=title_font).pack()

    tk.Button(
            root_initial,
            text="INICIAR SESIÓN",
            command=lambda: [root_initial.destroy(), show_login_window()],
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
            root_initial,
            text="REGISTRARSE",
            command=lambda: [root_initial.destroy(), show_register_window()],
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

    foot_font = tkfont.Font(family="Impact", size=20)
    tk.Label(root_initial, text="夜の峠を制覇せよ  -  Domina la noche", fg="#ffffff", bg="#111", font = foot_font).pack(pady=(70, 0))

    root_initial.mainloop()

def show_login_window():
    root_login = tk.Tk()
    root_login.title("Login CryptoRacers")
    root_login.resizable(False, False)

    # Tamaño y centrado
    width = 800
    height = 600
    screen_width = root_login.winfo_screenwidth()
    screen_height = root_login.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root_login.geometry(f"{width}x{height}+{x}+{y}")
    root_login.configure(bg="#191919")

    # --- Estilo general ---
    title_font = tkfont.Font(family="Impact", size=70, weight="bold")
    label_font = tkfont.Font(family="Consolas", size=17, weight="bold")
    button_font = tkfont.Font(family="Consolas", size=12, weight="bold")
    # --- Título estilo "CryptoRacers" ---
    tk.Label(root_login, text="INICIO SESIÓN", fg="white", bg="#191919", font=title_font).pack(pady=(10, 10))

    # --- Campos de usuario y contraseña ---
    tk.Label(root_login, text="USUARIO", fg="#FF0000", bg="#191919", font=label_font).pack(pady=(10, 5))
    username_entry = tk.Entry(root_login, font=("Consolas", 12), justify="center", bg="#2c2c2c", fg="white", insertbackground="white", relief="flat", width=30)
    username_entry.pack(pady=(0, 20))

    tk.Label(root_login, text="CONTRASEÑA", fg="#FF0000", bg="#191919", font=label_font).pack(pady=(10, 5))
    password_entry = tk.Entry(root_login, show="*", font=("Consolas", 12), justify="center", bg="#2c2c2c", fg="white", insertbackground="white", relief="flat", width=30)
    password_entry.pack(pady=(0, 0))

    tk.Button(
            root_login,
            text="INICIAR SESIÓN",
            command=lambda: [login_user(username_entry.get(), password_entry.get(), terminal, root_login)],
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
        ).pack(pady=(40, 0))
    
    tk.Button(
            root_login,
            text="ATRÁS",
            command=lambda: [root_login.destroy(), show_initial_window()],
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
        ).pack(pady=(20, 30))

    # --- Área tipo terminal ---
    terminal = tk.Text(root_login, width=70, bg="#0e0e0e", fg="#29FFF4",
                       insertbackground="white", font=("Consolas", 11), relief="flat")
    terminal.pack(pady=(0, 20))
    type_text(terminal, "Bienvenido a CryptoRacers\nIntroduzca su usuario y contraseña :)")

    root_login.mainloop()


def show_register_window():
    root_register = tk.Tk()
    root_register.title("Register CryptoRacers")
    root_register.resizable(False, False)

    # Tamaño y centrado
    width = 800
    height = 600
    screen_width = root_register.winfo_screenwidth()
    screen_height = root_register.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root_register.geometry(f"{width}x{height}+{x}+{y}")
    root_register.configure(bg="#191919")

    # --- Estilo general ---
    title_font = tkfont.Font(family="Impact", size=70, weight="bold")
    label_font = tkfont.Font(family="Consolas", size=17, weight="bold")
    button_font = tkfont.Font(family="Consolas", size=12, weight="bold")
    # --- Título estilo "CryptoRacers" ---
    tk.Label(root_register, text="REGISTRO", fg="white", bg="#191919", font=title_font).pack(pady=(10, 10))

    # --- Campos de usuario y contraseña ---
    tk.Label(root_register, text="USUARIO", fg="#FF0000", bg="#191919", font=label_font).pack(pady=(10, 5))
    username_entry = tk.Entry(root_register, font=("Consolas", 12), justify="center", bg="#2c2c2c", fg="white", insertbackground="white", relief="flat", width=30)
    username_entry.pack(pady=(0, 20))

    tk.Label(root_register, text="CONTRASEÑA", fg="#FF0000", bg="#191919", font=label_font).pack(pady=(10, 5))
    password_entry = tk.Entry(root_register, show="*", font=("Consolas", 12), justify="center", bg="#2c2c2c", fg="white", insertbackground="white", relief="flat", width=30)
    password_entry.pack(pady=(0, 0))

    tk.Button(
            root_register,
            text="REGISTRARSE",
            command=lambda: [register_user(username_entry.get(), password_entry.get(), terminal)],
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
        ).pack(pady=(40, 0))
    
    tk.Button(
            root_register,
            text="ATRÁS",
            command=lambda: [root_register.destroy(), show_initial_window()],
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
        ).pack(pady=(20, 30))

    # --- Área tipo terminal ---
    terminal = tk.Text(root_register, width=70, bg="#0e0e0e", fg="#29FFF4",
                       insertbackground="white", font=("Consolas", 11), relief="flat")
    terminal.pack(pady=(0, 20))
    type_text(terminal, "Bienvenido a CryptoRacers\nIntroduzca un usuario y una contraseña :)")

    root_register.mainloop()


### REGISTER AND LOGIN FUNCTIONS ###
def register_user(username: str, password: str, terminal):
    terminal.delete("1.0", tk.END)
    if password == "" or username == "":
        type_text(terminal, "Complete todos los campos por favor\n")
        return 
    
    if user_exists(username):
        type_text(terminal, "El usuario ya existe.\n")
        return
    
    '''    
    regex = re.compile(r'^(?=.{8,}$)(?=.*[A-Z])(?=.*\d)(?=.*[_-])\S+$')  
    if not regex.match(password):
        type_text(terminal, "Debe introducir una contraseña válida\nEsta debe contener al menos 1 mayúscula, 1 número, un símbolo (-, _) \ny tener una longitud mínima de 8")
        return 
    '''

    salt_b64, hash_b64 = hash_password(password)


    users_auth = load_data(USERS_FILE)
    users_auth[username] = {
        "salt": salt_b64,
        "hash": hash_b64
    }
    USER_DATA_PATH = f"User_data/{username}_data.json"
    user_data = load_data(USER_DATA_PATH)
    user_data["username"] = username
    user_data["garage"] = []
    user_data["points"] = 200

    
    store_data(users_auth, USERS_FILE)
    store_data(user_data, USER_DATA_PATH)

    type_text(terminal, (
    f"Salt {salt_b64} generado y aplicado...\n"
    "Aplicado pepper secreto...\n"
    f"Aplicando {DEFAULT_ITERATIONS} iteraciones...\n"
    f"Hash SHA-256 {hash_b64} generado\ncorrectamente...\n"
    "Datos registrados correctamente!\n"))


def login_user(username: str, password: str, terminal, root):
    terminal.delete("1.0", tk.END)
    if password == "" or username == "":
        type_text(terminal, "Complete todos los campos por favor\n")
        return 
    
    if not user_exists(username):
        type_text(terminal, "Usuario no encontrado.\nIntroduzca uno que esté registrado\n")
        return

    users = load_data(USERS_FILE)
    user_data = users[username]
    salt_b64 = user_data["salt"]
    stored_hash = user_data["hash"]
    salt = base64.b64decode(salt_b64)

    _, computed_hash = hash_password(password, salt)

    if computed_hash == stored_hash:
        USER_DATA_PATH = f"User_data/{username}_data.json"
        root.destroy()
        show_secondary_menu(USER_DATA_PATH, username)
        return
    else:
        type_text(terminal, "Contraseña incorrecta.\nInténtelo de nuevo :(\n")
        return


### AUXILIARY FUNCTIONS ###
def user_exists(username: str) -> bool:
    users = load_data(USERS_FILE)
    return username in users

def hash_password(password: str, salt: bytes = None) -> tuple:
    if salt is None:
        salt = os.urandom(16)

    password_peppered = (password + PEPPER).encode("utf-8")
    
    value = salt + password_peppered

    for _ in range(DEFAULT_ITERATIONS):
        value = hashlib.sha256(value).digest()

    return (
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(value).decode("ascii")
    )
