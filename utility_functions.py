import json
import tkinter as tk

def load_data(path: str) -> dict:
    """Carga y devuelve el diccionario de usuarios desde users.json."""
    try:
        with open(path, "r", encoding="utf-8", newline="") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}
    except json.JSONDecodeError:
        raise Exception("Error leyendo el archivo\n")
    return users

def store_data(data: dict, path: str):
    """Guarda el diccionario de usuarios en users.json de forma atómica."""
    existing_data = load_data(path)
    existing_data.update(data)
    try:
        with open(path, "w", encoding="utf-8", newline="") as file:
                json.dump(existing_data, file, indent=2)
    except json.JSONDecodeError:
        raise Exception("Error guardando el archivo\n")

def type_text(terminal, text, index=0, delay=10):
    if index < len(text):
        terminal.insert(tk.END, text[index])
        terminal.see(tk.END) 
        terminal.after(delay, type_text, terminal, text, index + 1, delay)
    else:
        terminal.insert(tk.END, "\n")
