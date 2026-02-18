import requests
from supabase import create_client, Client
from datetime import datetime, timedelta
import time

# --- CONFIGURACIÓN ---
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
        
        print(f"⏳ Procesando analítica completa del: {fecha_str}...")
        url = f"https://api.esios.ree.es/archives/70/download_json?locale=es&date={fecha_str}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                datos = response.json()
                pvpc_data = datos.get('PVPC', [])
                
                if not pvpc_data:
                    print(f"⚠️ Sin datos para {fecha_str}")
                    continue

                registros_dia = []
                precios_solo = []

                # Primero extraemos precios para calcular la media
                for item in pvpc_data:
                    p = float(item['PCB'].replace(',', '.')) / 1000
                    precios_solo.append(p)
                
                media_dia = sum(precios_solo) / len(precios_solo)

                # Ahora procesamos cada hora con su tramo
                for idx, item in enumerate(pvpc_data):
                    # Usamos el índice (0 a 23) como hora para evitar el error de formato de fecha
                    hora_real = idx 
                    precio = float(item['PCB'].replace(',', '.')) / 1000
                    vs_media = ((precio - media_dia) / media_dia) * 100
                    tramo = obtener_tramo_real(hora_real, es_fin_de_semana)
                    
                    registros_dia.append({
                        "fecha": fecha_str,
                        "hora": hora_real,
                        "precio_kwh": round(precio, 5),
                        "tramo": tramo,
                        "vs_media": round(vs_media, 2)
                    })
                
                # Guardado masivo por día
                if registros_dia:
                    supabase.table("datos_energia").upsert(registros_dia, on_conflict="fecha, hora").execute()
                    print(f"✅ {fecha_str}: {len(registros_dia)} horas guardadas. Media: {round(media_dia,4)}")
            
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Error crítico en {fecha_str}: {e}")

if __name__ == "__main__":
    recuperar_rango_inteligente(15)
