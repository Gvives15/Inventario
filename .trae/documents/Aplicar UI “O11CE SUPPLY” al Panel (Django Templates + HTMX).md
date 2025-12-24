## Decisión de Base
- Elegir fondo gris carbón como default para legibilidad y look corporativo.

## Paleta y Tokens (en `panel/templates/panel/base.html`)
- Definir variables CSS en `:root`:
  - `--bg:#0f1114` (gris carbón)
  - `--surface:#15181d`
  - `--border:#23272e`
  - `--text:#ffffff`
  - `--muted:#9aa1a9`
  - `--brand:#157afe`
  - `--brand2:#29d3ff`
  - `--ok:#17a673`
  - `--bad:#d22`
- Incorporar utilidades y componentes:
  - `.container` ancho máx y padding
  - `.card` fondo, borde, radio, padding
  - `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-danger` (primary con gradiente `linear-gradient(90deg,var(--brand),var(--brand2))`)
  - `.input`, `.select`, `.textarea`
  - `.badge`, `.badge-entry`, `.badge-exit`, `.badge-adjust`
  - `.toast`, `.toast-ok`, `.toast-bad`, `.toast-info`
  - `.table`, `.table-zebra`, `.table-dense`
- Ajustar tipografía: una sans (e.g., `system-ui, Segoe UI, Arial`) con 4 tamaños (`.h1`, `.h2`, `.text`, `.meta`).

## Header Minimal (en `base.html`)
- Izquierda: logo chico (placeholder por ahora) + título.
- Derecha: links “Dashboard”, “Movimientos”, “Salir”.
- Estilos: fondo `var(--surface)`, borde inferior `var(--border)`, links con acento marca en hover.

## Dashboard (en `panel/templates/panel/dashboard.html` y parciales)
- Zona A — Métricas: tarjetas grandes en grilla, cada card con número grande (`.h1`), label `.meta`.
- Zona B — Acciones rápidas: 3 forms HTMX (ya existentes) con inputs `.input` grandes y botón `.btn-primary` con gradiente marca; etiqueta “Motivo (obligatorio)”.
- Zona C — Control: listas recientes/alertas en cards con `.table-dense`.

## Toasts (en `panel/templates/panel/partials/_toast.html`)
- Usar `.toast-ok`, `.toast-bad`, `.toast-info` (fondo suavizado con texto blanco). Mantener HTMX swap.

## Movimientos (en `movements.html` y `_movements_list.html`)
- Barra de filtros en una línea: rango (Hoy/7d), SKU, Tipo, botón `.btn-secondary` (o auto con HTMX actual).
- Tabla auditoría con columnas: Fecha, SKU, Tipo (badge), Delta (verde si +, rojo si -), Stock, Motivo, Usuario.
- Zebra suave, números alineados a la derecha, badges por tipo (`entry`, `exit`, `adjust_*`).

## Detalle de Producto (en `product_detail.html` y `_kardex.html`)
- Arriba: Nombre + SKU, Stock actual grande (`.h1`), mínimo y categoría como `.meta`.
- Abajo: Kardex con la misma tabla/badge que movimientos.

## Responsive
- Grilla: 2 columnas en desktop, 1 en mobile.
- Botones full-width en mobile (`.btn { width:100% }` bajo breakpoint).

## Errores de Formulario
- Mensajes humanos: “SKU no existe”, “Motivo es obligatorio”, “No hay stock suficiente”. Mostrar como `.toast-bad` y, si aplica, inline bajo input con `.meta` rojo suave.

## Cambios por Archivo
- `panel/templates/panel/base.html`: tokens, header, utilidades, contenedor.
- `panel/templates/panel/partials/_toast.html`: mapear niveles a clases.
- `panel/templates/panel/partials/_quick_actions.html`: aplicar `.input` y `.btn-primary` + copy “Motivo (obligatorio)”.
- `panel/templates/panel/movements.html`: barra de filtros con clases.
- `panel/templates/panel/partials/_movements_list.html`: tabla con badges y zebra, delta coloreado.
- `panel/templates/panel/product_detail.html`: cabecera de producto con stock grande.
- `panel/templates/panel/partials/_kardex.html`: reutilizar tabla/badge.

## Verificación
- Navegar Dashboard: métricas visibles, acciones rápidas operables en 10–15s.
- Movimientos: filtros en una línea, tabla clara, delta coloreado.
- Producto: stock actual grande + kardex consistente.
- Mobile: 1 columna y botones full width.

## Documentación
- `docs/IMPROVEMENTS.md`: agregar ticket “INV-UI-001 — O11CE Brand UI”.
- `README`: sección “UI Style Guide — O11CE” con paleta, componentes base y reglas.

## Nota de Marca
- Gradiente solo en CTAs y highlights; resto en azul marca sólido.
- Fondo gris carbón como default. Si deseas negro puro, los tokens permiten cambiar `--bg` y `--surface` fácilmente.