import tkinter as tk
from tkinter import messagebox, font

# ------------------------------
# Funciones
# ------------------------------
def login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if usuario == "admin" and contraseña == "123":  # Ejemplo simple
        messagebox.showinfo("Login", "¡Login correcto!")
        ventana_login.destroy()
        mostrar_ventana_principal()
    else:
        messagebox.showerror("Login", "Usuario o contraseña incorrectos")

def mostrar_ventana_principal():
    root = tk.Tk()
    root.title("CryptoRacers - Initial D")
    root.geometry("700x500")
    root.configure(bg="#1a1a1a")

    fuente_titulo = font.Font(family="Courier", size=28, weight="bold")
    fuente_botones = font.Font(family="Courier", size=14, weight="bold")
    fuente_texto = font.Font(family="Courier", size=12)

    label_titulo = tk.Label(root, text="CRYPTO RACERS", font=fuente_titulo, fg="#ffcc00", bg="#1a1a1a")
    label_titulo.pack(pady=20)

    # Aquí podrías poner los botones de costes y la "terminal" interna
    # Solo un ejemplo de botón
    btn_cerrar = tk.Button(root, text="Salir", command=root.destroy, bg="#ff0000", fg="#fff", font=fuente_botones)
    btn_cerrar.pack(pady=20)

    root.mainloop()


# ------------------------------
# Ventana de login
# ------------------------------
ventana_login = tk.Tk()
ventana_login.title("Login CryptoRacers")
ventana_login.geometry("400x300")
ventana_login.configure(bg="#1a1a1a")
ventana_login.resizable(False, False)

fuente_label = font.Font(family="Courier", size=12, weight="bold")
fuente_entry = font.Font(family="Courier", size=12)

# Etiquetas y entradas
tk.Label(ventana_login, text="Usuario:", font=fuente_label, fg="#00ffcc", bg="#1a1a1a").pack(pady=10)
entry_usuario = tk.Entry(ventana_login, font=fuente_entry)
entry_usuario.pack(pady=5)

tk.Label(ventana_login, text="Contraseña:", font=fuente_label, fg="#00ffcc", bg="#1a1a1a").pack(pady=10)
entry_contraseña = tk.Entry(ventana_login, font=fuente_entry, show="*")
entry_contraseña.pack(pady=5)

# Botón login
tk.Button(ventana_login, text="Login", command=login, bg="#4CAF50", fg="white", font=fuente_label).pack(pady=20)

ventana_login.mainloop()
