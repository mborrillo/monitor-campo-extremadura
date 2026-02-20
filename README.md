## 🚀 Extremadura Agrotech: Motor de Inteligencia Agraria
Ecosistema automatizado de captura, normalización y procesamiento de datos críticos para el sector agroindustrial de Extremadura.

🛠️ Stack Tecnológico
Base de Datos: Supabase (PostgreSQL) con lógica de negocio integrada en vistas SQL.

Backend / Ingesta: Python 3.9 (Requests, Supabase-py).

Automatización: GitHub Actions (Programación horaria/CRON).

Fuentes de Datos: AEMET (Clima), REE/PVPC (Energía), Lonjas Locales (Precios), Yahoo Finance (Mercados Globales).

# 🏗️ Arquitectura de Datos
El sistema se basa en una arquitectura de 3 capas:

Capa de Ingesta (Raw Data): Scripts que limpian y suben datos crudos evitando duplicados mediante upsert y claves compuestas (fecha, estacion, fecha, producto).

Capa de Normalización (Mapping): Tabla mapeo_productos que actúa como traductor entre nombres de lonja locales y estándares internacionales.

Capa de Inteligencia (Business Views): Vistas SQL que transforman datos estáticos en recomendaciones activas (ej. v_asesor_operaciones).

# 🔧 Componentes Críticos
Normalización Monetaria: La vista v_comparativa_mercados realiza conversiones dinámicas de USD/Bushel a EUR/Kg usando el tipo de cambio Euro_Dolar del día.

Análisis Climático: Procesamiento de series temporales de 24h para extraer temperaturas Máximas y Mínimas reales, superando las limitaciones de lecturas instantáneas.
