import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN DE CONEXIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp6dWN2c3JlbWF2a2lrZWNzcHRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA5ODIzMTUsImV4cCI6MjA4NjU1ODMxNX0.3J-whUICeuP-IgrVJ4J7t7ZpawqVn8arGSboNIZHetw" # Asegúrate de mantener la Service Role Key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_precios_multi_sector():
    print(f"🚀 Generando reporte multisectorial: {datetime.now().strftime('%d/%m/%Y')}")
    
    # Definimos los diccionarios de datos reales de las últimas sesiones 
    # (Esto lo automatizaremos sector por sector conforme mapeemos las URLs)
    
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
        ]
    }

    registros_totales = []
    
    for sector, productos in sectores.items():
        for p in productos:
            registros_totales.append({
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "sector": sector,
                "producto": p["prod"],
                "precio_min": p["min"],
                "precio_max": p["max"],
                "unidad": "€/kg",
                "fuente": "Lonja de Extremadura"
            })

    try:
        # Inserción masiva (Bulk insert) - Mucho más eficiente
        res = supabase.table("precios_agricolas").insert(registros_totales).execute()
        print(f"✅ Monitor expandido: {len(res.data)} nuevos registros en 4 sectores.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    obtener_precios_multi_sector()