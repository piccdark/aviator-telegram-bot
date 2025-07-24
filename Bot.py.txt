import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

# --- CONFIGURA ESTOS DATOS ---
TELEGRAM_BOT_TOKEN = "TU_TOKEN_DEL_BOT"
TELEGRAM_CHAT_ID = "TU_CHAT_ID"
SPREADSHEET_NAME = "Predicciones aviator BOT"
HOJA = "Hoja 1"
# ------------------------------

def enviar_mensaje_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje
    }
    requests.post(url, data=data)

def leer_datos_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).worksheet(HOJA)
    datos = sheet.get_all_values()
    return datos[-1]  # Última fila

def main():
    while True:
        try:
            fila = leer_datos_google_sheets()
            hora, salida_segura, salida_riesgo, probabilidad, riesgo, confianza, mensaje_final = fila

            mensaje = ""
            if float(probabilidad) >= 80:
                mensaje = f"✅ Entrada recomendada\n🕒 Hora: {hora}\n📈 Probabilidad: {probabilidad}%\n🔒 Confianza: {confianza}\n💬 {mensaje_final}"
            else:
                mensaje = f"🚫 No recomendado\n🕒 Hora: {hora}\n📉 Probabilidad: {probabilidad}%\n🔓 Riesgo: {riesgo}\n💬 {mensaje_final}"

            enviar_mensaje_telegram(mensaje)

        except Exception as e:
            print("Error:", e)

        time.sleep(180)  # Espera 3 minutos

if __name__ == "__main__":
    main()
