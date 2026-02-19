import os
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_precios_locales():
    print(f"🚜 Actualizando Precios de Lonja (Extremadura) - {datetime.now().strftime('%d/%m/%Y')}")
    
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    # DICCIONARIO UNIFICADO Y ESCALABLE
    # Estos nombres de sector aparecerán directamente en los filtros de tu Dashboard
    sectores = {
        "Aceites": [
            {"prod": "AOVE", "min": 8.75, "max": 9.25, "uni": "€/kg"},
            {"prod": "Aceite Virgen", "min": 8.15, "max": 8.50, "uni": "€/kg"}
        ],
        "Porcino": [
            {"prod": "Cerdos de Bellota (100% Ibérico)", "min": 3.85, "max": 4.15, "uni": "€/kg"},
            {"prod": "Cebo de Campo", "min": 2.50, "max": 2.70, "uni": "€/kg"}
        ],
        "Vacuno": [
            {"prod": "Ternero Pastero (200kg)", "min": 3.45, "max": 3.85, "uni": "€/kg"},
            {"prod": "Vaca de Desvieje", "min": 1.15, "max": 1.50, "uni": "€/kg"}
        ],
        "Cereales": [
            {"prod": "Trigo Duro", "min": 0.28, "max": 0.30, "uni": "€/kg"},
            {"prod": "Maíz", "min": 0.22, "max": 0.24, "uni": "€/kg"}
        ],
        "Industria": [
            {"prod": "Tomate de Industria", "min": 0.13, "max": 0.15, "uni": "€/kg"},
            {"prod": "Pimentón de la Vera", "min": 3.80, "max": 4.25, "uni": "€/kg"}
        ],
        "Frutas": [
            {"prod": "Cereza del Jerte (Picota)", "min": 2.50, "max": 5.00, "uni": "€/kg"}
        ]
    }

    registros_finales = []

    for sector, productos in sectores.items():
        for p in productos:
            precio_med_hoy = (p["min"] + p["max"]) / 2
            
            # Lógica de analítica: Buscamos el último precio registrado para este producto
            variacion = 0
            try:
                res = supabase.table("precios_agricolas")\
                    .select("precio_min, precio_max")\
                    .eq("producto", p["prod"])\
                    .order("fecha", desc=True)\
                    .limit(1).execute()
                
                if res.data:
                    ant = res.data[0]
                    med_ant = (ant["precio_min"] + ant["precio_max"]) / 2
                    if med_ant > 0:
                        variacion = ((precio_med_hoy - med_ant) / med_ant) * 100
            except Exception:
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
        try:
            # El upsert garantiza integridad y evita los duplicados detectados anteriormente
            supabase.table("precios_agricolas").upsert(
                registros_finales, 
                on_conflict="fecha, producto"
            ).execute()
            print(f"✅ Lonja sincronizada: {len(registros_finales)} productos actualizados.")
        except Exception as e:
            print(f"❌ Error al guardar en Supabase: {e}")

if __name__ == "__main__":
    obtener_precios_locales()
