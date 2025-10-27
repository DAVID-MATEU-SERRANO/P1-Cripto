from time import sleep
from utility_functions import load_encrypted_data, store_encrypted_data, type_text
import tkinter as tk
from utility_functions import load_data, store_data, type_text

### Variables globales
selected_car = 0
selected_upgrade = 0

### Funciones auxiliares compra coche
def type_car(car_data:list, terminal):
    global selected_car
    type_text(terminal, 
    f"""
    --- {car_data[selected_car]["brand"]} {car_data[selected_car]["model"]} ---
    Velocidad: {car_data[selected_car]["stats"]["speed"]}
    Manejo: {car_data[selected_car]["stats"]["handling"]}
    Aceleración: {car_data[selected_car]["stats"]["acceleration"]}
    Frenada: {car_data[selected_car]["stats"]["braking"]}

    Precio: {car_data[selected_car]["cost"]} puntos""")

def next_car(car_data:list, terminal):
    global selected_car
    selected_car +=1
    if selected_car == len(car_data):
        selected_car = 0
    type_car(car_data, terminal)

def previous_car(car_data:list, terminal):
    global selected_car
    selected_car -=1
    if selected_car < 0:
        selected_car = len(car_data) - 1
    type_car(car_data, terminal)

def car_exists(model:str, user_data:dict):
    for car in user_data["garage"]:
        if car["model"] == model:
            return True
    return False
    
def buy_car(car_data:list, user_path:str, terminal, user_key):
    global selected_car
    print(user_path)
    user_data = load_encrypted_data(user_path, user_key, terminal)
    if not user_data:
        type_text(terminal, "ERROR GRAVE: tus datos han sido modificados desde la última vez que se encriptaron 💀")
        return
    if car_exists(car_data[selected_car]["model"], user_data):
        type_text(terminal, "Ya has comprado este coche.\nElige otro\n")
        return
    if car_data[selected_car]["cost"] <= user_data["points"]:
        user_data["garage"].append(car_data[selected_car])
        user_data["points"] -= car_data[selected_car]["cost"]
        store_encrypted_data(user_data, user_path, user_key, terminal)
        type_text(terminal, f"{car_data[selected_car]["brand"]} {car_data[selected_car]["model"]} añadido a tu garaje\n")
    else:
        type_text(terminal, f"No tienes suficientes puntos para comprar este coche\nTe faltan {car_data[selected_car]["cost"] - user_data["points"]} puntos\n.")

### Funciones auxiliares compra mejoras
def type_upgrade(upgrade_data:list, terminal):
    global selected_upgrade
    type_text(terminal, 
    f"""
    --- {upgrade_data[selected_upgrade]["name"]} ---
    Velocidad: {upgrade_data[selected_upgrade]["effects"]["speed"]}
    Manejo: {upgrade_data[selected_upgrade]["effects"]["handling"]}
    Aceleración: {upgrade_data[selected_upgrade]["effects"]["acceleration"]}
    Frenada: {upgrade_data[selected_upgrade]["effects"]["braking"]}

    Precio: {upgrade_data[selected_upgrade]["cost"]} puntos""")

def next_upgrade(upgrade_data:list, terminal):
    global selected_upgrade
    selected_upgrade +=1
    if selected_upgrade == len(upgrade_data):
        selected_upgrade = 0
    type_upgrade(upgrade_data, terminal)

def previous_upgrade(upgrade_data:list, terminal):
    global selected_upgrade
    selected_upgrade -=1
    if selected_upgrade < 0:
        selected_upgrade = len(upgrade_data) - 1
    type_upgrade(upgrade_data, terminal)

def upgrade_exists(upgrade:str, user_data:dict, car_selected:str):
    car_pos = 0
    for car in user_data["garage"]:
        if car["model"] == car_selected:
            for up in car["upgrades"]:
                if up["name"] == upgrade:
                    return True
        else:
            car_pos += 1
    return False, car_pos
    
def buy_upgrade(upgrade_data:list, terminal, user_path:str, car_selected:str, user_key):
    global selected_upgrade
    user_data = load_encrypted_data(user_path, user_key, terminal)
    if not user_data:
        type_text(terminal, "ERROR GRAVE: tus datos han sido modificados desde la última vez que se encriptaron 💀")
        return
    if car_selected == "":
        type_text(terminal, "Indique el coche al que quiere instalar la mejora\n")
        return
    if not car_exists(car_selected, user_data):
        type_text(terminal, "No tienes este coche en tu garaje\n")
        return

    upgrade, car_pos = upgrade_exists(upgrade_data[selected_upgrade]["name"], user_data, car_selected)
    if upgrade:
        type_text(terminal, f"Tu {car_selected} ya cuenta con {upgrade_data[selected_upgrade]["name"]}\n")
        return
    if upgrade_data[selected_upgrade]["cost"] <= user_data["points"]:
        user_data["garage"][car_pos]["upgrades"].append(upgrade_data[selected_upgrade])
        user_data["points"] -= upgrade_data[selected_upgrade]["cost"]

        user_data["garage"][car_pos]["stats"]["speed"] += upgrade_data[selected_upgrade]["effects"]["speed"]
        user_data["garage"][car_pos]["stats"]["handling"] += upgrade_data[selected_upgrade]["effects"]["handling"]
        user_data["garage"][car_pos]["stats"]["acceleration"] += upgrade_data[selected_upgrade]["effects"]["acceleration"]
        user_data["garage"][car_pos]["stats"]["braking"] += upgrade_data[selected_upgrade]["effects"]["braking"]

        store_encrypted_data(user_data, user_path, user_key, terminal) 
        type_text(terminal, f"{upgrade_data[selected_upgrade]["name"]} añadido a tu {user_data["garage"][car_pos]["brand"]} {user_data["garage"][car_pos]["model"]}\n")
       
    else:
        type_text(terminal, f"No tienes suficientes puntos para comprar este coche\nTe faltan {upgrade_data[selected_upgrade]["cost"] - user_data["points"]} puntos\n.")

