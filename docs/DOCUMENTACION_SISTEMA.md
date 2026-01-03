# Documentación del Sistema de Inventario

**Versión del Documento:** 1.0  
**Fecha de Actualización:** 2026-01-02  
**Estado:** Activo (V1)

---

## 1. Descripción Detallada del Sistema

### Propósito y Alcance
El sistema de inventario está diseñado bajo la filosofía "80/20" para proporcionar un control real y eficiente del stock sin la complejidad de un ERP masivo. Su propósito principal es garantizar la integridad del inventario mediante un registro inmutable de movimientos, evitando ediciones directas de stock.

**Alcance Actual (V1):**
*   **Gestión de Productos:** Creación, edición y visualización (Kardex).
*   **Control de Stock:** Entradas, Salidas y Ajustes (por conteo o delta).
*   **Auditoría:** Registro histórico de todos los movimientos con motivo y usuario.
*   **Alertas:** Detección automática de stock bajo mínimo.
*   **Panel de Control:** Dashboard operativo con métricas en tiempo real.
*   **Integración:** API RESTful para automatización y sistemas externos (ej. bots de WhatsApp).

### Diagrama de Flujo del Proceso
El siguiente diagrama ilustra el flujo principal de información desde la acción del usuario hasta la persistencia y visualización.

```mermaid
graph TD
    User[Usuario / Operador]
    API[API Externa / Bot]
    
    subgraph "Interfaz de Entrada"
        Panel[Panel Web (HTMX)]
        Endpoints[API REST (Django Ninja)]
    end
    
    subgraph "Capa de Aplicación (Use Cases)"
        CmdEntry[Comando Entrada]
        CmdExit[Comando Salida]
        CmdAdjust[Comando Ajuste]
        Queries[Consultas de Lectura]
    end
    
    subgraph "Dominio (Reglas de Negocio)"
        Rules[Validaciones: Stock Negativo, Razones]
        SKU[Normalización SKU]
    end
    
    subgraph "Infraestructura (Persistencia)"
        DB[(Base de Datos SQLite)]
        Logs[Logging del Sistema]
    end

    User -->|Acción Visual| Panel
    API -->|JSON Request| Endpoints
    
    Panel -->|POST| CmdEntry
    Panel -->|POST| CmdExit
    Panel -->|POST| CmdAdjust
    Panel -->|GET| Queries
    
    Endpoints -->|POST| CmdEntry
    Endpoints -->|POST| CmdExit
    
    CmdEntry & CmdExit & CmdAdjust --> Rules
    Rules -->|OK| DB
    Rules -->|Error| Panel
    
    DB --> Queries
    Queries --> Panel
```

### Tecnologías Utilizadas
*   **Backend:** Python 3.11+, Django 5.x.
*   **API:** Django Ninja (FastAPI-like para Django) con Pydantic.
*   **Frontend (Panel):** Django Templates + HTMX (para interactividad sin SPA compleja).
*   **Base de Datos:** SQLite (Defecto V1), compatible con PostgreSQL.
*   **Contenedorización:** Docker & Docker Compose.
*   **Autenticación:**
    *   **Panel:** Sesiones estándar de Django.
    *   **API:** JWT (JSON Web Tokens).

> **Nota Técnica:** Para detalles profundos sobre la estructura de código, patrones de diseño y decisiones de arquitectura (DDD/CQRS), consulte el documento dedicado: [ARQUITECTURA.md](ARQUITECTURA.md).

---

## 2. Funcionamiento del Sistema

### Proceso Completo (Entrada a Salida)
1.  **Entrada de Datos:**
    *   El operador escanea o ingresa un SKU en el Panel o envía una petición a la API.
    *   El sistema normaliza el SKU (ej. mayúsculas, sin espacios) automáticamente.
2.  **Validación:**
    *   Se verifica que el producto exista.
    *   Se valida que la operación cumpla las reglas de negocio (ej. no dejar stock negativo en salidas, razón obligatoria para ajustes).
3.  **Transacción:**
    *   Se ejecuta una transacción atómica: se actualiza el `stock_current` del producto Y se crea un registro en `StockMovement` simultáneamente.
4.  **Feedback:**
    *   El sistema confirma la operación exitosa o devuelve un error descriptivo.
    *   El dashboard y el kardex se actualizan instantáneamente.

### Roles y Permisos
*   **Versión V1:** Modelo de acceso simplificado. Todo usuario autenticado tiene acceso completo (Admin/Operador).
*   **Versión V2 (Planificada):** Sistema basado en Scopes (`inventory.read`, `inventory.write`) centralizado en `require_scope.py`.

### Procedimientos Operativos Estándar (SOP)
1.  **Inmutabilidad del Stock:** NUNCA editar el campo `stock` directamente en la base de datos. Siempre usar las acciones de "Entrada", "Salida" o "Ajuste" para generar trazabilidad.
2.  **Ajustes de Inventario:** Todo ajuste (diferencia entre sistema y realidad) debe tener una "Razón" explícita (ej. "Robo", "Vencimiento", "Error de Conteo").
3.  **Normalización:** Al crear productos, usar SKUs limpios. El sistema forzará mayúsculas, pero se recomienda mantener un estándar.

---

## 3. Componentes y Producción

### Listado de Módulos
1.  **Core Inventory (`core/src/inventory`):**
    *   Corazón del sistema. Maneja productos y movimientos.
    *   *Funciones:* `record_entry`, `record_exit`, `adjust_to_count`.
2.  **Core Contact (`core/src/contact`):**
    *   Gestión de clientes y proveedores (integración WhatsApp).
    *   *Funciones:* Gestión de estados de conversación, propuestas de pedidos.
3.  **Panel Web (`panel`):**
    *   Interfaz gráfica para humanos.
    *   *Funciones:* Dashboard, Kardex, Acciones Rápidas (HTMX).

### Métricas y KPI del Sistema
El Dashboard calcula en tiempo real:

| Métrica | Descripción | Frecuencia |
| :--- | :--- | :--- |
| **Stock Bajo** | Cantidad de productos con stock <= mínimo. | Tiempo Real |
| **Actividad Diaria** | Unidades y conteo de Entradas, Salidas y Ajustes del día actual. | Tiempo Real |
| **Top Salidas (7d)** | Productos con mayor volumen de salida en la última semana. | 7 días |
| **Ajustes Recientes** | Listado de los últimos ajustes realizados (para auditoría rápida). | Tiempo Real |
| **Top Ajustes (7d)** | Productos que más veces han requerido ajustes (indica problemas operativos). | 7 días |

### Entradas y Salidas Técnicas
*   **Entrada API:** JSON estricto validado por Pydantic (ej. `{ "sku": "A1", "quantity": 10, "reason": "Compra" }`).
*   **Salida API:** JSON con estado actualizado del recurso.
*   **Entrada Panel:** Formularios HTML procesados por HTMX.
*   **Salida Panel:** Fragmentos HTML (Partials) que actualizan solo la sección relevante de la página.

---

## 4. Mantenimiento y Actualización

### Procedimientos para Actualizar Datos
Las actualizaciones de estructura de base de datos se manejan vía migraciones de Django:
1.  Detener el servicio (si es crítico).
2.  Ejecutar `python manage.py migrate`.
3.  Reiniciar el servicio.

### Protocolos de Respaldo y Recuperación
*   **Base de Datos (SQLite):** Copia diaria del archivo `db.sqlite3` a una ubicación segura (fuera del contenedor/servidor).
*   **Recuperación:** Simplemente reemplazar el archivo `db.sqlite3` con el respaldo y reiniciar el servicio.

### Plan de Mantenimiento Preventivo
1.  **Semanal:** Revisar el dashboard de "Alertas" para identificar productos estancados o con ajustes frecuentes.
2.  **Mensual:** Verificar logs de errores (`django.request`) para detectar intentos fallidos o errores de sistema.
3.  **Trimestral:** Revisar usuarios activos y rotar claves si es necesario.
4.  **Actualización de Software:** Ejecutar `git pull` y `pip install -r requirements.txt` para aplicar parches de seguridad y mejoras (registradas en `IMPROVEMENTS.md`).

---

**Registro de Cambios del Documento:**
*   **2026-01-02:** Creación inicial basada en la arquitectura V1, incluyendo detalles de Dashboard y Panel HTMX.
