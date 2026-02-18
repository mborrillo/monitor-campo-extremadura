import yfinance as yf
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_mercados():
    print("📈 Consultando Mercados Internacionales (Chicago/NY/ICE)...")
    
    # Tickers seleccionados por relevancia para Extremadura
    activos = {
        "Trigo": {"ticker": "ZW=F", "cat": "Cereal"},
        "Maiz": {"ticker": "ZC=F", "cat": "Cereal"},
        "Soja": {"ticker": "ZS=F", "cat": "Cereal"},
        "Arroz": {"ticker": "ZR=F", "cat": "Cereal"},
        "Aceite_Soja": {"ticker": "ZL=F", "cat": "Grasas"},
        "Ganado_Vivo": {"ticker": "LE=F", "cat": "Ganaderia"},
        "Ganado_Feeder": {"ticker": "GF=F", "cat": "Ganaderia"},
        "Gas_Natural": {"ticker": "NG=F", "cat": "Energia_Agro"},
        "Brent": {"ticker": "BZ=F", "cat": "Energia_Agro"},
        "Euro_Dolar": {"ticker": "EURUSD=X", "cat": "Divisa"}
    }

    registros = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    for nombre, info in activos.items():
        try:
            print(f"→ Analizando {nombre}...")
            ticket = yf.Ticker(info['ticker'])
            hist = ticket.history(period="2d") # Pedimos 2 días para calcular la variación
            
            if len(hist) >= 1:
                ultimo_cierre = hist['Close'].iloc[-1]
                precio_ant = hist['Close'].iloc[-2] if len(hist) > 1 else ultimo_cierre
                
                # Calcular variación porcentual
                variacion = ((ultimo_cierre - precio_ant) / precio_ant) * 100
                
                registros.append({
                    "fecha": fecha_hoy,
                    "activo": nombre,
                    "precio_cierre": round(ultimo_cierre, 2),
                    "variacion_p": round(variacion, 2),
                    "categoria": info['cat'],
                    "moneda": "USD" if "USD" in info['ticker'] or "=F" in info['ticker'] else "EUR"
                })
                print(f"  ✓ {nombre}: {round(ultimo_cierre, 2)} ({round(variacion, 2)}%)")
            else:
                print(f"  ⚠️ Sin datos recientes para {nombre}")

        except Exception as e:
            print(f"  ❌ Error en {nombre}: {e}")

    if registros:
        # IMPORTANTE: Asegúrate de tener un índice único en (fecha, activo) en Supabase
        supabase.table("mercados_internacionales").upsert(registros, on_conflict="fecha, activo").execute()
        print(f"\n✅ ¡Éxito! {len(registros)} activos actualizados.")
    else:
        print("\n❌ No se pudo recuperar ningún dato de mercado.")

if __name__ == "__main__":
    obtener_mercados()
