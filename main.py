import time
import tkinter as tk
from tkinter import messagebox, font

# Funciones de tu app
def ejecutar_test(coste):
    # Aquí iría tu lógica real, por ahora simulamos
    resultado = f"Coste seleccionado: {coste}\nResultado del test: OK"
    text_resultado.config(state='normal')
    text_resultado.delete(1.0, tk.END)
    text_resultado.insert(tk.END, resultado)
    text_resultado.config(state='disabled')

def salir():
    root.destroy()

# Ventana principal
root = tk.Tk()
root.title("CryptoRacers - Initial D Style")
root.geometry("700x500")  # Ventana más grande
root.configure(bg="#1a1a1a")  # Fondo oscuro
root.resizable(False, False)

# Fuente estilo arcade
fuente_titulo = font.Font(family="Courier", size=28, weight="bold")
fuente_botones = font.Font(family="Courier", size=14, weight="bold")
fuente_texto = font.Font(family="Courier", size=12)

# Título
label_titulo = tk.Label(root, text="CRYPTO RACERS", font=fuente_titulo, fg="#ffcc00", bg="#1a1a1a")
label_titulo.pack(pady=20)

# Botones de costes
frame_botones = tk.Frame(root, bg="#1a1a1a")
frame_botones.pack(pady=10)

btn_barato = tk.Button(frame_botones, text="Barato", command=lambda: ejecutar_test(100), bg="#00ff00", fg="#000", font=fuente_botones, width=10)
btn_barato.grid(row=0, column=0, padx=10)

btn_medio = tk.Button(frame_botones, text="Medio", command=lambda: ejecutar_test(200), bg="#ffff00", fg="#000", font=fuente_botones, width=10)
btn_medio.grid(row=0, column=1, padx=10)

btn_caro = tk.Button(frame_botones, text="Caro", command=lambda: ejecutar_test(400), bg="#ff3300", fg="#fff", font=fuente_botones, width=10)
btn_caro.grid(row=0, column=2, padx=10)

# Caja de resultados
text_resultado = tk.Text(root, height=15, width=70, state='disabled', bg="#111", fg="#00ffcc", font=fuente_texto)
text_resultado.pack(pady=20)

# Botón salir
btn_salir = tk.Button(root, text="SALIR", command=salir, bg="#ff0000", fg="#fff", font=fuente_botones, width=20)
btn_salir.pack(pady=10)


# Iniciar GUI
root.mainloop()
