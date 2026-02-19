import os
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_precios_locales():
    ahora = datetime.now()
    fecha_hoy = ahora.strftime("%Y-%m-%d")
    print(f"🚜 Sincronizando Lonja de Extremadura: {fecha_hoy}")
    
    sectores = {
        "Aceites": [
            {"prod": "AOVE", "var": "Multivarietal", "min": 8.75, "max": 9.25, "uni": "€/kg"},
            {"prod": "Aceite Virgen", "var": "Estándar", "min": 8.15, "max": 8.50, "uni": "€/kg"}
        ],
        "Porcino": [
            {"prod": "Cerdos de Bellota (100% Ibérico)", "var": "Bellota", "min": 3.85, "max": 4.15, "uni": "€/kg"},
            {"prod": "Cebo de Campo", "var": "Ibérico", "min": 2.50, "max": 2.70, "uni": "€/kg"}
        ],
        "Vacuno": [
            {"prod": "Ternero Pastero (200kg)", "var": "Cruzado", "min": 3.45, "max": 3.85, "uni": "€/kg"},
            {"prod": "Vaca de Desvieje", "var": "Industria", "min": 1.15, "max": 1.50, "uni": "€/kg"}
        ],
        "Cereales": [
            {"prod": "Trigo Duro", "var": "RGT Pelayo", "min": 0.28, "max": 0.30, "uni": "€/kg"},
            {"prod": "Maíz", "var": "Standard", "min": 0.22, "max": 0.24, "uni": "€/kg"}
        ]
    }

    registros_finales = []

    for sector, productos in sectores.items():
        for p in productos:
            precio_med_hoy = (p["min"] + p["max"]) / 2
            med_ant = None
            variacion = 0
            
            try:
                # Buscamos el precio más reciente PERO que sea de una fecha anterior a hoy
                res = supabase.table("precios_agricolas")\
                    .select("precio_min, precio_max")\
                    .eq("producto", p["prod"])\
                    .lt("fecha", fecha_hoy)\
                    .order("fecha", desc=True)\
                    .limit(1).execute()
                
                if res.data:
                    ant = res.data[0]
                    med_ant = (ant["precio_min"] + ant["precio_max"]) / 2
                    variacion = ((precio_med_hoy - med_ant) / med_ant) * 100
            except Exception as e:
                print(f"  ℹ️ Sin histórico para {p['prod']}")

            registros_finales.append({
                "fecha": fecha_hoy,
                "sector": sector,
                "producto": p["prod"],
                "variedad": p["var"], # Ahora sí enviamos variedad
                "precio_min": p["min"],
                "precio_max": p["max"],
                "precio_anterior_med": round(med_ant, 4) if med_ant else None, # GUARDAMOS EL DATO
                "variacion_p": round(variacion, 2) if variacion != 0 else 0,
                "unidad": p["uni"],
                "fuente": "Lonja de Extremadura"
            })

    if registros_finales:
        try:
            supabase.table("precios_agricolas").upsert(
                registros_finales, on_conflict="fecha, producto"
            ).execute()
            print(f"✅ ¡Hecho! {len(registros_finales)} registros procesados con analítica completa.")
        except Exception as e:
            print(f"❌ Error Supabase: {e}")

if __name__ == "__main__":
    obtener_precios_locales()
