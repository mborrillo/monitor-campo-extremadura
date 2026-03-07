# ══════════════════════════════════════════════════════════════════
# ARCHIVO: energia_monitor.py
# PROYECTO: Monitor Campo Extremadura — Ingesta de Energía
# PLATAFORMA: Script ETL · ejecutado via GitHub Actions
# FUENTE: Red Eléctrica de España (REE) — precio PVPC
# DESTINO: Supabase → tabla datos_energia
# REPO: https://github.com/mborrillo/agro-tech-es
# ══════════════════════════════════════════════════════════════════

import requests
from supabase import create_client, Client
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_tramo(hora, es_fin_de_semana):
    if es_fin_de_semana:
        return "Valle"
    if 0 <= hora < 8:
        return "Valle"
    elif hora in [10, 11, 12, 13, 18, 19, 20, 21]:
        return "Punta"
    else:
        return "Llano"

def obtener_precios_luz():
    print("⚡ Consultando Precios de Energía (REE) con Analítica y Limpieza...")
    
    ahora = datetime.now()
    fecha_hoy = ahora.strftime("%Y-%m-%d")
    fecha_ayer = (ahora - timedelta(days=1)).strftime("%Y-%m-%d")
    es_fin_de_semana = ahora.weekday() >= 5
    
    url = f"https://api.esios.ree.es/archives/70/download_json?locale=es&date={fecha_hoy}"
    
    try:
        # Paso 0: Obtener media del día anterior para calcular var_precio_p
        media_ayer = None
        try:
            r_ayer = supabase.table("datos_energia").select("precio_kwh").eq("fecha", fecha_ayer).execute()
            if r_ayer.data:
                precios_ayer = [row["precio_kwh"] for row in r_ayer.data]
                media_ayer = sum(precios_ayer) / len(precios_ayer)
                print(f"📅 Media ayer ({fecha_ayer}): {round(media_ayer, 4)} €/kWh")
            else:
                print(f"⚠️ Sin datos del día anterior ({fecha_ayer}) para calcular variación")
        except Exception as e_ayer:
            print(f"⚠️ No se pudo obtener media de ayer: {e_ayer}")

        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"⚠️ Error API REE: {response.status_code}")
            return

        datos = response.json()
        dict_limpio = {}

        # Paso 1: Recolectar y limpiar
        # Usamos enumerate() en lugar de parsear el campo 'Dia' porque ESIOS cambió
        # su formato en Feb 2026 (de "0-1" a "2026-02-19") rompiendo el split('-')[0]
        # La API siempre devuelve las 24 horas en orden, así que el índice = hora
        for hora_int, hora_dato in enumerate(datos.get('PVPC', [])):
            try:
                precio_kwh = float(hora_dato['PCB'].replace(',', '.')) / 1000
            except (KeyError, ValueError):
                try:
                    precio_kwh = float(hora_dato['TCHA'].replace(',', '.')) / 1000
                except (KeyError, ValueError):
                    continue
            dict_limpio[hora_int] = precio_kwh

        if not dict_limpio:
            print("⚠ No se encontraron datos de PVPC.")
            return

        # Paso 2: Calcular la media del día actual
        precios_unicos = list(dict_limpio.values())
        media_dia = sum(precios_unicos) / len(precios_unicos)

        # Paso 3: Calcular var_precio_p (variación media hoy vs media ayer)
        if media_ayer is not None:
            var_precio_p = round(((media_dia - media_ayer) / media_ayer) * 100, 2)
            signo = "+" if var_precio_p > 0 else ""
            print(f"📊 Media hoy: {round(media_dia, 4)} €/kWh  |  var_precio_p: {signo}{var_precio_p}%")
        else:
            var_precio_p = None
            print(f"📊 Media hoy: {round(media_dia, 4)} €/kWh  |  var_precio_p: sin referencia")

        # Paso 4: Preparar registros finales
        registros_finales = []
        for hora_int, precio in dict_limpio.items():
            vs_media = round(((precio - media_dia) / media_dia) * 100, 2)
            tramo = obtener_tramo(hora_int, es_fin_de_semana)
            registros_finales.append({
                "fecha": fecha_hoy,
                "hora": hora_int,
                "precio_kwh": round(precio, 5),
                "tramo": tramo,
                "vs_media": round(vs_media, 2),
                "var_precio_p": var_precio_p,
            })

        # Paso 5: Guardar en Supabase
        if registros_finales:
            supabase.table("datos_energia").upsert(
                registros_finales,
                on_conflict="fecha, hora"
            ).execute()
            print(f"✅ ¡Éxito! {len(registros_finales)} registros guardados. (Media: {round(media_dia, 4)} €/kWh).")

    except Exception as e:
        print(f"❌ Error en monitor de energía: {e}")

if __name__ == "__main__":
    obtener_precios_luz()
