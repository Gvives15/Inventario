## Alcance y Reglas
- Objetivo: que la pantalla Productos permita buscar y registrar movimientos en 2 clicks, con UI clara y consistente.
- Estricto: no tocar modelos/commands/queries ni agregar features; sólo HTML/CSS/templating y micro‑copys.
- Contrato HTMX: mantener IDs `#products-table`, `#product-sheet`, `#movement-drawer`, `#alerts-list`, `#movements-list`, `#toast-stack` y el evento `inventory:changed`.
- Criterio de calidad: si se rompe refresh/swap, se revierte inmediatamente.

## Sistema Visual (tema claro)
- Aplicar tokens en `panel/src/web/templates/panel/base.html`:
  - Fondo gris muy claro, superficies blancas, texto primario casi negro, secundario gris medio.
  - Bordes 12px, espaciado 8/16/24/32, tipografía system 14–16px.
  - Estados: OK verde suave, Bajo ámbar, Sin stock rojo suave.
- Tablas:
  - Header claro semibold; separadores suaves; hover de fila; zebra opcional muy leve.
  - Altura de fila ~48px; columna Producto más ancha.
- Botones:
  - Primary único visible por pantalla; secundarios uniformes; danger reservado.
  - Estados: normal/hover/focus/disabled; loading con texto.

## Layout — App Shell
- Topbar minimal: Search global grande, botón `+ Movimiento` (primary), Perfil minimal.
- Content: `max-width 1200–1400px`, padding 24px.
- Mantener nav simple existente; sin íconos decorativos.

## Productos — Diseño exacto
- En `panel/src/web/templates/panel/products.html`:
  - Título “Productos”.
  - Barra de acciones: input búsqueda grande “Buscar por nombre o código…”, botón primary “+ Movimiento”.
  - Fila de chips: OK/Bajo/Sin stock + link “Limpiar filtros”.
  - Tabla ocupa el resto; columnas: Código | Producto | Stock (+ badge) | Mínimo | Vence | Últ. mov. | Acciones.
- En `panel/src/web/templates/panel/partials/_products_table.html`:
  - Unificar estilo de badges (altura 24–28px, padding 6–10px, borde suave).
  - Acciones finales con 3 botones compactos idénticos: Entrada, Salida, Ajuste.
  - Estados vacíos/error: mensaje claro y CTA “Limpiar filtros”.

## Drawer Movimiento — UX minuciosa
- En `panel/src/web/templates/panel/partials/_movement_drawer.html`:
  - Ancho 420–520px, backdrop visible, scroll interno.
  - Título “Registrar movimiento”; subtítulo contextual según tipo.
  - Tipo: editable sólo si viene de topbar; si viene de fila/sheet, mostrar badge bloqueado.
  - Producto: bloqueado si preseleccionado; si no, buscador/select “Buscar producto…”.
  - Cantidad (input grande); Motivo visible y requerido en Salida/Ajuste (Entrada opcional/oculto).
  - Footer sticky: Cancelar (secondary) + Continuar (primary).
  - Validaciones UI (sin dominio): cantidad > 0; motivo obligatorio en salida/ajuste; mensajes debajo del campo.
- Confirmación en `panel/src/web/templates/panel/partials/_movement_confirm.html`:
  - Resumen: “Vas a registrar: [TIPO] [CANTIDAD] — [PRODUCTO]”.
  - Botones: Volver (secondary) / Confirmar (primary, con estado loading).
  - En éxito: Toast “Movimiento registrado”, disparar `HX-Trigger: inventory:changed`, cerrar drawer (o limpiar si existe registrar‑y‑continuar).
  - En error: no cerrar; bloque de error y opción “Reintentar”.

## Product Sheet — Detalle mínimo
- En `panel/src/web/templates/panel/partials/_product_sheet.html`:
  - Ancho 520–640px; header con nombre/código/badges/botones Entrada/Salida/Ajuste.
  - Sección Estado: stock, mínimo, vence, último movimiento.
  - Sección Movimientos recientes (10–20) con tabla clara; sin tabs extra.

## Accesibilidad y Micro‑copys
- Focus visible en inputs/botones; contraste suficiente.
- Copys estándar: `+ Movimiento`, `Entrada/Salida/Ajuste`, `Continuar`, `Confirmar`, `Cancelar`, `Volver`, `Reintentar`, `Limpiar filtros`.
- Placeholders y errores:
  - “Buscar por nombre o código…”, “Buscar producto…”, “Ej: Reposición proveedor / Diferencia conteo”.
  - “Ingresá una cantidad mayor a 0.”, “El motivo es obligatorio para Salida/Ajuste.”

## HTMX — Contrato intacto
- Mantener triggers/targets exactos:
  - `#products-table`, `#product-sheet`, `#movement-drawer`, `#alerts-list`, `#movements-list`, `#toast-stack`.
  - Confirmación de movimientos emite `HX-Trigger: inventory:changed`.
  - Refrescar automáticamente listas y sheet si abiertos.

## Pruebas de Usabilidad (U1–U5) — Evidencia
- U1 Entendibilidad: debe describirse en 1 frase “buscar producto y registrar movimiento”.
- U2 Encontrar: búsqueda obvia y funcional.
- U3 Accionar: Entrada en 2 pasos (continuar/confirmar) sin dudas.
- U4 Estados: identificar 3 badges distintos claramente.
- U5 Drawer/Sheet: abrir/cerrar sin romper scroll ni layout.
- STOP: si falla U1–U3, corregir UI antes de cualquier otra cosa.

## Archivos a tocar (solo UI)
- `panel/src/web/templates/panel/base.html` (tokens, tabla, topbar, modal styling)
- `panel/src/web/templates/panel/products.html` (layout y acciones)
- `panel/src/web/templates/panel/partials/_products_table.html` (badges y acciones)
- `panel/src/web/templates/panel/partials/_movement_drawer.html` (form y validaciones UI)
- `panel/src/web/templates/panel/partials/_movement_confirm.html` (resumen y estados)
- `panel/src/web/templates/panel/partials/_product_sheet.html` (estructura mínima)
- `panel/src/web/templates/panel/alerts.html` y `.../_alerts_tab.html` (consistencia visual)
- `panel/src/web/templates/panel/movements.html` y `.../_movements_list.html` (consistencia visual)

## Entregable Final
- Lista de archivos UI tocados; capturas de Productos, Drawer, Confirmación y Sheet.
- Resultado U1–U5 con PASS/FAIL y notas.
- Confirmación de que no se tocó dominio ni se agregaron extras.

¿Confirmo y procedo con estos cambios de UI/UX estrictos manteniendo el contrato HTMX y sin tocar dominio?