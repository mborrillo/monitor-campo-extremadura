import os
import requests
from supabase import create_client, Client
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG" 
AEMET_API_KEY = "TU_API_KEY_AQUI" # Asegúrate de poner tu clave aquí

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_clima_extremadura():
    ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"🌦️ Buscando datos consolidados del día: {ayer}")
    
    # Estaciones: 4452 (Badajoz), 3431 (Cáceres)
    estaciones = {"Badajoz": "4452", "Caceres": "3431"}
    headers = {'api_key': AEMET_API_KEY}
    registros_clima = []

    for ciudad, id_estacion in estaciones.items():
        url = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{id_estacion}"
        
        try:
            res = requests.get(url, headers=headers)
            res_json = res.json()
            
            if res_json.get('estado') == 200:
                url_descarga = res_json.get('datos')
                datos = requests.get(url_descarga).json()
                
                # Filtramos solo las lecturas que pertenecen al día de ayer
                lecturas_ayer = [d for d in datos if ayer in d.get('fth', '')]
                
                if lecturas_ayer:
                    # Extraemos valores extremos del día
                    t_max = max([float(d.get('ta', -99)) for d in lecturas_ayer if d.get('ta') is not None], default=None)
                    t_min = min([float(d.get('ta', 99)) for d in lecturas_ayer if d.get('ta') is not None], default=None)
                    # La lluvia es el valor máximo acumulado reportado en el día (prec)
                    lluvia = max([float(d.get('prec', 0)) for d in lecturas_ayer if d.get('prec') is not None], default=0)

                    registros_clima.append({
                        "fecha": ayer,
                        "estacion": ciudad,
                        "temp_max": t_max,
                        "temp_min": t_min,
                        "precipitacion": lluvia
                    })
                    print(f"✅ Procesado {ciudad}: Max {t_max}°, Min {t_min}°, Lluvia {lluvia}mm")
            else:
                print(f"⚠️ AEMET no tiene datos listos para {ciudad} todavía.")
                
        except Exception as e:
            print(f"❌ Error en {ciudad}: {e}")

    if registros_clima:
        try:
            supabase.table("datos_clima").upsert(registros_clima).execute()
            print(f"📊 ¡Supabase actualizado con éxito!")
        except Exception as e:
            print(f"❌ Error Supabase: {e}")
    else:
        print("Empty: No se encontraron lecturas válidas para ayer.")

if __name__ == "__main__":
    obtener_clima_extremadura()
