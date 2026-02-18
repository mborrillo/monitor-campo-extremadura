import requests
from supabase import create_client, Client
from datetime import datetime, timedelta
import time

SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_tramo_real(hora, es_fin_de_semana):
    if es_fin_de_semana:
        return "Valle"
    if 0 <= hora < 8:
        return "Valle"
    elif hora in [10, 11, 12, 13, 18, 19, 20, 21]:
        return "Punta"
    else:
        return "Llano"

def recuperar_rango_inteligente(dias_atras):
    for i in range(dias_atras, -1, -1):
        fecha_dt = datetime.now() - timedelta(days=i)
        fecha_str = fecha_dt.strftime("%Y-%m-%d")
        es_fin_de_semana = fecha_dt.weekday() >= 5
        
        print(f"⏳ Procesando analítica del: {fecha_str}...")
        url = f"https://api.esios.ree.es/archives/70/download_json?locale=es&date={fecha_str}"
        
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
                        tramo = obtener_tramo_real(h, es_fin_de_semana) # Lógica real
                        
                        registros.append({
                            "fecha": fecha_str, 
                            "hora": h, 
                            "precio_kwh": round(p, 5),
                            "tramo": tramo, 
                            "vs_media": round(vs_media, 2)
                        })
                    
                    supabase.table("datos_energia").upsert(registros, on_conflict="fecha, hora").execute()
                    print(f"✅ {fecha_str} corregido con tramos y analítica.")
            
            time.sleep(0.5) 
        except Exception as e:
            print(f"❌ Error en {fecha_str}: {e}")

if __name__ == "__main__":
    recuperar_rango_inteligente(15) # Recuperamos los últimos 15 días
