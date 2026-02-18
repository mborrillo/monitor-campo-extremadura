import requests
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_tramo(hora, es_fin_de_semana):
    """Determina el tramo eléctrico en España (Península)"""
    if es_fin_de_semana:
        return "Valle"
    
    # Horarios laborables:
    if 0 <= hora < 8:
        return "Valle"
    elif hora in [10, 11, 12, 13, 18, 19, 20, 21]:
        return "Punta"
    else:
        return "Llano"

def obtener_precios_luz():
    print("⚡ Consultando Precios de Energía (REE) con Analítica...")
    
    ahora = datetime.now()
    fecha_hoy = ahora.strftime("%Y-%m-%d")
    es_fin_de_semana = ahora.weekday() >= 5 # 5=Sábado, 6=Domingo
    
    url = f"https://api.esios.ree.es/archives/70/download_json?locale=es&date={fecha_hoy}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"⚠️ Error API REE: {response.status_code}")
            return

        datos = response.json()
        precios_temp = []
        
        # Paso 1: Recolectar precios básicos
        for hora_dato in datos.get('PVPC', []):
            precio_kwh = float(hora_dato['PCB'].replace(',', '.')) / 1000
            hora_int = int(hora_dato['Dia'].split('-')[0]) if '-' in hora_dato['Dia'] else 0
            precios_temp.append({"hora": hora_int, "precio": precio_kwh})

        if not precios_temp:
            print("⚠ No se encontraron datos de PVPC.")
            return

        # Paso 2: Calcular la media del día
        suma_precios = sum(p['precio'] for p in precios_temp)
        media_dia = suma_precios / len(precios_temp)

        # Paso 3: Enriquecer datos para el "Semáforo"
        registros_finales = []
        for p in precios_temp:
            vs_media = ((p['precio'] - media_dia) / media_dia) * 100
            tramo = obtener_tramo(p['hora'], es_fin_de_semana)
            
            registros_finales.append({
                "fecha": fecha_hoy,
                "hora": p['hora'],
                "precio_kwh": round(p['precio'], 5),
                "tramo": tramo,
                "vs_media": round(vs_media, 2)
            })

        # Paso 4: Guardar en Supabase
        if registros_finales:
            supabase.table("datos_energia").upsert(
                registros_finales, 
                on_conflict="fecha, hora"
            ).execute()
            print(f"✅ ¡Éxito! 24 horas actualizadas con analítica (Media hoy: {round(media_dia, 4)} €/kWh).")

    except Exception as e:
        print(f"❌ Error en monitor de energía: {e}")

if __name__ == "__main__":
    obtener_precios_luz()
