import os
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_precios_locales():
    print(f"🚜 Actualizando Precios de Lonja con Analítica...")
    
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    # Estos precios son los que tú irás actualizando en este diccionario
    # hasta que logremos automatizar la lectura de la web de la lonja.
    sectores = {
        "Aceite de Oliva": [
            {"prod": "AOVE", "min": 8.75, "max": 9.25, "uni": "€/kg"},
            {"prod": "Aceite Virgen", "min": 8.15, "max": 8.50, "uni": "€/kg"}
        ],
        "Sector Ibérico": [
            {"prod": "Cerdos de Bellota (100% Ibérico)", "min": 3.85, "max": 4.15, "uni": "€/kg"},
            {"prod": "Cebo de Campo", "min": 2.50, "max": 2.70, "uni": "€/kg"}
        ],
        "Ganado Vacuno": [
            {"prod": "Ternero Pastero (200kg)", "min": 3.45, "max": 3.85, "uni": "€/kg"},
            {"prod": "Vaca de Desvieje", "min": 1.15, "max": 1.50, "uni": "€/kg"}
        ]
    }

    registros_finales = []

    for sector, productos in sectores.items():
        for p in productos:
            precio_med_hoy = (p["min"] + p["max"]) / 2
            
            # 1. Intentamos buscar el precio anterior para calcular la tendencia
            variacion = 0
            try:
                res = supabase.table("datos_agrotech")\
                    .select("precio_min, precio_max")\
                    .eq("producto", p["prod"])\
                    .order("fecha", desc=True)\
                    .limit(1).execute()
                
                if res.data:
                    ant = res.data[0]
                    med_ant = (ant["precio_min"] + ant["precio_max"]) / 2
                    variacion = ((precio_med_hoy - med_ant) / med_ant) * 100
            except:
                variacion = 0

            registros_finales.append({
                "fecha": fecha_hoy,
                "sector": sector,
                "producto": p["prod"],
                "precio_min": p["min"],
                "precio_max": p["max"],
                "variacion_p": round(variacion, 2),
                "unidad": p["uni"],
                "fuente": "Lonja de Extremadura"
            })

    if registros_finales:
        # El upsert evita los duplicados que vimos en tu CSV
        supabase.table("datos_agrotech").upsert(
            registros_finales, on_conflict="fecha, producto"
        ).execute()
        print(f"✅ Lonja actualizada. {len(registros_finales)} productos procesados.")

if __name__ == "__main__":
    obtener_precios_locales()
