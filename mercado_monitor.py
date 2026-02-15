import yfinance as yf
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_datos_mercado():
    print("📈 Consultando Panel de Mercados Internacionales Ampliado...")
    
    # Mapeo de Tickers estratégicos
    tickers = {
        "Trigo (Chicago)": "ZW=F",
        "Maiz (Chicago)": "ZC=F",
        "Aceite de Soja": "ZL=F",
        "Cerdo Magro (Futuros)": "HE=F",
        "Gasoleo (Diesel)": "HO=F",
        "Gas Natural (Fertilizantes)": "NG=F",
        "Euro/Dolar": "EURUSD=X"
    }
    
    registros = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    for nombre, ticker in tickers.items():
        try:
            data = yf.Ticker(ticker)
            # Intentamos obtener el precio de cierre o el último precio disponible
            precio = data.fast_info.get('last_price')
            
            if precio:
                registros.append({
                    "fecha": fecha_hoy,
                    "activo": nombre,
                    "precio_cierre": round(float(precio), 4),
                    "moneda": "USD" if "EURUSD" not in ticker else "Ratio",
                })
                print(f"✅ {nombre}: {precio}")
        except Exception as e:
            print(f"❌ Error con {nombre}: {e}")

    if registros:
        try:
            supabase.table("mercados_internacionales").upsert(registros).execute()
            print(f"📊 ¡Éxito! {len(registros)} activos internacionales actualizados.")
        except Exception as e:
            print(f"❌ Error al guardar en Supabase: {e}")

if __name__ == "__main__":
    obtener_datos_mercado()
