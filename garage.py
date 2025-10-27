from utility_functions import load_data, type_text
import tkinter as tk


selected_garage_car = 0

def type_garage_car(user_path:str, terminal):
    global selected_garage_car
    user_data = load_data(user_path)
    terminal.delete("1.0", tk.END)

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

def next_garage_car(user_path:str, terminal):
    global selected_garage_car
    selected_garage_car +=1
    type_garage_car(user_path, terminal)

def previous_garage_car(user_path:str, terminal):
    global selected_garage_car
    selected_garage_car -=1
    type_garage_car(user_path, terminal)    