import requests
import json
import pandas as pd
import os

# Credenciales de autenticación
access_token = "1000.d9a6ec9e7dddf9668be1f7bcac0812c7.ac72907364870253e5f11fb8ce70d307"
refresh_token = "1000.0b8233b62707b577fe16832434abc213.b66c40f4c700c262ce57fedb128d3f06"
client_id = "1000.9KLJEBGO230LA4N7PDKFH9G9G69WXH"
client_secret = "ccba688719aba106669ffd09fcfe1eb5ecd12e28c2"

# Refrescar token de acceso si ha expirado
def refresh_access_token():
    url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        global access_token
        access_token = response.json()['access_token']
        print("Access token actualizado correctamente.")
    else:
        print("Error al actualizar el access token:", response.status_code)
        print(response.text)

# Encabezados para la API
def get_headers():
    return {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

# Buscar por cédula en módulo específico
def buscar_en_modulo(modulo, campo, cedula):
    url = f"https://www.zohoapis.com/crm/v2/{modulo}/search?criteria=({campo}:equals:{cedula})"
    response = requests.get(url, headers=get_headers())

    if response.status_code == 401:
        refresh_access_token()
        response = requests.get(url, headers=get_headers())

    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            return data['data'][0]
    return None

# Procesar archivo CSV y buscar cédulas
def procesar_csv_y_buscar():
    resultados = []

    # Ruta a la carpeta de Descargas
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    archivo_salida = os.path.join(downloads_folder, "resultados_real.csv")

    try:
        df = pd.read_csv(r"C:\documentos\DATA.csv", encoding='utf-8')

        for _, row in df.iterrows():
            cedula = row['CC']
            print(f"🔎 Buscando Cédula: {cedula}")
            modulo_encontrado = ""
            owner_name = "No encontrado"
            owner_email = "No encontrado"
            periodo = "No disponible"
            gestor_name = "No disponible"

            resultado = buscar_en_modulo("Potentials", "N_mero_de_Documento_de_Identidad", cedula)

            if resultado:
                modulo_encontrado = "Potentials"
                owner_info = resultado.get('Owner', {})
                owner_name = owner_info.get('name', 'Desconocido')
                owner_email = owner_info.get('email', 'Desconocido')
                periodo = resultado.get('Periodo', 'No disponible')
                gestor = resultado.get('Gestor_Comercial')
                gestor_name = gestor.get('name', 'Desconocido') if gestor else 'Desconocido'
                print(f"✅ Encontrado - Owner: {owner_name}, Email: {owner_email}")
            else:
                print("❌ No se encontró ningún registro con esa cédula.")

            resultados.append({
                "cedula": cedula,
                "modulo": modulo_encontrado if modulo_encontrado else "No encontrado",
                "owner_name": owner_name,
                "owner_email": owner_email,
                "periodo": periodo,
                "gestor_name": gestor_name
            })

        resultados_df = pd.DataFrame(resultados)
        resultados_df.to_csv(archivo_salida, index=False, encoding='utf-8')

        print(f"📁 Resultados guardados en '{archivo_salida}'.")

    except FileNotFoundError:
        print("❌ El archivo 'DATA.csv' no fue encontrado.")

# Ejecutar
procesar_csv_y_buscar()

