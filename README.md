# Dashboard de Indicadores Económicos de México

Panel interactivo de indicadores macroeconómicos de México, desarrollado por la **Dirección de Análisis de la Secretaría de Economía del Gobierno Federal**.

## 🔗 Ver el dashboard

> El sitio se publica automáticamente en: `https://<tu-usuario>.github.io/<nombre-del-repositorio>/`

---

## 📊 Indicadores incluidos

| Indicador | Fuente | Frecuencia |
|---|---|---|
| Producto Interno Bruto (PIB) | INEGI | Trimestral |
| PIB por Actividad Económica (Sectorial) | INEGI | Trimestral |
| Indicador Global de Actividad Económica (IGAE) | INEGI | Mensual |
| Indicador Mensual de Actividad Industrial (IMAI) | INEGI | Mensual |
| Consumo Privado | INEGI | Mensual |
| Inversión Extranjera Directa (IED) | RNIE – Secretaría de Economía | Trimestral |
| Tasa de Desocupación | INEGI (ENOE) | Mensual |
| INPC – Inflación General, Subyacente y No Subyacente | INEGI | Mensual |
| Balanza Comercial de Mercancías | INEGI | Mensual |

---

## 🔄 Cómo actualizar el dashboard

### Requisitos
- Cuenta de GitHub con acceso a este repositorio
- El archivo `Indicadores_macroeconómicos_de_México.xlsx` actualizado

### Pasos para actualizar

1. **Actualizar el Excel** con el nuevo dato publicado por INEGI/Banxico/SE
2. **Compartir el archivo** en el chat de Claude (claude.ai)
3. **Solicitar la regeneración** del dashboard: *"Actualiza el dashboard con este nuevo archivo"*
4. **Descargar el nuevo `index.html`** generado por Claude
5. **Subir a GitHub**:
   - Ir al repositorio en github.com
   - Clic en `index.html` → ícono de lápiz ✏️ (editar)
   - Seleccionar todo el contenido (Ctrl+A) y pegarlo con el nuevo
   - O bien: clic en **"Add file" → "Upload files"** y arrastrar el nuevo `index.html`
   - Escribir mensaje de commit: *"Actualización IGAE abril 2026"*
   - Clic en **"Commit changes"**
6. **Esperar 1–2 minutos** y la página se actualiza automáticamente

---

## 📅 Calendario de próximas publicaciones

| Fecha | Indicador | Período |
|---|---|---|
| 24 jun 2026 | INPC 1ª quincena | Junio 2026 |
| 25 jun 2026 | Política monetaria Banxico + Empleo (ENOE) | Mayo 2026 |
| 26 jun 2026 | Balanza Comercial | Mayo 2026 |
| Mediados ago 2026 | IED | 2T-2026 |
| Finales jul 2026 | IGAE | Mayo 2026 |

---

## 🛠️ Tecnologías utilizadas

- **Chart.js 4.4.1** — gráficas de series de tiempo
- **SheetJS (xlsx 0.18.5)** — exportación a Excel
- **IBM Plex Sans / IBM Plex Mono** — tipografía
- **HTML5 / CSS3 / JavaScript** — sin frameworks, archivo único autónomo

---

## 📋 Historial de actualizaciones

| Fecha | Cambio | Responsable |
|---|---|---|
| 23 jun 2026 | Actualización IGAE abril 2026 (revisión serie) | Dirección de Análisis |
| 23 jun 2026 | Versión inicial del dashboard | Dirección de Análisis |

---

*Secretaría de Economía — Gobierno Federal de México*
