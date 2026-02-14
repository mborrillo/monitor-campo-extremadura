import os
from supabase import create_client, Client
from datetime import datetime
import re
import sys

# 1. Capturamos variables RAW (sin limpiar aún) SUPABASE_URL SUPABASE_KEY
url_raw = os.environ.get("https://zzucvsremavkikecsptg.supabase.co")
key_raw = os.environ.get("sb_publishable_bnh1EYxSi_Omwtm-THae7A_lcCldwDY")

# 2. DEBUG EXTREMO: Ver EXACTAMENTE qué llega
print("=" * 70)
print("🔍 DEBUG EXTREMO - ANÁLISIS BYTE POR BYTE")
print("=" * 70)
print(f"URL RAW (repr): {repr(url_raw)}")
print(f"URL RAW (bytes): {url_raw.encode('utf-8')}")
print(f"KEY RAW (primeros 30 chars repr): {repr(key_raw[:30])}")
print(f"Versión Python: {sys.version}")

# 3. Mostrar versión de supabase
try:
    import supabase
    print(f"Versión supabase: {supabase.__version__ if hasattr(supabase, '__version__') else 'No disponible'}")
except:
    print("⚠️ No se pudo determinar versión de supabase")

# 4. Limpiar variables
url = url_raw.strip().strip('"').strip("'").strip()
key = key_raw.strip().strip('"').strip("'").strip()

# 5. DEBUG: Mostrar después de limpiar
print("\n" + "=" * 70)
print("📋 DESPUÉS DE LIMPIAR")
print("=" * 70)
print(f"URL limpia: {url}")
print(f"Longitud URL: {len(url)} caracteres")
print(f"KEY limpia (primeros 30): {key[:30]}...")
print(f"Longitud KEY: {len(key)} caracteres")

# 3. Verificación de seguridad
if not url or url == "None":
    print("❌ ERROR: La URL de Supabase no llega desde GitHub Secrets.")
    print("👉 Verifica que SUPABASE_URL esté configurado en GitHub Secrets")
    exit(1)

if not key or key == "None":
    print("❌ ERROR: La KEY de Supabase no llega desde GitHub Secrets.")
    print("👉 Verifica que SUPABASE_KEY esté configurado en GitHub Secrets")
    exit(1)

# 4. Validar formato de URL
url_pattern = re.compile(r'^https://[a-zA-Z0-9-]+\.supabase\.co$')
if not url_pattern.match(url):
    print("❌ ERROR: Formato de URL inválido")
    print(f"   URL recibida: '{url}'")
    print("   ✅ Formato correcto: https://tuproyecto.supabase.co")
    print("   ❌ NO incluyas: /rest/v1, espacios, comillas extra, barras finales")
    print("\n📋 PASOS PARA CORREGIR:")
    print("   1. Ve a tu proyecto en Supabase")
    print("   2. Settings → API → Project URL")
    print("   3. Copia SOLO la URL base (ejemplo: https://abcdefg.supabase.co)")
    print("   4. Ve a GitHub → Settings → Secrets → Edita SUPABASE_URL")
    print("   5. Pega la URL SIN espacios ni comillas")
    exit(1)

# 5. Inicialización del cliente con MÚLTIPLES INTENTOS
print("\n" + "=" * 70)
print("🔌 INTENTANDO CONEXIÓN A SUPABASE")
print("=" * 70)

# INTENTO 1: Método estándar
print("\n🔹 INTENTO 1: Método estándar")
try:
    supabase: Client = create_client(url, key)
    print("✅ ÉXITO con método estándar")
except Exception as e:
    print(f"❌ Falló método estándar: {e}")
    print(f"   Tipo de error: {type(e).__name__}")
    
    # INTENTO 2: Asegurar que termine con .supabase.co
    print("\n🔹 INTENTO 2: Verificar y corregir formato")
    if not url.endswith('.supabase.co'):
        print(f"   ⚠️ URL no termina en .supabase.co, intentando limpiar...")
        # Extraer solo la parte base
        import re
        match = re.search(r'(https://[a-zA-Z0-9-]+\.supabase\.co)', url)
        if match:
            url_clean = match.group(1)
            print(f"   URL corregida: {url_clean}")
            try:
                supabase: Client = create_client(url_clean, key)
                print("✅ ÉXITO con URL corregida")
                url = url_clean  # Actualizar para uso posterior
            except Exception as e2:
                print(f"❌ Falló con URL corregida: {e2}")
                
                # INTENTO 3: Modo debugging de supabase
                print("\n🔹 INTENTO 3: Intentar con opciones alternativas")
                try:
                    from supabase import Client as SupabaseClient
                    from supabase._sync.client import SyncClient
                    supabase = SyncClient(url, key)
                    print("✅ ÉXITO con SyncClient directo")
                except Exception as e3:
                    print(f"❌ FALLÓ TODO: {e3}")
                    print("\n" + "=" * 70)
                    print("💥 ERROR CRÍTICO - INFORMACIÓN PARA DEBUGGING")
                    print("=" * 70)
                    print(f"URL que está causando problema: '{url}'")
                    print(f"Caracteres de la URL: {[c for c in url]}")
                    print(f"URL es string?: {isinstance(url, str)}")
                    print(f"KEY es string?: {isinstance(key, str)}")
                    print("\n📋 PASOS SIGUIENTES:")
                    print("1. Copia la salida completa de este log")
                    print("2. Verifica en Supabase Settings → API que tu URL sea exactamente:")
                    print("   https://[tu-proyecto].supabase.co")
                    print("3. Verifica que en GitHub Secrets no haya espacios ni caracteres raros")
                    exit(1)
    else:
        print(f"❌ Error inesperado: {e}")
        print(f"   La URL parece correcta: {url}")
        print(f"   Pero supabase la rechaza")
        exit(1)

print("=" * 70)

def obtener_precios_multi_sector():
    print(f"🚀 Iniciando reporte: {datetime.now().strftime('%d/%m/%Y')}")
    
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
        # Inserción masiva
        res = supabase.table("precios_agricolas").insert(registros_totales).execute()
        print(f"✅ Éxito: {len(res.data)} registros insertados en el historial.")
    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")

if __name__ == "__main__":
    obtener_precios_multi_sector()


