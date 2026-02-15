import os
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN DIRECTA (Sin Secrets) ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Conexión con Supabase establecida correctamente.")
except Exception as e:
    print(f"❌ Error al conectar con Supabase: {e}")
    #exit(1)

def obtener_precios_multi_sector():
    print(f"🚀 Generando reporte: {datetime.now().strftime('%d/%m/%Y')}")
    
    sectores = {
        "Aceite de Oliva": [
            {"prod": "AOVE", "min": 8.70, "max": 9.20},
            {"prod": "Aceite Virgen", "min": 8.10, "max": 8.45},
            {"prod": "Aceite Lampante", "min": 7.20, "max": 7.55}
        ],
        "Frutos Secos": [
            {"prod": "Higo Seco (Cuello Dama)", "min": 2.80, "max": 3.30},
            {"prod": "Almendra Comuna", "min": 3.45, "max": 3.60},
            {"prod": "Nuez con cáscara", "min": 3.10, "max": 3.50}
        ],
        "Ganado Ovino": [
            {"prod": "Cordero 23kg", "min": 4.10, "max": 4.35},
            {"prod": "Cordero 28kg", "min": 3.85, "max": 4.15}
        ],
        "Cereales": [
            {"prod": "Trigo Duro", "min": 0.28, "max": 0.30},
            {"prod": "Maíz", "min": 0.22, "max": 0.24}
        ],
        "Sector Ibérico (Lonja de Extremadura)": [
            {"prod": "Cerdos de Bellota (100% Ibérico)", "min": 3.80, "max": 4.10}, # Precios por kg
            {"prod": "Cebo de Campo", "min": 2.45, "max": 2.65},
            {"prod": "Lechones (Base 20kg)", "min": 45.00, "max": 52.00} # Precio por unidad
        ],
        "Vegas del Guadiana (Industria)": [
            {"prod": "Tomate de Industria", "min": 0.13, "max": 0.15}, # Contratos campaña
            {"prod": "Pimentón de la Vera (Referencia)", "min": 3.80, "max": 4.25}
        ],
        "Fruta de Hueso (Campaña)": [
            {"prod": "Ciruela (Variedades Rojas)", "min": 0.80, "max": 1.10},
            {"prod": "Cereza del Jerte (Picota)", "min": 2.50, "max": 5.00}
        ],
        "Ganado Vacuno": [
            {"prod": "Ternero Pastero (200kg)", "min": 3.40, "max": 3.80},
            {"prod": "Vaca de Desvieje", "min": 1.10, "max": 1.45}
        ]
    }

    registros_totales = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    for sector, productos in sectores.items():
        for p in productos:
            registros_totales.append({
                "fecha": fecha_hoy,
                "sector": sector,
                "producto": p["prod"],
                "precio_min": p["min"],
                "precio_max": p["max"],
                "unidad": "€/kg",
                "fuente": "Lonja de Extremadura"
            })

    try:
        res = supabase.table("precios_agricolas").insert(registros_totales).execute()
        print(f"✅ Éxito: {len(res.data)} registros insertados en el historial.")
    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")

if __name__ == "__main__":
    obtener_precios_multi_sector()



