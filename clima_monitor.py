import os
import requests
from supabase import create_client, Client
from datetime import datetime
import sys

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG" 
AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2OGJvcnJpc21hckBnbWFpbC5jb20iLCJqdGkiOiI1YzRjYzlkZC04OTI0LTQzZjgtOTI1OC1hZWZiZjRhOWIzNGMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc3MTA4MjI3MSwidXNlcklkIjoiNWM0Y2M5ZGQtODkyNC00M2Y4LTkyNTgtYWVmYmY0YTliMzRjIiwicm9sZSI6IiJ9.EQqSYmGFYaCQvhzPv2gxYHkwa1Zyqr9sDLRCG8xLaV4"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_clima_extremadura():
    print(f"=== Monitor de Clima Pro - {datetime.now().strftime('%d/%m/%Y %H:%M')} ===")
    
    ciudades = {
        "Badajoz": "4452", "Caceres": "3431", "Merida": "4410",
        "Plasencia": "3519", "Don Benito": "4358", "Almendralejo": "4446",
        "Zafra": "4427", "Navalmoral de la Mata": "3411", "Trujillo": "3441", "Hervas": "3469"
    }
    
    datos_procesados = {}
    headers = {'api_key': AEMET_API_KEY}
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    for ciudad, id_estacion in ciudades.items():
        print(f"→ Consultando {ciudad}...")
        url = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{id_estacion}"
        
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                detalles_url = r.json().get('datos')
                if detalles_url:
                    resp_datos = requests.get(detalles_url)
                    lecturas = resp_datos.json()
                    
                    if lecturas:
                        ultima = lecturas[-1]
                        # EXTRAEMOS LOS NUEVOS CAMPOS CRÍTICOS
                        datos_procesados[ciudad] = {
                            "fecha": fecha_hoy,
                            "estacion": ciudad,
                            "id_estacion": id_estacion,
                            "temp_max": ultima.get('ta'),
                            "temp_min": ultima.get('ta'),
                            "precipitacion": ultima.get('prec', 0),
                            "humedad": ultima.get('hr'),      # Humedad Relativa %
                            "viento_vel": ultima.get('vv')    # Velocidad viento km/h
                        }
                        print(f"  ✓ Datos completos recibidos (Temp, Hum, Viento).")
            else:
                print(f"  ✗ Estación no disponible.")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    if datos_procesados:
        registros = list(datos_procesados.values())
        print(f"\n→ Guardando {len(registros)} estaciones con datos enriquecidos...")
        try:
            supabase.table("datos_clima").upsert(registros, on_conflict="fecha, estacion").execute()
            print("✓ Base de datos de clima actualizada.")
        except Exception as e:
            print(f"✗ Error Supabase: {e}")

if __name__ == "__main__":
    obtener_clima_extremadura()
