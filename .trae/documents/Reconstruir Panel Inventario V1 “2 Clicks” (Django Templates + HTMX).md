## Alcance
- Construir Panel V1 con 4 pantallas (Productos, Alertas, Movimientos, Configuración) y 2 interacciones (Drawer Movimiento, Product Sheet).
- Usuarios gestionados solo en Django Admin; roles simples por Grupos de Django; `require_scope` valida scopes sin tocar dominio.

## Prohibiciones
- Sin dashboards/BI, gráficos, widgets extra, filtros avanzados, exportaciones, menús ocultos, tabs en Productos, refactors grandes, cambios en modelos/commands/queries, ni CRUD de usuarios en UI.

## Orden (no reordenar)
1. AppShell + tokens + componentes base
2. Rutas nuevas + vistas "vacías" que rendericen
3. Productos (page + tabla parcial + estados)
4. Drawer Movimiento (partial + confirm + wiring)
5. Product Sheet (partial + kardex breve)
6. Alertas (page + tabs partial)
7. Movimientos (adaptación mínima)
8. Contrato HTMX global + consistencia + accesibilidad + skeletons
9. Roles por grupo + `require_scope` (simple)
10. DoD (3 flujos + roles)

## Checkpoints
- Branch: `panel-v1-ui`.
- Commits por bloque: shell, urls+views, productos, drawer, sheet, alertas, movimientos, polish+htmx, roles, DoD.
- Contrato HTMX: fijar IDs y no cambiarlos.

## Contrato HTMX Global
- Targets fijos: `#products-table`, `#product-sheet`, `#movement-drawer`, `#alerts-list`, `#movements-list`, `#toast-stack`.
- Evento `inventory:changed` tras confirmar movimiento:
  - En Productos: recargar `#products-table`.
  - Si sheet abierto: recargar `#product-sheet`.
  - En Alertas: recargar `#alerts-list`.
- STOP: si movimiento no refresca UI, corregir antes de avanzar.

## 1) AppShell + Sistema Visual
- Sidebar: Productos, Alertas, Movimientos, Configuración (solo admin, link `/admin`).
- Topbar: Búsqueda global, `+ Movimiento` (abre drawer), Perfil.
- Tokens (tema claro): primario marca (CTAs), fondo claro, texto oscuro, estados verde/ámbar/rojo, bordes 12px, spacing 8/16/24/32, tipografía system.
- Componentes base: Button, SearchInput, FilterChips, Table, BadgeStatus, Drawer, Sheet, ConfirmDialog, Toast, Skeleton.
- STOP: componente nuevo por conveniencia → eliminar.

## 2) URLs + Views base
- Nuevas: `panel:products_page`, `panel:products_table_partial`, `panel:product_sheet_partial`, `panel:movement_drawer_partial`, `panel:movement_confirm_partial`, `panel:alerts_page`, `panel:alerts_list_partial`.
- Reusar: `panel:movements_page`, `panel:movements_list_partial`.
- Views vacías primero con `login_required` + `require_scope`.
- STOP: si no renderiza, no avanzar.

## 3) Productos
- `products.html`: header (título, search, `+ Movimiento`), chips (estado, pronto, almacén, categoría, limpiar), contenedor tabla.
- `_products_table.html`: estados `loading/empty/no results/error`.
- Contrato HTMX: search/chips/paginado actualizan solo `#products-table`.
- Tabla: Código | Producto | Stock(+badge) | Mínimo | Vence | Últ. mov. | Acciones. Acciones visibles (Entrada/Salida/Ajuste). Click en nombre abre sheet.
- `products_view.py`: lista/pagina con `list_products(...)`, calcula badges sin tocar dominio.
- STOP: si buscar+listar no es fluido, no avanzar.

## 4) Drawer Movimiento
- Parciales: `_movement_drawer.html`, `_movement_confirm.html`.
- Aperturas: fila, topbar, sheet.
- Form mínimo: Tipo, Producto, Cantidad, Almacén (si aplica), Motivo (obligatorio en salida/ajuste), Nota opcional.
- Validaciones UI: cantidad > 0; motivo requerido; advertencia visual si reduce fuerte.
- Wiring a `actions_stock_view.py` (`stock_entry_*`, `stock_exit_*`, `stock_adjust_to_count_*`).
- Errores: mostrar en drawer, botón Reintentar.
- Resultado: toast → `inventory:changed` → refresh según contrato.
- STOP: si no actualiza stock visible + feedback, no avanzar.

## 5) Product Sheet
- `_product_sheet.html`: Header (Nombre + código + badges + botones), Estado (stock/mínimo/vencimiento/últ. mov.), Movimientos recientes (10–20: fecha/tipo/cantidad/usuario/motivo).
- `product_sheet_partial`: producto + `list_movements_q` limitado; lazy load.
- STOP: si muestra más de lo definido, recortar.

## 6) Alertas
- `alerts.html` + `_alerts_tab.html` con tabs (Bajo stock/Sin stock/Por vencer). Lista con Producto, indicador, `Entrada`, `Ver` abre sheet.
- `alerts_list_partial`: reusa `dashboard.alerts_q` con paginado.
- STOP: si no permite entrada directa en 2 clicks, está mal.

## 7) Movimientos
- Adaptar a filtros mínimos (hoy/7/30; tipo; producto) y columnas: Fecha/hora | Producto | Tipo | Cantidad | Usuario | Motivo | Almacén (si aplica). Sin export/detalle.

## 8) Consistencia + Accesibilidad + Skeletons
- Unificación de botones, badges, espacios/bordes; focus visible; contraste; botones con texto; skeleton de tabla y sheet/drawer.

## 9) Roles por Grupo + require_scope
- Grupos: `admin`, `operador`, `auditor` (se crean/asignan en `/admin`).
- Scopes (6): `panel.read`, `inventory.read`, `inventory.write`, `alerts.read`, `movements.read`, `user.admin`.
- Asignación: admin (todos); operador (todos menos `user.admin`); auditor (`panel.read`, `inventory.read`, `alerts.read`, `movements.read`).
- Extender `panel/src/web/access/require_scope.py` (actualmente solo autentica) para validar `scope_name` por pertenencia a grupos, sin tocar dominio.
- STOP: si auditor puede registrar movimiento, corregir antes de DoD.

## 10) DoD — Pruebas Manuales
- Reposición: Productos → buscar → Entrada → Confirmar → stock actualizado + movimiento visible.
- Corrección: Productos → Ajuste (motivo obligatorio) → Confirmar → auditado (usuario + motivo).
- Alertas: Bajo stock → Entrada → Confirmar → resuelto sin navegar extra.
- Roles: Operador puede registrar; Auditor no; Admin accede Configuración (/admin) y gestiona usuarios/grupos.

## Entregables
- AppShell; Productos + tabla + estados; Drawer + confirm + errores; Product Sheet; Alertas; Movimientos; Contrato HTMX global; `require_scope` con roles por grupo; DoD pasando.