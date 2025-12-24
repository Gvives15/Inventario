# Inventario V1 — O11CE (Django + Django Ninja + Panel HTMX)

Sistema mínimo 80/20 para control real de inventario:
- API (Django Ninja + JWT) para integraciones y automatización.
- Panel (Django Templates + HTMX) para control diario y acciones rápidas.
- Regla central: el stock no se edita directo. Solo cambia por movimientos auditables.

---

## Qué es este sistema (alcance V1)

### Incluye (V1)
- Productos (crear / listar / ver / editar campos permitidos).
- Movimientos de stock:
  - entry (entrada)
  - exit (salida)
  - adjust-to-count (ajuste por conteo real)
  - adjust-delta (ajuste por delta)
- Auditoría por movimiento (StockMovement).
- Alertas: productos bajo mínimo.
- Dashboard con 5 bloques:
  - Resumen
  - Actividad de hoy
  - Alertas (bajo mínimo + ajustes recientes)
  - Top impacto (7 días)
  - Acciones rápidas (entry/exit/adjust-to-count)
- Login por sesión para Panel (no JWT).

### NO incluye (V1)
- Roles/permisos reales (todos los usuarios logueados acceden a todo).
- Multi-almacén / lotes / vencimientos.
- Compras/ventas completas (solo movimientos de stock).
- Reportes BI avanzados.

---

## Arquitectura (la regla del proyecto)

Este repo evita carpetas genéricas tipo `services.py` / `views.py` ambiguos.

### Capas
- `inventory/src/domain/`  
  Contrato de negocio: tipos, errores, reglas puras.  
  No Django, no DB, no Ninja.
- `inventory/src/infrastructure/`  
  ORM Django + repos + transacciones.
- `inventory/src/application/`  
  Casos de uso:
  - `commands/` = escribe (mutaciones)
  - `queries/` = lee (dashboard, listados)
- `inventory/src/api/`  
  Django Ninja: routers/schemas/auth JWT.
- `panel/src/web/`  
  Django templates + HTMX para interfaz de control.

### Regla de oro: Stock inmutable por PATCH
`Product.stock_current` no se edita vía update de producto.
Solo cambia a través de comandos:
- `record_entry_cmd`
- `record_exit_cmd`
- `adjust_to_count_cmd`
- `adjust_delta_cmd`

---

## Estructura de carpetas (mapa)

### Inventario
- `inventory/src/infrastructure/orm/models.py`  
  Modelos `Product`, `StockMovement`.
- `inventory/src/infrastructure/orm/product_repo.py`  
  Lecturas + updates permitidos.
- `inventory/src/infrastructure/orm/stock_movement_repo.py`  
  Crear/listar movimientos.
- `inventory/src/application/commands/*`  
  Lógica de entrada/salida/ajustes.
- `inventory/src/application/queries/*`  
  Listados y dashboard.
- `inventory/src/api/routes/*`  
  Endpoints Ninja.
- `inventory/src/api/auth/jwt_bearer.py`  
  Auth JWT (API).

### Panel
- `panel/src/web/views/auth_view.py`  
  Login/logout sesión.
- `panel/src/web/views/dashboard_view.py`  
  Página dashboard + endpoints parciales HTMX.
- `panel/src/web/views/actions_stock_view.py`  
  Acciones rápidas (POST) que llaman a commands.
- `panel/src/web/views/product_view.py`  
  Detalle de producto + kardex (movimientos).
- `panel/src/web/templates/panel/*`  
  Templates y partials HTMX.
- `panel/src/web/access/require_scope.py`  
  Hook de permisos (V1 = allow; V2 = scopes reales).

---

## Instalación

### Requisitos
- Python 3.11+ (recomendado)
- pip

### Instalar dependencias
```bash
pip install -r requirements.txt
```

> Si no existe `requirements.txt`, instalar mínimo:

```bash
pip install django django-ninja PyJWT
```

### Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### Crear usuario (para panel y para emitir JWT)

```bash
python manage.py createsuperuser
```

### Levantar server

```bash
python manage.py runserver
```

---

## Uso — Panel (Templates + HTMX)

### Login

- `GET /panel/login/`

### Dashboard

- `GET /panel/`

### Detalle producto (kardex)

- `GET /panel/products/<id>/`

### Acciones rápidas (POST)

- `/panel/actions/stock/entry/`
- `/panel/actions/stock/exit/`
- `/panel/actions/stock/adjust-to-count/`

### Quick Actions por SKU

- `POST /panel/actions/stock/entry-by-sku/`
- `POST /panel/actions/stock/exit-by-sku/`
- `POST /panel/actions/stock/adjust-to-count-by-sku/`

Respuesta: partial HTMX `_toast.html` con OK/ERROR.

### Movimientos globales

- `GET /panel/movements/`
- `GET /panel/movements/partials/list/?range=today|7d&sku=SKU123&type=entry|exit|adjust_count|adjust_delta`

### Integridad (Reglas)

- `normalize_sku(raw)` aplicado en todos los puntos de entrada (API, panel, imports).
- `require_reason(reason)` obligatorio en `entry`, `exit`, `adjust-*`.
- `movement_type` con choices reales: `entry`, `exit`, `adjust_count`, `adjust_delta`.

### Errores y Logging

- Templates `403.html`, `404.html`, `500.html` con estilo del panel.
- `LOGGING` en `config/settings.py` con canal `inventory.movements`.
- Los commands emiten logs con: `sku`, `type`, `delta`, `stock`, `reason`, `user_id`.

---

## Uso — API (Django Ninja + JWT)

Base: `/api/`

### Obtener token

`POST /api/auth/token`

```json
{"username":"...", "password":"..."}
```

Respuesta:

```json
{"access_token":"...","token_type":"Bearer","expires_in_seconds":43200}
```

### Usar token

Header: `Authorization: Bearer <token>`

### Inventario (protegido por JWT)

- `POST /api/inventory/products`
- `GET /api/inventory/products`
- `GET /api/inventory/products/{id}`
- `PATCH /api/inventory/products/{id}` (sin stock_current)
- `POST /api/inventory/stock/entry`
- `POST /api/inventory/stock/exit`
- `POST /api/inventory/stock/adjust-to-count`
- `POST /api/inventory/stock/adjust-delta`
- `GET /api/inventory/products/{id}/movements?limit=50`
- `GET /api/inventory/alerts/low-stock`

---

## Configuración JWT

Variables opcionales:
- `JWT_SIGNING_KEY`
- `JWT_TTL_SECONDS`
- `JWT_ISSUER`
- `JWT_AUDIENCE`
- `JWT_ALGORITHM`

En dev, si no se setea `JWT_SIGNING_KEY`, se usa `SECRET_KEY`.

---

## Permisos y escalabilidad (V2 planificado)

V1: todo usuario logueado tiene acceso total.

V2: permisos reales sin reescribir templates ni vistas:
- Punto único: `panel/src/web/access/require_scope.py`
- Agregar:
  - roles (admin, operador, auditor, etc.)
  - scopes por módulo (`inventory.read`, `inventory.write`, `dashboard.read`, etc.)
  - chequeo centralizado
- Meta: cambiar permisos sin tocar 50 archivos.

---

## Cambios y mejoras (obligatorio)

Todo cambio (feature, refactor, fix) se registra en:
- `docs/IMPROVEMENTS.md`

Regla:
- No se trabaja “de memoria”.
- Cada cambio tiene ID (`INV-xxx`), estado y checklist.
- Si no está escrito, no existe.
