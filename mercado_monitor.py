import yfinance as yf
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_datos_mercado():
    print("📈 Consultando Mercados Internacionales...")
    
    # Tickers: ZW=F (Trigo), ZC=F (Maíz), CL=F (Petróleo/Energía)
    tickers = {
        "Trigo (Chicago)": "ZW=F",
        "Maiz (Chicago)": "ZC=F",
        "Aceite Vegetal": "ZL=F"
    }
    
    registros = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    for nombre, ticker in tickers.items():
        try:
            data = yf.Ticker(ticker)
            precio = data.fast_info['last_price']
            
            registros.append({
                "fecha": fecha_hoy,
                "activo": nombre,
                "precio_cierre": precio,
                "moneda": "USD"
            })
            print(f"✅ {nombre}: {precio}")
        except Exception as e:
            print(f"❌ Error con {nombre}: {e}")

    if registros:
        supabase.table("mercados_internacionales").insert(registros).execute()
        print("📊 Datos de mercado guardados en Supabase.")

if __name__ == "__main__":
    obtener_datos_mercado()
