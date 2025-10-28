import json
import tkinter as tk
from Crypto.Cipher import AES
import base64
import hashlib
import os
from collections import deque

DEFAULT_ITERATIONS = 200_000
typing_after_id = None

typing_after_id = None
typing_queue = deque()

def generate_user_key(password: str, salt: bytes) -> bytes:
    value = salt + (password).encode("utf-8")
    for _ in range(DEFAULT_ITERATIONS):
        value = hashlib.sha256(value).digest()
    return value  # 32 bytes → clave AES-256


def load_encrypted_data(filepath: str, key: bytes, terminal) -> dict:
    try:
        with open(filepath, "rb") as f:
            file_bytes = f.read()

        nonce = file_bytes[:16]
        tag = file_bytes[16:32]
        ciphertext = file_bytes[32:]

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        type_text(terminal, 
                  "Desencriptando archivo del usuario...\n"
                  f"Nonce extraído: {base64.b64encode(nonce).decode('ascii')}\n"
                  f"Tag de autenticidad extraído: {base64.b64encode(tag).decode('ascii')}\n"
                  f"Verificación MAC exitosa\n"
                  f"Desencriptación con AES-256 GCM exitosa                         \n") #Los espacios son para q tarde un tiempo en saltar al siguient mensaje en cola
        return json.loads(plaintext.decode("utf-8"))
    
    except ValueError as e:
        type_text(terminal, "ERROR GRAVE: tus datos han sido modificados desde la última vez que se encriptaron 💀\n")
        return None
    

def store_encrypted_data(data: dict, filepath: str, key: bytes, terminal):
    plaintext = json.dumps(data).encode("utf-8")  # de dict → bytes
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    

    # Guardamos nonce + tag + ciphertext en binario
    with open(filepath, "wb") as f:
        f.write(cipher.nonce + tag + ciphertext)

    type_text(terminal, 
                  "Encriptando archivo del usuario...\n"
                  f"Usando nonce generado aleatoriamente -> {base64.b64encode(cipher.nonce).decode("ascii")}\n"
                  f"Usada clave para AES-GCM de 32 bytes... \n"
                  f"Generado tag de autenticacion {base64.b64encode(tag).decode("ascii")}\n"
                  f"Encriptación con AES-256 GCM exitosa\n"
                  "Datos del usuario guardados correctamente                         \n") #Los espacios son para q tarde un tiempo en saltar al siguient mensaje en cola

### Normales
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
    """
    Escribe el texto en el terminal letra a letra usando una cola.
    """
    global typing_after_id, typing_queue

    # Si estamos empezando un nuevo texto (index == 0)
    if index == 0:
        # Si ya hay un texto escribiéndose, añadimos a la cola y salimos
        if typing_after_id is not None:
            typing_queue.append(text)
            return
        else:
            # Si no hay texto en curso, limpiamos el terminal
            terminal.delete("1.0", tk.END)

    # Escribimos el texto
    if index < len(text):
        terminal.insert(tk.END, text[index])
        terminal.see(tk.END)
        typing_after_id = terminal.after(delay, type_text, terminal, text, index + 1, delay)
    else:
        # Terminamos este texto
        terminal.insert(tk.END, "\n")
        typing_after_id = None
        
        # Si hay mensajes en la cola, procesamos el siguiente
        if typing_queue:
            next_text = typing_queue.popleft()
            type_text(terminal, next_text, 0, delay)