import random
from const import RACES_PATH, USERS_PATH
from shop import car_exists
from utility_functions import load_encrypted_data, store_encrypted_data, type_text, user_exists
import tkinter as tk
from utility_functions import load_data, store_data, type_text

selected_race = 0

def create_race(rival, race_car_data, user_name, terminal):
    path = RACES_PATH + f"{rival}" + "_races.json" 
    race_data = load_data(path)
    if race_data == {}:
        race_data = []
    race = {
        "rival":user_name,
        "race_car":race_car_data
    }
    race_data.append(race)
    store_data(race_data, path)
    type_text(terminal, "Carrera enviada correctamente\n")


def send_race(rival:str, race_car:str, user_name:str, terminal, user_path, user_key):
    if rival == "" or race_car == "":
        type_text(terminal, "Complete todos los campos por favor\n")
        return 

    if rival == user_name:
        type_text(terminal, "No puedes hacer una carrera contra ti mismo\nIntroduzca uno válido\n")
        return
    if not user_exists(rival, USERS_PATH):
        type_text(terminal, "Username no encontrado\nIntroduzca uno válido\n")
        return
    
    user_data = load_encrypted_data(user_path, user_key, terminal)
    car, car_pos = car_exists(race_car, user_data)
    if not car:
        type_text(terminal, "No tienes este coche\nConsulta tu garage y elige uno\n")
        return
    create_race(rival, user_data["garage"][car_pos], user_name, terminal)


def type_race(user_name, terminal, user_key):
    global selected_race
    race_path = RACES_PATH + f"{user_name}" + "_races.json" 

    race_data = load_data(race_path)
    if race_data == {}:
        type_text(terminal, "Vaya, nadie te ha desafiado aún\n")
        return

    if selected_race == len(race_data):
        selected_race = 0
    
    if selected_race < 0:
        selected_race = len(race_data) - 1


    if race_data[selected_race]["race_car"]["upgrades"]:
        upgrades_text = ""
        for u in race_data[selected_race]["race_car"]["upgrades"]:
            upgrades_text += f"    - {u["name"]}"
    else:
        upgrades_text = "    (Sin mejoras)"

    type_text(terminal, 
    f"""
    --- {race_data[selected_race]["race_car"]["brand"]} {race_data[selected_race]["race_car"]["model"]} de {race_data[selected_race]["rival"]} ---
    Velocidad: {race_data[selected_race]["race_car"]["stats"]["speed"]}
    Manejo: {race_data[selected_race]["race_car"]["stats"]["handling"]}
    Aceleración: {race_data[selected_race]["race_car"]["stats"]["acceleration"]}
    Frenada: {race_data[selected_race]["race_car"]["stats"]["braking"]}
    Mejoras: {upgrades_text}""")

def next_race(user_name:str, terminal, user_key):
    global selected_race
    selected_race +=1
    type_race(user_name, terminal, user_key)

def previous_race(user_name:str, terminal, user_key):
    global selected_race
    selected_race -=1
    type_race(user_name, terminal, user_key)    

def race(user_name, user_path, user_key, terminal, selected_race_car):
    global selected_race
    race_path = RACES_PATH + f"{user_name}" + "_races.json" 
    race_data = load_data(race_path)

    oponent_race_car = race_data[selected_race]["race_car"]

    user_data = load_encrypted_data(user_path, user_key, terminal)
    car, car_pos = car_exists(selected_race_car, user_data)
    if not car:
        type_text(terminal, "No tienes este coche\nConsulta tu garage y elige uno\n")
        return

    user_race_car = user_data["garage"][car_pos]
    oponnent_score = oponent_race_car["stats"]["speed"] +  oponent_race_car["stats"]["handling"] +  oponent_race_car["stats"]["acceleration"] +  oponent_race_car["stats"]["braking"]
    user_score = user_race_car["stats"]["speed"] +  user_race_car["stats"]["handling"] +  user_race_car["stats"]["acceleration"] +  user_race_car["stats"]["braking"]
    adelantamiento = random.randint(1, 10)
    type_text(terminal, "3                        \n")
    type_text(terminal, "2                        \n")
    type_text(terminal, "1                        \n")
    type_text(terminal, "YA!                        \n")  
    race_msg = ""
    if oponnent_score > user_score:
        race_msg += f"El {oponent_race_car["brand"]} {oponent_race_car["model"]} de {race_data[selected_race]["rival"]} toma la delantera!!\n"
        if adelantamiento > 7:
            race_msg += f"Increíble, el {oponent_race_car["brand"]} {oponent_race_car["model"]} de {race_data[selected_race]["rival"]} se ha salido en una curva y el {user_race_car["brand"]} {user_race_car["model"]} de {user_name} toma la delantera!!\n"
            winer_car = user_race_car
            winner = user_name
        else:
            winer_car = oponent_race_car
            winner = race_data[selected_race]["rival"]

    elif oponnent_score < user_score:
        race_msg += f"El {user_race_car["brand"]} {user_race_car["model"]} de {user_name} toma la delantera!!\n"
        if adelantamiento > 7:
            race_msg +=  f"Increíble, el {user_race_car["brand"]} {user_race_car["model"]} de {user_name} se ha salido en una curva y el {oponent_race_car["brand"]} {oponent_race_car["model"]} de {race_data[selected_race]["rival"]} toma la delantera!!\n"
            winer_car = oponent_race_car
            winner = race_data[selected_race]["rival"]

        else:
            winer_car = user_race_car
            winner = user_name
    else:
        race_msg += f"Ambos coches se mantienen par a par!!\n"
        if adelantamiento > 5:
            race_msg += f"Increíble, el {oponent_race_car["brand"]} {oponent_race_car["model"]} de {race_data[selected_race]["rival"]} se ha salido en una curva y el {user_race_car["brand"]} {user_race_car["model"]} de {user_name} toma la delantera!!\n"
            winer_car = user_race_car
            winner = user_name
        else:
            race_msg += f"Increíble, el {user_race_car["brand"]} {user_race_car["model"]} de {user_name} se ha salido en una curva y el {oponent_race_car["brand"]} {oponent_race_car["model"]} de {race_data[selected_race]["rival"]} toma la delantera!!\n"
            winer_car = oponent_race_car
            winner = race_data[selected_race]["rival"]

    if winner == user_name:
        race_msg += f"Enhorabuena tu {winer_car["brand"]} {winer_car["model"]} ha saido victorioso🏆\nSe te sumarán 200 puntos                         \n"
        user_data["points"] += 200

    else:
        race_msg += f"Vaya, parece que tu Enhorabuena tu {winer_car["brand"]} {winer_car["model"]} ha perdido👎\nSe te restarán 200 puntos                         \n"
        user_data["points"] -= 200

    type_text(terminal, race_msg)
    store_encrypted_data(user_data, user_path, user_key, terminal)


            

    



