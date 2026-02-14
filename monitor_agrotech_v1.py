import os
from supabase import create_client, Client
from datetime import datetime
import re

# 1. Capturamos y limpiamos las variables (evita espacios invisibles y comillas)
url = os.environ.get("SUPABASE_URL", "").strip().strip('"').strip("'")
key = os.environ.get("SUPABASE_KEY", "").strip().strip('"').strip("'")

# 2. DEBUG: Mostrar información de las variables (SIN mostrar valores sensibles completos)
print("=" * 60)
print("🔍 DIAGNÓSTICO DE VARIABLES DE ENTORNO")
print("=" * 60)
print(f"URL recibida: {url[:30]}{'...' if len(url) > 30 else ''}")
print(f"Longitud URL: {len(url)} caracteres")
print(f"KEY recibida: {key[:20]}{'...' if len(key) > 20 else ''}")
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

# 5. Inicialización única del cliente
try:
    supabase: Client = create_client(url, key)
    print("✅ Conexión con Supabase establecida correctamente.")
    print("=" * 60)
except Exception as e:
    print(f"❌ Error crítico de conexión: {e}")
    print("\n📋 POSIBLES CAUSAS:")
    print("   - URL incorrecta (debe ser https://tuproyecto.supabase.co)")
    print("   - KEY incorrecta (revisa que sea la 'anon/public' key)")
    print("   - Problemas de red o permisos")
    exit(1)

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
