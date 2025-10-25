# auth.py
import os
import json
import hashlib
import base64
import tkinter as tk
from json_functions import load_data, store_data

DEFAULT_ITERATIONS = 200_000
USERS_FILE = "Passwords/users.json"
PEPPER = "practica_crypto_racers"

#### SHOW WINDOWS ####
def show_initial_window():
    root_initial = tk.Tk()
    root_initial.title("CryptoRacers")
    root_initial.geometry("800x600")

    tk.Label(root_initial, text="Bienvenido a CryptoRacers").pack(pady=10)
    tk.Button(root_initial, text="Iniciar Sesión", command=lambda: [root_initial.destroy(), show_login_window()]).pack(pady=5)
    tk.Button(root_initial, text="Registrarse", command=lambda: [root_initial.destroy(), show_register_window()]).pack(pady=5)

    root_initial.mainloop()

def show_login_window():
    root_login = tk.Tk()
    root_login.title("Login CryptoRacers")
    root_login.geometry("800x600")

    tk.Label(root_login, text="Usuario").pack()
    username_entry = tk.Entry(root_login)
    username_entry.pack()

    tk.Label(root_login, text="Contraseña").pack()
    password_entry = tk.Entry(root_login, show="*")
    password_entry.pack()

    # Área de terminal
    terminal = tk.Text(root_login, height=10, width=60)
    terminal.pack()
    terminal.insert(tk.END, "Bienvenido a CryptoRacers\n")

    tk.Button(root_login, text="Login",
              command=lambda: login_user(username_entry.get(), password_entry.get(), terminal)).pack()
    tk.Button(root_login, text="Atras", command=lambda: [root_login.destroy(), show_initial_window()]).pack()

    root_login.mainloop()


def show_register_window():
    root_register = tk.Tk()
    root_register.title("Registro CryptoRacers")
    root_register.geometry("800x600")

    tk.Label(root_register, text="Usuario").pack()
    username_entry = tk.Entry(root_register)
    username_entry.pack()

    tk.Label(root_register, text="Contraseña").pack()
    password_entry = tk.Entry(root_register, show="*")
    password_entry.pack()

    # Área de terminal
    terminal = tk.Text(root_register, height=10, width=60)
    terminal.pack()
    terminal.insert(tk.END, "Bienvenido a CryptoRacers\n")

    tk.Button(root_register, text="Registrarse",
              command=lambda: register_user(username_entry.get(), password_entry.get(), terminal)).pack()
    tk.Button(root_register, text="Atras", command=lambda: [root_register.destroy(), show_initial_window()]).pack()

    root_register.mainloop()


### REGISTER AND LOGIN FUNCTIONS ###
def register_user(username: str, password: str, terminal):
    if user_exists(username):
        terminal.insert(tk.END, "❌ El usuario ya existe.\n")
        return

    salt_b64, hash_b64 = hash_password(password)

    users = load_data(USERS_FILE)
    users[username] = {
        "salt": salt_b64,
        "hash": hash_b64
    }

    store_data(users, USERS_FILE)
    terminal.insert(tk.END, "✅ Usuario registrado correctamente.\n")


def login_user(username: str, password: str, terminal) -> bool:
    if not user_exists(username):
        terminal.insert(tk.END, "❌ Usuario no encontrado.\n")
        return False

    users = load_data(USERS_FILE)
    user_data = users[username]
    salt_b64 = user_data["salt"]
    stored_hash = user_data["hash"]

    salt = base64.b64decode(salt_b64)
    _, computed_hash = hash_password(password, salt)

    if computed_hash == stored_hash:
        terminal.insert(tk.END, "✅ Inicio de sesión exitoso.\n")
        return True
    else:
        terminal.insert(tk.END, "❌ Contraseña incorrecta.\n")
        return False


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
