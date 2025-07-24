import time
import requests
import os
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Simula una predicción de probabilidad
def obtener_probabilidad():
    # En el futuro este valor puede venir desde una hoja de cálculo o scraping del juego
    return round(random.uniform(60, 100), 2)

# Envía mensaje a Telegram
def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto
    }
    requests.post(url, data=payload)

def iniciar_bot():
    enviar_mensaje("🤖 Bot Aviator iniciado.")
    while True:
        probabilidad = obtener_probabilidad()
        print(f"Probabilidad actual: {probabilidad}%")

        if probabilidad >= 80:
            mensaje = f"✅ Alta probabilidad ({probabilidad}%). ¡ENTRAR AHORA en Aviator!"
        else:
            mensaje = f"⚠️ Probabilidad baja ({probabilidad}%). NO se recomienda entrar."

        enviar_mensaje(mensaje)
        
        # Espera entre 3 y 4 minutos antes de repetir
        tiempo_espera = random.randint(180, 240)
        time.sleep(tiempo_espera)

if __name__ == "__main__":
    iniciar_bot()
