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
    url = f"https://api.esios.ree.es/archives/70/download_json?locale=es&date={fecha_hoy}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return

        datos = response.json()
        # Usamos un diccionario para asegurar UN SOLO registro por hora
        registros_dict = {}
        
        for hora_dato in datos['PVPC']:
            precio_mwh = float(hora_dato['PCB'].replace(',', '.'))
            precio_kwh = precio_mwh / 1000
            hora_int = int(hora_dato['Dia'].split('-')[0]) if '-' in hora_dato['Dia'] else 0
            
            # Esto sobrescribe cualquier duplicado antes de ir a la DB
            registros_dict[hora_int] = {
                "fecha": fecha_hoy,
                "hora": hora_int,
                "precio_kwh": round(precio_kwh, 5)
            }

        if registros_dict:
            registros = list(registros_dict.values())
            supabase.table("datos_energia").upsert(
                registros, 
                on_conflict="fecha, hora"
            ).execute()
            print(f"✅ ¡Éxito! {len(registros)} precios horarios procesados.")

    except Exception as e:
        print(f"❌ Error en el monitor de energía: {e}")

if __name__ == "__main__":
    obtener_precios_luz()
