import requests
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_precios_luz():
    print("⚡ Consultando Precios de Energía (REE)...")
    
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    # Endpoint de ESIOS para el PVPC (Indicador 1001)
    url = f"https://api.esios.ree.es/archives/70/download_json?locale=es&date={fecha_hoy}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"⚠️ No se pudieron obtener datos de energía para hoy ({response.status_code})")
            return

        datos = response.json()
        registros = []
        
        # Extraemos los precios horarios
        # Nota: REE devuelve los datos en un formato específico dentro de 'PVPC'
        for hora_dato in datos['PVPC']:
            # El precio viene en €/MWh, lo pasamos a €/kWh dividiendo por 1000
            precio_mwh = float(hora_dato['PCB'].replace(',', '.'))
            precio_kwh = precio_mwh / 1000
            
            # La hora viene en formato "00-01", tomamos el primer número
            hora_int = int(hora_dato['Dia'].split('-')[0]) if '-' in hora_dato['Dia'] else 0
            
            registros.append({
                "fecha": fecha_hoy,
                "hora": hora_int,
                "precio_kwh": round(precio_kwh, 5)
            })

        if registros:
            supabase.table("datos_energia").upsert(registros).execute()
            print(f"✅ ¡Éxito! {len(registros)} registros horarios de energía guardados.")

    except Exception as e:
        print(f"❌ Error en el monitor de energía: {e}")

if __name__ == "__main__":
    obtener_precios_luz()
