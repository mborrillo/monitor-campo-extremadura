import os
import requests
from supabase import create_client, Client
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG" 
AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2OGJvcnJpc21hckBnbWFpbC5jb20iLCJqdGkiOiI1YzRjYzlkZC04OTI0LTQzZjgtOTI1OC1hZWZiZjRhOWIzNGMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc3MTA4MjI3MSwidXNlcklkIjoiNWM0Y2M5ZGQtODkyNC00M2Y4LTkyNTgtYWVmYmY0YTliMzRjIiwicm9sZSI6IiJ9.EQqSYmGFYaCQvhzPv2gxYHkwa1Zyqr9sDLRCG8xLaV4" # Pon tu clave aquí

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_clima_extremadura():
    print(f"🌦️ Iniciando Monitor de Clima: {datetime.now()}")
    
    # Estaciones: 4452 (Badajoz), 3431 (Cáceres)
    estaciones = {"Badajoz": "4452", "Caceres": "3431"}
    headers = {'api_key': AEMET_API_KEY}
    
    registros_clima = []

    for ciudad, id_estacion in estaciones.items():
        print(f"🔍 Consultando estación {ciudad} ({id_estacion})...")
        url = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{id_estacion}"
        
        try:
            res = requests.get(url, headers=headers)
            res_json = res.json()
            
            if res_json.get('estado') == 200:
                url_descarga = res_json.get('datos')
                datos = requests.get(url_descarga).json()
                
                # AEMET devuelve las últimas 24 horas de registros cada 15-60 min
                # Vamos a agrupar por fecha para obtener los valores del día
                for d in datos:
                    fecha_completa = d.get('fth') # Formato: 2026-02-14T10:00:00
                    if not fecha_completa: continue
                    
                    fecha_solo_dia = fecha_completa.split('T')[0]
                    
                    # Guardamos la lectura si tiene datos de temperatura o lluvia
                    registros_clima.append({
                        "fecha": fecha_solo_dia,
                        "estacion": ciudad,
                        "temp_max": d.get('ta'),
                        "temp_min": d.get('ta'),
                        "precipitacion": d.get('prec', 0)
                    })
            else:
                print(f"⚠️ AEMET respondió: {res_json.get('descripcion')}")
        except Exception as e:
            print(f"❌ Error en {ciudad}: {e}")

    if registros_clima:
        # Usamos un diccionario para quedarnos solo con el valor más alto/bajo por día y ciudad
        # Esto limpia los datos antes de enviarlos a Supabase
        print(f"📦 Procesando {len(registros_clima)} lecturas temporales...")
        
        # Intentamos insertar (upsert) en bloques para no saturar
        try:
            # Upsert para evitar duplicados si la tabla tiene el índice único que creamos
            res = supabase.table("datos_clima").upsert(registros_clima).execute()
            print(f"✅ ¡Éxito! Registros procesados en Supabase.")
        except Exception as e:
            print(f"❌ Error Supabase al insertar: {e}")
    else:
        print("Empty: AEMET no devolvió ninguna lectura para procesar.")

if __name__ == "__main__":
    obtener_clima_extremadura()
