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

# DICCIONARIO DE GEOPOSICIÓN
ESTACIONES_EXTREMADURA = {
    "4478X": {"nombre": "BADAJOZ", "lat": 38.882, "lon": -6.845},
    "3469A": {"nombre": "CÁCERES", "lat": 39.482, "lon": -6.340},
    "4410X": {"nombre": "MÉRIDA", "lat": 38.922, "lon": -6.350},
    "4436Y": {"nombre": "ALMENDRALEJO", "lat": 38.681, "lon": -6.408},
    "4358X": {"nombre": "DON BENITO", "lat": 38.946, "lon": -5.845},
    "4486X": {"nombre": "OLIVENZA", "lat": 38.685, "lon": -7.098},
    "4427X": {"nombre": "ZAFRA", "lat": 38.423, "lon": -6.405},
    "3504X": {"nombre": "HERVÁS", "lat": 40.274, "lon": -5.861},
    "3519X": {"nombre": "PLASENCIA", "lat": 40.034, "lon": -6.075},
    "3434X": {"nombre": "NAVALMORAL DE LA MATA", "lat": 39.889, "lon": -5.541},
    "4386B": {"nombre": "LLERENA", "lat": 38.238, "lon": -6.012},
    "4411C": {"nombre": "ALCUESCAR", "lat": 39.181, "lon": -6.230},
    "3463Y": {"nombre": "TRUJILLO", "lat": 39.462, "lon": -5.877},
    "4511C": {"nombre": "JEREZ DE LOS CABALLEROS", "lat": 38.324, "lon": -6.772},
    "4501X": {"nombre": "FUENTE DE CANTOS", "lat": 38.243, "lon": -6.311},
    "4499X": {"nombre": "MONESTERIO", "lat": 38.087, "lon": -6.273},
    "3576X": {"nombre": "VALENCIA DE ALCÁNTARA", "lat": 39.412, "lon": -7.243},
    "4244X": {"nombre": "HERRERA DEL DUQUE", "lat": 39.167, "lon": -5.048},
    "4520X": {"nombre": "FREGENAL DE LA SIERRA", "lat": 38.169, "lon": -6.654},
    "4468X": {"nombre": "PUEBLA DE OBANDO", "lat": 39.176, "lon": -6.632},
    "4395X": {"nombre": "VILLAFRANCA DE LOS BARROS", "lat": 38.563, "lon": -6.335},
    "4362X": {"nombre": "RETAMAL DE LLERENA", "lat": 38.577, "lon": -5.836},
    "3562X": {"nombre": "ALISEDA", "lat": 39.421, "lon": -6.691},
    "3475X": {"nombre": "CAÑAVERAL", "lat": 39.790, "lon": -6.391},
    "3436D": {"nombre": "GARGANTA LA OLLA", "lat": 40.111, "lon": -5.773},
    "3455X": {"nombre": "JARAICEJO", "lat": 39.667, "lon": -5.811},
    "4236Y": {"nombre": "PUERTO REY", "lat": 39.423, "lon": -5.025},
    "3531X": {"nombre": "TORRECILLA DE LOS ANGELES", "lat": 40.245, "lon": -6.467}
}

def obtener_clima():
    # ... (tu lógica de llamada a la API de AEMET)
    
    registros_clima = []
    
    # Supongamos que 'dato' es el JSON que devuelve AEMET para una estación
    for dato in datos_aemet:
        id_estacion = dato.get('idema')
        
        if id_estacion in ESTACIONES_EXTREMADURA:
            info_geo = ESTACIONES_EXTREMADURA[id_estacion]
            
            registro = {
                "fecha": dato.get('fint'),
                "localidad": info_geo['nombre'],
                "latitud": info_geo['lat'],
                "longitud": info_geo['lon'],
                "temperatura": dato.get('ta'),
                "humedad": dato.get('hr'),
                "viento_velocidad": dato.get('vv'),
                "precipitacion": dato.get('prec')
            }
            registros_clima.append(registro)

    # GUARDADO EN SUPABASE
    supabase.table("datos_clima").upsert(registros_clima).execute()

def obtener_clima_inteligente():
    print(f"🌦️ Iniciando captura de clima inteligente: {datetime.now()}")
    
    ciudades = {"BADAJOZ": "4478X", "CÁCERES": "3469A", "MÉRIDA": "4410X", "ALMENDRALEJO": "4436Y", "DON BENITO": "4358X", "OLIVENZA": "4486X", "ZAFRA": "4427X","HERVÁS":"3504X","PLASENCIA":"3519X","NAVALMORAL DE LA MATA":"3434X","LLERENA":"4386B","ALCUESCAR":"4411C","TRUJILLO":"3463Y", 
                "JEREZ DE LOS CABALLEROS":"4511C", "FUENTE DE CANTOS":"4501X", "MONESTERIO":"4499X", "VALENCIA DE ALCÁNTARA":"3576X","HERRERA DEL DUQUE":"4244X","FREGENAL DE LA SIERRA":"4520X","PUEBLA DE OBANDO":"4468X","VILLAFRANCA DE LOS BARROS":"4395X","RETAMAL DE LLERENA":"4362X",
                "ALISEDA":"3562X","CAÑAVERAL":"3475X","GARGANTA LA OLLA":"3436D","JARAICEJO":"3455X","PUERTO REY":"4236Y","TORRECILLA DE LOS ANGELES":"3531X"}
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
                        "viento_vel": ultima.get('vv'),
                        "latitud": Lat,
                        "longitud": Long,
                        "estado_tratamiento": estado
                    }

                    supabase.table("datos_clima").upsert(registro, on_conflict="fecha, estacion").execute()
                    print(f"✅ {ciudad}: Max {t_max}° / Min {t_min}° / Lluvia {round(p_acumulada, 2)}mm")
        
        except Exception as e:
            print(f"❌ Error procesando {ciudad}: {e}")

if __name__ == "__main__":
    obtener_clima_inteligente()
