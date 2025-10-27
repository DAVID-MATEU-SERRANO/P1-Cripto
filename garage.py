from utility_functions import load_data, load_encrypted_data, type_text
import tkinter as tk


selected_garage_car = 0

def type_garage_car(user_path:str, terminal, user_key):
    global selected_garage_car
    user_data = load_encrypted_data(user_path, user_key, terminal)
    if not user_data:
        type_text(terminal, "ERROR GRAVE: tus datos han sido modificados desde la última vez que se encriptaron 💀")
        return

    if selected_garage_car == len(user_data["garage"]):
        selected_garage_car = 0
    
    if selected_garage_car < 0:
        selected_garage_car = len(user_data["garage"]) - 1


    if user_data["garage"][selected_garage_car]["upgrades"]:
        upgrades_text = ""
        for u in user_data["garage"][selected_garage_car]["upgrades"]:
            upgrades_text += f"    - {u["name"]}"
    else:
        upgrades_text = "    (Sin mejoras)"

    type_text(terminal, 
    f"""
    --- {user_data["garage"][selected_garage_car]["brand"]} {user_data["garage"][selected_garage_car]["model"]} ---
    Velocidad: {user_data["garage"][selected_garage_car]["stats"]["speed"]}
    Manejo: {user_data["garage"][selected_garage_car]["stats"]["handling"]}
    Aceleración: {user_data["garage"][selected_garage_car]["stats"]["acceleration"]}
    Frenada: {user_data["garage"][selected_garage_car]["stats"]["braking"]}
    Mejoras: {upgrades_text}""")

def next_garage_car(user_path:str, terminal, user_key):
    global selected_garage_car
    selected_garage_car +=1
    type_garage_car(user_path, terminal, user_key)

def previous_garage_car(user_path:str, terminal, user_key):
    global selected_garage_car
    selected_garage_car -=1
    type_garage_car(user_path, terminal, user_key)    