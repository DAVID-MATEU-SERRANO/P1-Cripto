#shop.py
from utility_functions import car_exists, load_encrypted_data, store_encrypted_data, type_text, upgrade_exists
from utility_functions import type_text
import tkinter as tk
### Variables globales
selected_car = 0
selected_upgrade = 0

### Funciones auxiliares compra coche
# Imprimir el coche
def type_car(car_data:list, terminal):
    global selected_car
    terminal.delete("1.0", tk.END)
    type_text(terminal, 
    f"""
    --- {car_data[selected_car]["brand"]} {car_data[selected_car]["model"]} ---
    Velocidad: {car_data[selected_car]["stats"]["speed"]}
    Manejo: {car_data[selected_car]["stats"]["handling"]}
    Aceleración: {car_data[selected_car]["stats"]["acceleration"]}
    Frenada: {car_data[selected_car]["stats"]["braking"]}

    Precio: {car_data[selected_car]["cost"]} puntos""")

def next_car(car_data:list, terminal):
    #Avanzamos en la lista
    global selected_car
    selected_car +=1
    if selected_car == len(car_data):
        selected_car = 0
    type_car(car_data, terminal)

def previous_car(car_data:list, terminal):
    #Retrocedemos en la lista
    global selected_car
    selected_car -=1
    if selected_car < 0:
        selected_car = len(car_data) - 1
    type_car(car_data, terminal)

#Compra del coche
def buy_car(car_data:list, user_path:str, terminal, user_key):
    global selected_car
    terminal.delete("1.0", tk.END)
    # Tenemos que cargar los datos del usuario para las comprobaciones
    user_data = load_encrypted_data(user_path, user_key, terminal)
    if not user_data:
        return
    car, _ = car_exists(car_data[selected_car]["model"], user_data)
    # Nos aseguramos que el coche no esté ya comprado y que el usuario tenga suficientes puntos
    if car:
        type_text(terminal, "Ya has comprado este coche.\nElige otro\n")
        return
    if car_data[selected_car]["cost"] <= user_data["points"]:
        # Se añade el coche al garage
        user_data["garage"].append(car_data[selected_car])
        # Se restan los puntos
        user_data["points"] -= car_data[selected_car]["cost"]
        # Se encriptan otra vez todos los datos del usuario
        store_encrypted_data(user_data, user_path, user_key, terminal)
        type_text(terminal, f"{car_data[selected_car]["brand"]} {car_data[selected_car]["model"]} añadido a tu garaje\n")
    else:
        type_text(terminal, f"No tienes suficientes puntos para comprar este coche\nTe faltan {car_data[selected_car]["cost"] - user_data["points"]} puntos\n.")

### Funciones auxiliares compra mejoras
def type_upgrade(upgrade_data:list, terminal):
    global selected_upgrade
    terminal.delete("1.0", tk.END)
    type_text(terminal, 
    f"""
    --- {upgrade_data[selected_upgrade]["name"]} ---
    Velocidad: {upgrade_data[selected_upgrade]["effects"]["speed"]}
    Manejo: {upgrade_data[selected_upgrade]["effects"]["handling"]}
    Aceleración: {upgrade_data[selected_upgrade]["effects"]["acceleration"]}
    Frenada: {upgrade_data[selected_upgrade]["effects"]["braking"]}

    Precio: {upgrade_data[selected_upgrade]["cost"]} puntos""")

def next_upgrade(upgrade_data:list, terminal):
    #Avanzamos en la lista
    global selected_upgrade
    selected_upgrade +=1
    if selected_upgrade == len(upgrade_data):
        selected_upgrade = 0
    type_upgrade(upgrade_data, terminal)

def previous_upgrade(upgrade_data:list, terminal):
    #Retrocedemos en la lista
    global selected_upgrade
    selected_upgrade -=1
    if selected_upgrade < 0:
        selected_upgrade = len(upgrade_data) - 1
    type_upgrade(upgrade_data, terminal)
    
def buy_upgrade(upgrade_data:list, terminal, user_path:str, car_selected:str, user_key):
    global selected_upgrade
    terminal.delete("1.0", tk.END)
    # Hay que cargar los datos del usuario para comprobaciones y para actualizarlos en caso necesario
    user_data = load_encrypted_data(user_path, user_key, terminal)
    # Comprobaciones previas (el coche debe estar en el garage del usuario y no contener la mejora)
    if not user_data:
        return
    if car_selected == "":
        type_text(terminal, "Indique el coche al que quiere instalar la mejora\n")
        return
    car, car_pos = car_exists(car_selected, user_data)
    if not car:
        type_text(terminal, "No tienes este coche en tu garaje\n")
        return

    upgrade = upgrade_exists(upgrade_data[selected_upgrade]["name"], user_data, car_pos)
    if upgrade:
        type_text(terminal, f"Tu {car_selected} ya cuenta con {upgrade_data[selected_upgrade]["name"]}\n")
        return
    
    # Si tienes los suficientes puntos se añade al coche que elijas la mejora (se actualizan además todos los datos -> cifrar de nuevo)
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

