import requests
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_precios_luz():
    print("⚡ Consultando Precios de Energía (REE)...")
    
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    # Endpoint de ESIOS para el PVPC (Indicador 1001)
    url = f"https://api.esios.ree.es/archives/70/download_json?locale=es&date={fecha_hoy}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"⚠️ No se pudo conectar con REE: {response.status_code}")
            return

        datos = response.json()
        # Usamos un diccionario para limpiar duplicados antes de enviar a Supabase
        registros_dict = {}
        
        # Procesamos el bloque PVPC que devuelve la API
        for hora_dato in datos.get('PVPC', []):
            # El precio viene en €/MWh, lo pasamos a €/kWh
            precio_mwh = float(hora_dato['PCB'].replace(',', '.'))
            precio_kwh = precio_mwh / 1000
            
            # Extraemos la hora (ej: de "00-01" tomamos el 0)
            hora_str = hora_dato['Dia'].split('-')[0] if '-' in hora_dato['Dia'] else "0"
            hora_int = int(hora_str)
            
            # Guardamos en el diccionario usando la hora como clave
            registros_dict[hora_int] = {
                "fecha": fecha_hoy,
                "hora": hora_int,
                "precio_kwh": round(precio_kwh, 5)
            }

        # Si tenemos datos, los enviamos todos juntos
        if registros_dict:
            lista_final = list(registros_dict.values())
            supabase.table("datos_energia").upsert(
                lista_final, 
                on_conflict="fecha, hora"
            ).execute()
            print(f"✅ ¡Éxito! {len(lista_final)} precios horarios guardados en Supabase.")

    except Exception as e:
        print(f"❌ Error en el monitor de energía: {e}")

if __name__ == "__main__":
    obtener_precios_luz()
