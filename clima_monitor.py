import os
import requests
from supabase import create_client, Client
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG" # Tu clave directa
AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2OGJvcnJpc21hckBnbWFpbC5jb20iLCJqdGkiOiI1YzRjYzlkZC04OTI0LTQzZjgtOTI1OC1hZWZiZjRhOWIzNGMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc3MTA4MjI3MSwidXNlcklkIjoiNWM0Y2M5ZGQtODkyNC00M2Y4LTkyNTgtYWVmYmY0YTliMzRjIiwicm9sZSI6IiJ9.EQqSYmGFYaCQvhzPv2gxYHkwa1Zyqr9sDLRCG8xLaV4" # <--- PEGA AQUÍ TU CLAVE DE AEMET

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_clima_extremadura():
    print(f"🌦️ Consultando AEMET: {datetime.now().strftime('%d/%m/%Y')}")
    
    # Consultamos los datos de AYER (ya que hoy aún no ha terminado)
    ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Estaciones: 4452 (Badajoz Talavera Real) y 3431 (Cáceres)
    estaciones = {"Badajoz": "4452", "Caceres": "3431"}
    
    headers = {'api_key': AEMET_API_KEY}
    registros_clima = []

    for ciudad, id_estacion in estaciones.items():
        # URL para datos diarios de una estación
        url = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{id_estacion}"
        
        try:
            # AEMET funciona en dos pasos: te da una URL de descarga y luego bajas los datos
            res = requests.get(url, headers=headers)
            url_descarga = res.json().get('datos')
            
            if url_descarga:
                datos = requests.get(url_descarga).json()
                # Tomamos la última lectura completa del día anterior
                # (Simplificado: buscamos el acumulado de precipitación y temp extremas)
                lectura = datos[-1] 
                
                registros_clima.append({
                    "fecha": ayer,
                    "estacion": ciudad,
                    "temp_max": lectura.get('ta', 0), # Temperatura actual/máxima
                    "temp_min": lectura.get('tamin', 0),
                    "precipitacion": lectura.get('prec', 0)
                })
                print(f"✅ Datos obtenidos para {ciudad}")
        except Exception as e:
            print(f"❌ Error en {ciudad}: {e}")

    if registros_clima:
        try:
            supabase.table("datos_clima").upsert(registros_clima).execute()
            print(f"📊 ¡Historial climático actualizado para {len(registros_clima)} estaciones!")
        except Exception as e:
            print(f"❌ Error al guardar en Supabase: {e}")

if __name__ == "__main__":
    obtener_clima_extremadura()
