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

def obtener_clima_inteligente():
    print(f"🌦️ Iniciando captura de clima inteligente: {datetime.now()}")
    
    ciudades = {"BADAJOZ": "4452", "CÁCERES": "3469A", "MËRIDA": "4410X", "ALMENDRALEJO": "4436Y", "DON BENITO": "4358X", "OLIVENZA": "4486X", "ZAFRA": "4427X","HERVÁS":"3504X","PLASENCIA":"3519X","NAVALMORAL DE LA MATA":"3434X" }
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
                    # Filtramos solo las lecturas que pertenecen al día de hoy
                    lecturas_hoy = [l for l in lecturas if l.get('fint', '').startswith(fecha_hoy)]
                    
                    if not lecturas_hoy:
                        # Si es muy temprano, usamos la última lectura disponible para tener continuidad
                        lecturas_hoy = [lecturas[-1]]

                    # --- PROCESAMIENTO ANALÍTICO ---
                    temps = [l.get('ta') for l in lecturas_hoy if l.get('ta') is not None]
                    precips = [l.get('prec') for l in lecturas_hoy if l.get('prec') is not None]
                    
                    t_max = max(temps) if temps else None
                    t_min = min(temps) if temps else None
                    p_acumulada = sum(precips) if precips else 0
                    
                    ultima = lecturas_hoy[-1]

                    registro = {
                        "fecha": fecha_hoy,
                        "estacion": ciudad,
                        "id_estacion": id_estacion,
                        "temp_max": t_max,
                        "temp_min": t_min,
                        "temp_actual": ultima.get('ta'),
                        "precipitacion": round(p_acumulada, 2),
                        "humedad": ultima.get('hr'),
                        "viento_vel": ultima.get('vv')
                        ,"latitud": Lat
                        ,"longitud": Long
                    }

                    supabase.table("datos_clima").upsert(registro, on_conflict="fecha, estacion").execute()
                    print(f"✅ {ciudad}: Max {t_max}° / Min {t_min}° / Lluvia {round(p_acumulada, 2)}mm")
        
        except Exception as e:
            print(f"❌ Error procesando {ciudad}: {e}")

if __name__ == "__main__":
    obtener_clima_inteligente()
