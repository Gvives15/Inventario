## [INV-001] - Setup V1 inicial y estructura de capas
Estado: Hecha
Versión objetivo: V1.x
Autor: IA
Fecha: 2025-12-24

Contexto:
Se inicializa proyecto Django + Ninja y estructura API-first según README.

Problema:
No existía proyecto ni estructura base.

Propuesta:
Crear proyecto, app `inventory`, capas `domain/application/infrastructure/api`, JWT, endpoints V1.

Impacto:
- domain: sin cambios de reglas
- application: commands y queries implementados
- infrastructure: modelos, repos y transacciones
- api: routers, schemas y auth

Riesgos:
Configuración JWT en dev usa SECRET_KEY si no hay clave dedicada.

Decisión:
Avanzar en V1 con HS256 y TTL por defecto.

Implementación (archivos tocados):
- config/api.py
- config/urls.py
- config/security/jwt_settings.py
- inventory/models.py
- inventory/src/**
- inventory/tests.py

Resultado:
API V1 operativa con endpoints de productos, stock, movimientos y alertas; regla de `stock_current` protegida con test.

---

## INV-002 — Panel V1 (Templates + HTMX) + Queries Dashboard
Estado: Hecho
Fecha: 2025-12-24

Objetivo
Agregar una pantalla de control mínima (80/20) para operación diaria:
- dashboard con indicadores y alertas
- acciones rápidas sobre stock
- detalle de producto con kardex (movimientos)
Manteniendo el sistema escalable para permisos (V2) sin construir un “ERP gigante”.

Cambios técnicos (archivos creados / modificados)

Modificados
- config/settings.py
  - INSTALLED_APPS += ["panel"]
  - LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
- config/urls.py
  - incluye rutas del panel: path("panel/", include("panel.src.web.urls"))

Creados (Panel)
- panel/src/web/urls.py
- panel/src/web/access/require_scope.py
- panel/src/web/views/auth_view.py
- panel/src/web/views/dashboard_view.py
- panel/src/web/views/actions_stock_view.py
- panel/src/web/views/product_view.py
- panel/src/web/templates/panel/base.html
- panel/src/web/templates/panel/login.html
- panel/src/web/templates/panel/dashboard.html
- panel/src/web/templates/panel/product_detail.html
- panel/src/web/templates/panel/partials/_summary.html
- panel/src/web/templates/panel/partials/_activity.html
- panel/src/web/templates/panel/partials/_alerts.html
- panel/src/web/templates/panel/partials/_top_products.html
- panel/src/web/templates/panel/partials/_search_results.html
- panel/src/web/templates/panel/partials/_quick_actions.html
- panel/src/web/templates/panel/partials/_kardex.html

Creados (Queries Dashboard)
- inventory/src/application/queries/dashboard/__init__.py
- inventory/src/application/queries/dashboard/summary_q.py
- inventory/src/application/queries/dashboard/activity_q.py
- inventory/src/application/queries/dashboard/alerts_q.py
- inventory/src/application/queries/dashboard/top_products_q.py

DoD
- [x] Login por sesión funciona: /panel/login/
- [x] Dashboard carga partials HTMX sin errores: /panel/
- [x] Search parcial devuelve productos y linkea al detalle
- [x] Acciones rápidas funcionan (entry, exit, adjust-to-count con razón obligatoria)
- [x] Kardex muestra movimientos del producto
- [x] Queries dashboard verificadas por shell
- [x] Permisos preparados para escalar (V2) con require_scope

Resultado
Panel V1 operativo para control diario con el mínimo indispensable.

---

## INV-004 — Quick Actions por SKU — HECHO
Endpoints panel, vistas y partials para operar por SKU sin navegar.
- Rutas: `entry-by-sku`, `exit-by-sku`, `adjust-to-count-by-sku`
- UI: forms HTMX que rinden `_toast.html`

## INV-005 — Integridad — HECHO
Aplicada normalización global y razones obligatorias; choices en DB.
- `normalize_sku` en dominio y usado en API/panel/imports
- `require_reason` en entry/exit/adjust
- `movement_type` con choices `entry|exit|adjust_count|adjust_delta` y constraint

## INV-006 — Movimientos globales — HECHO
Pantalla y parciales con filtros HTMX (hoy/7d, sku, tipo).
- Query `application/queries/movements_q.py`
- Página `panel/movements.html` y parcial `_movements_list.html`

## INV-007 — UI errores + LOGGING — HECHO
Templates 403/404/500 y logging operativo.
- `LOGGING` en settings y hooks en commands
- `_toast.html` para errores consistentes en panel
