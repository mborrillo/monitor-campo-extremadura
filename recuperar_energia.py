import requests
from supabase import create_client, Client
from datetime import datetime, timedelta
import time

SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def recuperar_rango(dias_atras):
    for i in range(dias_atras, -1, -1):
        fecha_consulta = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        print(f"⏳ Recuperando datos del: {fecha_consulta}...")
        
        url = f"https://api.esios.ree.es/archives/70/download_json?locale=es&date={fecha_consulta}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                datos = response.json()
                dict_limpio = {}
                for hora_dato in datos.get('PVPC', []):
                    precio_kwh = float(hora_dato['PCB'].replace(',', '.')) / 1000
                    hora_int = int(hora_dato['Dia'].split('-')[0]) if '-' in hora_dato['Dia'] else 0
                    dict_limpio[hora_int] = precio_kwh
                
                if dict_limpio:
                    precios_unicos = list(dict_limpio.values())
                    media_dia = sum(precios_unicos) / len(precios_unicos)
                    registros = []
                    for h, p in dict_limpio.items():
                        vs_media = ((p - media_dia) / media_dia) * 100
                        registros.append({
                            "fecha": fecha_consulta, "hora": h, "precio_kwh": round(p, 5),
                            "tramo": "Calculado", "vs_media": round(vs_media, 2)
                        })
                    supabase.table("datos_energia").upsert(registros, on_conflict="fecha, hora").execute()
                    print(f"✅ {fecha_consulta} guardado.")
                
            time.sleep(1) # Pausa para no saturar la API
        except Exception as e:
            print(f"❌ Error en {fecha_consulta}: {e}")

if __name__ == "__main__":
    # Cambia el 7 por los días que quieras recuperar (ej. 30 para un mes)
    recuperar_rango(10)
