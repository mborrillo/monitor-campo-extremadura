# 📘 Manual de Interpretación de Umbrales: AgroTech Extremadura

Este manual explica la lógica detrás de cada recomendación emitida por el sistema. Los umbrales no son arbitrarios; son el resultado de cruzar la agronomía de precisión con la optimización financiera.

---

## 1. Gestión de Energía (El Umbral del Beneficio)

El coste de la luz es el principal factor que erosiona el margen neto en el regadío.

| Umbral (€/kWh) | Estado (`estado_costo`) | Recomendación del sistema | Justificación técnica |
| :--- | :--- | :--- | :--- |
| **< 0.10** | **BAJO** | **Riego recomendado** | Maximiza el margen. Momento de llenar depósitos o regar sectores de alta demanda hídrica. |
| **0.10 – 0.15** | **NORMAL** | **Consumo moderado permitido** | Coste asumible. Se permite el riego si la necesidad hídrica del cultivo es urgente. |
| **> 0.15** | **ALTO** | **Posponer consumo intensivo** | El coste de bombeo por m³ reduce el beneficio operativo un 30–50%. Evitar salvo emergencia. |

El Panel de Decisión Diaria traduce estos tres estados en un semáforo visible (🟢 / 🟡 / 🔴) con una recomendación textual accionable. La Calculadora de Ahorro permite al agricultor introducir la potencia de su bomba (en **kW**) y las horas de riego previstas para obtener el coste exacto en cada franja horaria del día.

> **Nota:** En Extremadura, con temperaturas estivales elevadas, regar en horas de precio alto no solo es costoso sino ineficiente por la evapotranspiración.

---

## 2. Tratamientos Fitosanitarios (La Regla de la Eficacia)

Fumigar fuera de estos umbrales es, literalmente, tirar producto al suelo o al aire.

- **Temperatura (10 °C – 25 °C):**
  - *Por debajo de 10 °C:* La planta cierra sus estomas o ralentiza su metabolismo. El producto no se absorbe y se lava con el rocío.
  - *Por encima de 28–30 °C:* El producto se evapora antes de tocar la hoja o puede causar quemaduras (fitotoxicidad) al reaccionar con el calor.

- **Viento (< 15 km/h):**
  Es el límite legal y técnico para evitar la deriva. Por encima de 20 km/h, hasta el 40 % del tratamiento no llega al objetivo, contaminando parcelas colindantes y representando pérdida económica directa.

- **Humedad relativa (> 50 %):**
  Una humedad baja reseca la gota demasiado rápido. Mantener el umbral sobre el 50 % asegura que el producto permanezca en estado líquido el tiempo suficiente para ser absorbido por la planta.

---

## 3. Arbitraje de Mercados (El Umbral de Negociación)

¿Vender ahora o esperar? El sistema usa el **Diferencial de Arbitraje** y la clasificación DIRECTO/PROXY.

### Mercado Directo (Trigo, Maíz)
Los precios internacionales son comparables en unidad (€/kg) con los de la lonja local, previa conversión desde los futuros de Chicago usando el tipo de cambio EUR/USD del día.

$$Diferencial = Precio_{Local} - Precio_{Internacional\ (€/kg)}$$

| Diferencial | `zona_arbitraje` | Recomendación |
| :--- | :--- | :--- |
| **> +5 %** sobre internacional | **FAVORABLE** | El mercado local paga más que el global. Momento de venta. |
| **±2 %** | **EQUILIBRADO** | Precio alineado con el mercado. Venta normal según liquidez. |
| **< –2 %** | **DESFAVORABLE** | Alerta: posible saturación local o falta de compradores. Retener si es posible. |

### Mercado Proxy (Aceites, Ganadería)
Los activos internacionales de referencia (Aceite de Soja, Ganado Vivo, Ganado Feeder) no son equivalentes en precio al producto local, por lo que no se comparan en valor absoluto. En su lugar, el sistema compara la **dirección de la variación semanal** (%).

| Condición | `zona_arbitraje` | Interpretación |
| :--- | :--- | :--- |
| Variación local y global en el **mismo sentido** | **ACOMPAÑANDO** | El precio local se mueve en línea con la tendencia global. |
| **Signos opuestos** con ambas variaciones distintas de cero | **DIVERGIENDO** | Desacoplamiento: el precio local va en dirección contraria al mercado de referencia. Señal de alerta. |
| Alguna variación es cero o no disponible | **NEUTRO** | Sin tendencia clara. |

---

## 4. Salud del Sector (Indicador Semafórico)

La vista `v_salud_sectores` agrega la tendencia semanal de todos los productos de cada sector y calcula el porcentaje al alza.

| `pct_alza` | `estado_mercado` | Interpretación |
| :--- | :--- | :--- |
| **≥ 80 %** de productos al alza o estables | 🟢 **ÓPTIMO** | Sector en buen momento. |
| **≥ 50 %** | 🟡 **ATENCIÓN** | Volatilidad detectada. Seguimiento recomendado. |
| **< 50 %** | 🔴 **ALERTA** | Caída generalizada. Momento de activar coberturas o buscar ayudas sectoriales. |

---

## 5. Estado de Estaciones (Mapa de Operaciones)

La vista `v_mapa_operaciones` combina clima actual y precio energético para emitir un estado operativo por estación.

| Estado | Condiciones | Acción recomendada |
| :--- | :--- | :--- |
| 🟢 **Óptimo** | Temperatura 10–25 °C, viento < 15 km/h, precio energía ≤ 0.15 €/kWh | Riego y tratamientos viables. |
| 🟡 **Precaución** | Algún parámetro en zona límite | Evaluar antes de actuar. |
| 🔴 **Crítico** | Temperatura fuera de rango, viento > 20 km/h, o precio > 0.15 €/kWh | Posponer operaciones de coste elevado. |

---

## ¿Por qué confiar en estos números?

A diferencia de un asesor tradicional que usa la intuición, AgroTech utiliza datos en tiempo real de la AEMET (clima), REE (precio PVPC horario) y lonjas de referencia (precios locales), cruzados con futuros internacionales de Chicago convertidos a €/kg. El sistema aplica estos umbrales de forma consistente en todas las vistas: si el Mapa dice que es caro regar a 0.15 €/kWh, la clasificación de energía también lo dice. La coherencia interna es parte del diseño.
