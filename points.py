from utility_functions import load_encrypted_data, type_text
import tkinter as tk
from utility_functions import load_data, type_text

def type_points(user_path:str, terminal, user_key):
    user_data = load_encrypted_data(user_path, user_key, terminal)
    terminal.delete("1.0", tk.END)
    type_text(terminal, f"Actualmente tienes un total de {user_data["points"]} puntos")

    