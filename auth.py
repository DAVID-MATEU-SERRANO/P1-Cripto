# auth.py
import os
import json
import hashlib
import base64
import hmac
import tempfile
import tkinter as tk

USERS_FILE = "Passwords/users.json"
PEPPER = os.environ.get("APP_PEPPER", "DefaultPracticePepper_ChangeMe!")

#### Mostrar ventanas de inicio sesion y registro de usuario ####

def show_login_window():
    root_login = tk.Tk()
    root_login.title("Login CryptoRacers")
    root_login.geometry("500x400")

    tk.Label(root_login, text="Usuario").pack()
    username_entry = tk.Entry(root_login)
    username_entry.pack()

    tk.Label(root_login, text="Contraseña").pack()
    password_entry = tk.Entry(root_login, show="*")
    password_entry.pack()

    tk.Button(root_login, text="Login", command=lambda: login_user(username_entry.get(), password_entry.get())).pack()
    tk.Button(root_login, text="Registrarse", command=lambda: register_user(username_entry.get(), password_entry.get())).pack()

    # Área de terminal
    terminal = tk.Text(root_login, height=10, width=60)
    terminal.pack()
    terminal.insert(tk.END, "Bienvenido a CryptoRacers\n")

    root_login.mainloop()





def save_user(username: str, salt_b64: str, hash: str, iterations: int):
    """Guarda o actualiza un usuario en users.json de forma atómica."""
    data = {username: {
        "salt": salt_b64,
        "iterations": iterations,
        "hash": hash} }
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Datos guardados en {USERS_FILE}")
    except Exception as e:
        print(f"Error guardando archivo: {e}")



'''
# ---------------------------
# Hashing con SHA-256 + salt + pepper + iteraciones
# ---------------------------
def _sha256_iterated(password: bytes, salt: bytes, iterations: int) -> bytes:
    """
    Devuelve el resultado de aplicar SHA-256 iterado.
    value inicial = salt || (password + pepper)
    Se retorna el digest binario final.
    """
    value = salt + password
    for _ in range(iterations):
        value = hashlib.sha256(value).digest()
    return value

def hash_password_raw(password: str, salt: bytes = None, iterations: int = DEFAULT_ITERATIONS):
    """
    Devuelve (salt_b64, hash_b64, iterations).
    salt: generará uno nuevo de 16 bytes si salt es None.
    """
    if salt is None:
        salt = os.urandom(16)

    # Concatena password + pepper (pepper NO se guarda)
    password_peppered = (password + PEPPER).encode("utf-8")
    digest = _sha256_iterated(password_peppered, salt, iterations)

    return base64.b64encode(salt).decode("ascii"), base64.b64encode(digest).decode("ascii"), iterations



def authenticate_user(username: str, password: str) -> bool:
    """
    Verifica credenciales. Devuelve True si coinciden, False en caso contrario.
    Usa comparación en tiempo constante para evitar leaks por temporización.
    """
    users = load_users()
    if username not in users:
        return False

    entry = users[username]
    try:
        salt = base64.b64decode(entry["salt"])
        iterations = int(entry.get("iterations", DEFAULT_ITERATIONS))
        stored_hash = base64.b64decode(entry["hash"])
    except Exception:
        return False

    password_peppered = (password + PEPPER).encode("utf-8")
    computed = _sha256_iterated(password_peppered, salt, iterations)

    # Comparación en tiempo constante
    return hmac.compare_digest(computed, stored_hash)

# ---------------------------
# Helpers para uso desde UI
# ---------------------------
def user_exists(username: str) -> bool:
    users = load_users()
    return username in users

def change_pepper_demo(new_pepper: str):
    """
    Útil solo para pruebas: permite cambiar el pepper (no recomendado en producción).
    No re-hashea contraseñas: si cambias pepper, las contraseñas existentes dejarán de validar.
    """
    global PEPPER
    PEPPER = new_pepper
'''