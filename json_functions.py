import json
def load_data(path: str) -> dict:
    """Carga y devuelve el diccionario de usuarios desde users.json."""
    try:
        with open(path, 'r', encoding='utf-8') as file:
            users = json.load(file)
        return users
    except FileNotFoundError:
        return {}
        
def store_data(data: dict, path: str):
    """Guarda el diccionario de usuarios en users.json de forma atómica."""
    store_data = load_data(path)
    store_data.update(data)
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(store_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando archivo: {e}")
