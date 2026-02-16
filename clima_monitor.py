import os
import requests
from supabase import create_client, Client
from datetime import datetime, timedelta
import sys

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG" 
AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2OGJvcnJpc21hckBnbWFpbC5jb20iLCJqdGkiOiI1YzRjYzlkZC04OTI0LTQzZjgtOTI1OC1hZWZiZjRhOWIzNGMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc3MTA4MjI3MSwidXNlcklkIjoiNWM0Y2M5ZGQtODkyNC00M2Y4LTkyNTgtYWVmYmY0YTliMzRjIiwicm9sZSI6IiJ9.EQqSYmGFYaCQvhzPv2gxYHkwa1Zyqr9sDLRCG8xLaV4"

# Inicializar cliente Supabase
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ Conexión con Supabase establecida")
except Exception as e:
    print(f"✗ Error al conectar con Supabase: {e}")
    sys.exit(1)

def obtener_clima_extremadura():
    """
    Obtiene datos climáticos de AEMET para Badajoz y Cáceres
    y los almacena en Supabase
    """
    print(f"=== Monitor de Clima - {datetime.now().strftime('%d/%m/%Y %H:%M')} ===")
    
    # Estaciones meteorológicas de Extremadura
    estaciones = {
        "Badajoz": "4452",
        "Caceres": "3431",
        "Merida": "4410",
        "Plasencia": "3519",
        "Don Benito": "4358",
        "Almendralejo": "4446",
        "Zafra": "4427",
        "Navalmoral de la Mata": "3411",
        "Trujillo": "3441",
        "Hervas": "3469"
    }
    
    headers = {'api_key': AEMET_API_KEY}
    datos_procesados = {}
    
    for ciudad, id_estacion in estaciones.items():
        print(f"\n→ Consultando estación {ciudad} (ID: {id_estacion})...")
        
        url = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{id_estacion}"
        
        try:
            # Primera petición a AEMET
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            res_json = response.json()
            
            if res_json.get('estado') == 200:
                # Obtener URL de descarga de datos
                url_descarga = res_json.get('datos')
                
                if not url_descarga:
                    print(f"  ✗ No se recibió URL de descarga")
                    continue
                
                # Segunda petición para obtener datos reales
                datos_response = requests.get(url_descarga, timeout=10)
                datos_response.raise_for_status()
                datos = datos_response.json()
                
                print(f"  ✓ Recibidas {len(datos)} lecturas")
                
                # Procesar datos - agrupar por fecha para obtener máx/mín del día
                for lectura in datos:
                    fecha_completa = lectura.get('fint')  # Fecha fin de intervalo
                    if not fecha_completa:
                        continue
                    
                    # Extraer solo la fecha (sin hora)
                    fecha_str = fecha_completa.split('T')[0]
                    
                    # Crear clave única por ciudad y fecha
                    clave = f"{ciudad}_{fecha_str}"
                    
                    # Inicializar si no existe
                    if clave not in datos_procesados:
                        datos_procesados[clave] = {
                            "fecha": fecha_str,
                            "estacion": ciudad,
                            "temp_max": None,
                            "temp_min": None,
                            "precipitacion": 0.0
                        }
                    
                    # Actualizar temperatura máxima
                    temp_actual = lectura.get('ta')
                    if temp_actual is not None:
                        temp_actual = float(temp_actual)
                        if datos_procesados[clave]["temp_max"] is None:
                            datos_procesados[clave]["temp_max"] = temp_actual
                        else:
                            datos_procesados[clave]["temp_max"] = max(
                                datos_procesados[clave]["temp_max"], 
                                temp_actual
                            )
                        
                        # Actualizar temperatura mínima
                        if datos_procesados[clave]["temp_min"] is None:
                            datos_procesados[clave]["temp_min"] = temp_actual
                        else:
                            datos_procesados[clave]["temp_min"] = min(
                                datos_procesados[clave]["temp_min"], 
                                temp_actual
                            )
                    
                    # Acumular precipitación
                    precip = lectura.get('prec')
                    if precip is not None and precip != 'Ip':  # 'Ip' = inapreciable
                        try:
                            datos_procesados[clave]["precipitacion"] += float(precip)
                        except (ValueError, TypeError):
                            pass
            
            elif res_json.get('estado') == 404:
                print(f"  ✗ Estación no encontrada")
            elif res_json.get('estado') == 429:
                print(f"  ✗ Límite de peticiones excedido")
            else:
                print(f"  ✗ AEMET respondió con estado {res_json.get('estado')}: {res_json.get('descripcion')}")
        
        except requests.exceptions.Timeout:
            print(f"  ✗ Timeout al consultar {ciudad}")
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error de red en {ciudad}: {e}")
        except Exception as e:
            print(f"  ✗ Error inesperado en {ciudad}: {e}")
    
    # Insertar datos en Supabase
    # Insertar datos en Supabase
        if datos_procesados:
            registros = list(datos_procesados.values())
            print(f"\n→ Procesando {len(registros)} registros diarios únicos...")
            
            try:
                # Forzamos el upsert sobre la combinación única de fecha y estación
                result = supabase.table("datos_clima").upsert(
                    registros,
                    on_conflict="fecha, estacion"
                ).execute()
                
                if result.data:
                    print(f"✓ Éxito: {len(result.data)} registros procesados en Supabase")
                else:
                    print("⚠ Los datos ya estaban actualizados (sin cambios).")
            
            except Exception as e:
                print(f"✗ Error al insertar en Supabase: {e}")
                # No cerramos con sys.exit(1) para que no rompa el flujo de los otros scripts
    else:
        print("\n✗ No se obtuvieron datos válidos de AEMET")
        sys.exit(1)
    
    print("\n=== Monitor completado ===")

if __name__ == "__main__":
    try:
        obtener_clima_extremadura()
    except KeyboardInterrupt:
        print("\n\n✗ Ejecución cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error fatal: {e}")
        # sys.exit(1)
