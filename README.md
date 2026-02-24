## 🚜 AgroTech Extremadura: Inteligencia de Mercados y Operaciones

AgroTech Extremadura es una plataforma de inteligencia de datos diseñada para transformar la toma de decisiones en el sector agropecuario. No es solo un panel de control; es un puente entre la realidad productiva de las parcelas extremeñas y los movimientos de los mercados globales.

## 💡 ¿Qué es y por qué existe esta herramienta?
En el modelo agrícola tradicional, el productor suele estar desconectado de los precios de Chicago o de la evolución horaria del mercado energético. AgroTech Extremadura democratiza el acceso a la información compleja, traduciéndola en acciones concretas.

El Diferencial: ¿Qué la hace única?
A diferencia de otras apps de clima, aquí vinculamos:

Clima Local Real: Datos directos de estaciones de la AEMET (Badajoz, Cáceres, Mérida).

Arbitraje de Mercados: Compara el precio de la Lonja local con los futuros internacionales de Chicago, permitiendo detectar cuándo el precio local está infravalorado.

Eficiencia Energética: Cruza el precio de la luz (PVPC) con la necesidad de riego para optimizar costes.

¿Para quién es?
Productores Individuales: Optimización de riego y tratamientos.

Gerentes de Cooperativas: Visión estratégica para la comercialización de cosechas.

Empresas de Seguros Agrarios: Monitorización de riesgos climáticos extremos.

## 🏛️ Arquitectura de Datos (Supabase SQL)
El cerebro de la herramienta reside en una base de datos PostgreSQL, estructurada para ser escalable y rápida.

Tablas (Donde guardamos los datos brutos)
Vistas SQL (La Inteligencia del Sistema)
v_asesor_operaciones: Traduce el viento y la lluvia en un semáforo de "Apto/No Apto" para pulverizar o regar.

v_comparativa_mercados: Realiza el cálculo de arbitraje (diferencia de precio local vs internacional) convertido a €/kg.

v_salud_sectores: Agrupa los productos para decir si el sector (Cereales, Aceites, etc.) está en expansión o contracción.

v_alertas_clima_extrema: Filtra automáticamente temperaturas críticas para prevenir heladas o golpes de calor.

## ⚙️ Estructura del Software (Python)
Los scripts actúan como "mayordomos digitales" que trabajan 24/7 de forma automatizada mediante GitHub Actions.

clima_monitor.py: Conecta con la API de AEMET. Su lógica "blinda" el sistema contra fallos de conexión, asegurando que siempre tengamos el clima de Badajoz, Cáceres y Mérida actualizado.

mercado_monitor.py: Extrae datos de Yahoo Finance. Realiza una limpieza de "anomalías" para evitar que un error en el mercado internacional ensucie nuestros informes.

energia_monitor.py: Consulta el precio de la luz en tiempo real. Es el motor detrás del ahorro en los costes de riego.

monitor_agrotech_v1.py: El orquestador que sincroniza la Lonja local con el resto de parámetros.

## 📚 Glosario para el Productor
Para entender esta herramienta, usamos conceptos que ya conoces, pero con un toque tecnológico:

Arbitraje: Es la diferencia de precio entre dos mercados. Si el Trigo en Chicago sube pero en Extremadura se mantiene, hay una oportunidad de negociación.

Proxy Market (Mercado de Referencia): Cuando un producto no cotiza en bolsa (como el Aceite de Oliva), usamos uno similar (Aceite de Soja) para entender hacia dónde va el viento del mercado.

ETL (Extraer, Transformar, Limpiar): Es lo que hacen nuestros scripts: recogen datos sucios de internet y te los entregan limpios y útiles.

Regadío Inteligente: Decidir no regar hoy porque la luz está cara y mañana se prevé lluvia según la estación local.

NOTA: 
El sistema se actualizará automáticamente cada mañana.

## 🏷️ Hashtags & Referencias
#AgroTech #Extremadura #SmartFarming #BigData #Agricultura40 #OpenData #Python #Supabase #AEMET #MercadoDeFuturos #LonjaExtremadura #InnovacionRural
