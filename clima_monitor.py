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
    print(f"=== Monitor de Clima Inteligente - {datetime.now().strftime('%d/%m/%Y %H:%M')} ===")
    
    ciudades = {"Badajoz": "4452", "Caceres": "3431", "Merida": "4455"}
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    for ciudad, id_estacion in ciudades.items():
        url_aemet = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{id_estacion}"
        params = {"api_key": AEMET_API_KEY}

        try:
            r = requests.get(url_aemet, params=params)
            if r.status_code == 200:
                datos_url = r.json().get('datos')
                resp_datos = requests.get(datos_url)
                lecturas = resp_datos.json()

                if lecturas:
                    # FILTRAMOS LECTURAS SOLO DE HOY
                    lecturas_hoy = [l for l in lecturas if l.get('fint', '').startswith(fecha_hoy)]
                    
                    if not lecturas_hoy: # Si es muy temprano, tomamos la última disponible
                        lecturas_hoy = [lecturas[-1]]

                    # PROCESAMOS ANALÍTICA DIARIA
                    temps = [l.get('ta') for l in lecturas_hoy if l.get('ta') is not None]
                    precips = [l.get('prec') for l in lecturas_hoy if l.get('prec') is not None]
                    
                    temp_max = max(temps) if temps else None
                    temp_min = min(temps) if temps else None
                    precip_acumulada = sum(precips) if precips else 0
                    
                    ultima = lecturas_hoy[-1] # Para humedad y viento tomamos la actual

                    registro = {
                        "fecha": fecha_hoy,
                        "estacion": ciudad,
                        "id_estacion": id_estacion,
                        "temp_max": temp_max,
                        "temp_min": temp_min,
                        "temp_actual": ultima.get('ta'), # Nueva columna recomendada
                        "precipitacion": round(precip_acumulada, 2),
                        "humedad": ultima.get('hr'),
                        "viento_vel": ultima.get('vv')
                    }

                    supabase.table("datos_clima").upsert(registro, on_conflict="fecha, estacion").execute()
                    print(f"  ✓ {ciudad}: Max {temp_max}ºC / Min {temp_min}ºC / Lluvia {round(precip_acumulada, 2)}mm")
        except Exception as e:
            print(f"  ✗ Error en {ciudad}: {e}")

if __name__ == "__main__":
    obtener_clima_extremadura()
