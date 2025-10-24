# main.py
from auth import show_login_window
import getpass

#### VARIABLES DE CONFIGURACIÓN ####
# Autenticación usuarios
DEFAULT_ITERATIONS = 200_000

show_login_window()

import smtplib
from email.message import EmailMessage

def enviar_codigo(correo_destino, codigo):
    EMAIL_ADDRESS = ""  # correo remitente
    EMAIL_PASSWORD = "tu_contraseña_app"   # contraseña o app password

    msg = EmailMessage()
    msg['Subject'] = 'Código de verificación CryptoRacers'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = correo_destino
    msg.set_content(f'Tu código de verificación es: {codigo}')

    # Conexión SMTP con Gmail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

enviar_codigo("davidmateu333@gmail.com", "123456")
