# 🚜 Monitor AgroTech Extremadura
> Plataforma de Inteligencia de Datos para el sector agroindustrial.

## 🌟 Propuesta de Valor
Este sistema automatiza la captura y análisis de datos críticos para la toma de decisiones en el campo extremeño, integrando precios de mercado, meteorología de precisión y costes energéticos.

## 📊 Arquitectura del Ecosistema
1. **Ingesta (Python):** Scripts automáticos que consultan APIs oficiales (AEMET, REE, Lonjas).
2. **Cerebro (Supabase/PostgreSQL):** Vistas SQL que procesan recomendaciones en tiempo real (Asesor de riego, salud sectorial).
3. **Automatización (GitHub Actions):** Flujos de trabajo que mantienen el sistema vivo 24/7 sin intervención humana.

## 🛠️ Vistas de Negocio Implementadas
- **v_asesor_operaciones:** Recomendaciones de riego y tratamiento fitosanitario.
- **v_comparativa_mercados:** Arbitraje dinámico entre Lonjas locales y Chicago/Euronext (USD/EUR normalizado).
- **v_salud_sectores:** Monitorización macro de la tendencia de precios por sectores.

## 🚀 Próximos Pasos
- Integración de Frontend en Lovable.
- Sistema de alertas Push vía WhatsApp/Telegram.
