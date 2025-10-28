#points.py
from utility_functions import load_encrypted_data, type_text
from utility_functions import type_text

def type_points(user_path:str, terminal, user_key):
    # Accedemos a los datos del usuario (hay que desencriptarlos)
    user_data = load_encrypted_data(user_path, user_key, terminal)
    if not user_data:
        return
    type_text(terminal, f"->Actualmente tienes un total de {user_data["points"]} puntos<-")

    