#garage.py
from utility_functions import load_encrypted_data, type_text
import tkinter as tk


selected_garage_car = 0

def type_garage_car(user_path:str, terminal, user_key):
    global selected_garage_car
    terminal.delete("1.0", tk.END)
    #Cargamos los coches del usuario (los desencriptamos)
    user_data = load_encrypted_data(user_path, user_key, terminal)
    if not user_data:
        return
    
    #Comprobaciones necesarias para que no haya errores de índice
    if len(user_data["garage"]) == 0:
        type_text(terminal, "Actualmente no tienes coches\n")
        return

    if selected_garage_car == len(user_data["garage"]):
        selected_garage_car = 0
    
    if selected_garage_car < 0:
        selected_garage_car = len(user_data["garage"]) - 1

    #Generación cadena texto de las mejoras (ya que solo queremos que aprarezcan los nombres de las mejoras)
    if user_data["garage"][selected_garage_car]["upgrades"]:
        upgrades_text = ""
        for u in user_data["garage"][selected_garage_car]["upgrades"]:
            upgrades_text += f"    - {u["name"]}"
    else:
        upgrades_text = "    (Sin mejoras)"

    #Se muestra el coche en pantalla
    type_text(terminal, 
    f"""
    --- {user_data["garage"][selected_garage_car]["brand"]} {user_data["garage"][selected_garage_car]["model"]} ---
    Velocidad: {user_data["garage"][selected_garage_car]["stats"]["speed"]}
    Manejo: {user_data["garage"][selected_garage_car]["stats"]["handling"]}
    Aceleración: {user_data["garage"][selected_garage_car]["stats"]["acceleration"]}
    Frenada: {user_data["garage"][selected_garage_car]["stats"]["braking"]}
    Mejoras: {upgrades_text}""")

def next_garage_car(user_path:str, terminal, user_key):
    #Avanzamos en la lista
    global selected_garage_car
    selected_garage_car +=1
    type_garage_car(user_path, terminal, user_key)

def previous_garage_car(user_path:str, terminal, user_key):
    #Retrocedemos en la lista
    global selected_garage_car
    selected_garage_car -=1
    type_garage_car(user_path, terminal, user_key)    