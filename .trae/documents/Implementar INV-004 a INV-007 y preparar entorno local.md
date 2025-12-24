## Alcance
- Implementar pendientes: INV-004 (Quick Actions por SKU), INV-005 (integridad y choices), INV-006 (Movimientos globales con filtros), INV-007 (UI errores + LOGGING).
- Preparar entorno local de desarrollo y validación completa antes de migrar al VPS.

## Cambios por tarea
### INV-004 — Quick Actions por SKU
- Agregar `normalize_sku(raw)` en `inventory/src/domain/rules.py` y reutilizar donde haga falta.
- Crear endpoints en `panel/src/web/urls.py` para acciones por SKU:
  - `actions/stock/entry-by-sku/`, `exit-by-sku/`, `adjust-to-count-by-sku/`.
- Vistas en `panel/src/web/views/actions_stock_view.py` (reusar patrón actual):
  - Resolver `sku` → `Product` vía `normalize_sku`, manejar errores (404 si no existe) y razones obligatorias.
- UI HTMX: extender `panel/src/web/templates/panel/partials/_quick_actions.html` con inputs de `sku` y toasts (OK/ERROR) apuntando a los nuevos endpoints.

### INV-005 — Integridad
- SKU normalizado: aplicar `normalize_sku` en:
  - Importadores CSV ya planificados (productos y stock inicial).
  - Create/Update de producto (API y panel): normalizar antes de persistir.
- Reason obligatorio: asegurar en comandos `record_entry_cmd.py`, `record_exit_cmd.py`, `adjust_to_count_cmd.py` usando `require_reason(reason)`.
- `movement_type` con choices:
  - Definir enum/choices en `inventory/src/infrastructure/orm/models.py` para `StockMovement.movement_type` (ENTRY, EXIT, ADJUST_COUNT, ADJUST_DELTA).
  - Actualizar comandos para usar constantes de elección.
  - Crear migración de cambio de campo si es necesario.

### INV-006 — Movimientos Globales
- URLs: `panel/src/web/urls.py`
  - `movements/` (página) y parciales HTMX `movements/partials/list/` con filtros.
- Vistas: `panel/src/web/views/movements_view.py`
  - Filtros: rango (hoy/7d), `sku` (normalizado), `movement_type`.
  - Paginación simple, render parcial para lista.
- Templates: `panel/src/web/templates/panel/movements.html` y `partials/_movements_list.html`.
- Query de aplicación: `inventory/src/application/queries/movements_q.py` para encapsular criterios.

### INV-007 — UI Errores + LOGGING
- Templates de error: `templates/403.html`, `404.html`, `500.html` con estilo del panel y mensajes consistentes.
- `LOGGING` mínimo en `config/settings.py`:
  - Consola `INFO` y canal `inventory.movements` para `StockMovement` (log en alta de movimientos críticos).
- Hook de logging en comandos de movimiento (emitir evento al crear movimiento).
- Toast HTMX en panel para mostrar errores de validación en formularios.

## Verificación local
- Migraciones: `python manage.py makemigrations` y `python manage.py migrate`.
- Tests:
  - Añadir casos a `inventory/tests.py`:
    - Normalización de SKU en create/update/import.
    - `require_reason` aplicado a entry/exit/adjust.
    - `movement_type` rechaza valores fuera de choices.
    - Lista de movimientos con filtros devuelve lo esperado.
- UI:
  - Probar `GET/POST /panel/imports/products/` y `/panel/imports/initial-stock/`.
  - Probar quick actions por SKU en dashboard.
  - Probar pantalla de movimientos y filtros HTMX.

## Entregables y archivos
- Dominio: `inventory/src/domain/rules.py` (agregar `normalize_sku`).
- ORM: `inventory/src/infrastructure/orm/models.py` (choices de `movement_type`).
- Aplicación: `inventory/src/application/commands/*` (reason obligatorio, uso de choices), `queries/movements_q.py`.
- Panel: nuevas vistas y templates (`movements`, quick actions por SKU), actualización de `urls.py`.
- Settings: `LOGGING` mínimo.
- Tests: actualizar `inventory/tests.py`.

## Despliegue local y VPS (posterior)
- Local: ejecutar servidor en desarrollo, validar UI/CLI/tests.
- VPS: preparar `gunicorn` + `systemd` + `nginx` (archivos de ejemplo a entregar tras validación local), sin dependencias de Vercel.

¿Confirmo y comienzo con estos cambios? 