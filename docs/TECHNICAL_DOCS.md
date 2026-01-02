# Documentación Técnica - Proyecto Inventario (Cierre Tarea 1)

## 1. Visión General de la Arquitectura

El proyecto sigue una arquitectura modular basada en **Domain-Driven Design (DDD)** simplificado y **CQRS (Command Query Responsibility Segregation)**, construida sobre Django y Django Ninja.

La estructura de directorios se ha refactorizado para promover `inventory` y `contact` como módulos de dominio hermanos, eliminando la dependencia de una carpeta `api` contenedora para la lógica de negocio.

### Estructura de Directorios

```
core/
└── src/
    ├── inventory/           # Módulo Core (Gestión de Stock)
    │   ├── domain/          # Reglas de negocio puras, errores, tipos
    │   ├── application/     # Casos de uso (Commands/Queries)
    │   ├── infrastructure/  # Persistencia (ORM, Repositorios)
    │   ├── schemas/         # Esquemas Pydantic (DTOs de Entrada/Salida)
    │   ├── routes.py        # Router Ninja del módulo
    │   └── models.py        # Modelos Django (Product, StockMovement)
    │
    ├── contact/             # Bounded Context Contact (Conversación + Pedidos)
    │   ├── modules/         # Sub-módulos (conversations, orders)
    │   ├── models.py        # Modelos (Contact, Order, ConversationState)
    │   ├── routes.py        # Router Ninja del módulo
    │   └── apps.py          # Configuración de la App Django
    │
    └── api/                 # Capa de Gateway / Integración
        ├── auth/            # Autenticación
        └── routes/          # (Vacío / obsoleto) Wiring centralizado en config/api.py
```

## 2. Componentes Principales

### 2.1. Core Inventory (`core/src/inventory`)

Este módulo maneja la lógica central de inventario. Es autocontenido y define su propia API a través de esquemas y routers.

*   **Modelos (`models.py`)**:
    *   `Product`: Entidad principal (SKU, nombre, stock actual).
    *   `StockMovement`: Registro inmutable de cambios (Entrada, Salida, Ajuste).
*   **Esquemas (`schemas/`)**:
    *   Define los contratos de datos (DTOs) para la API (`ProductOut`, `StockEntryIn`), movidos aquí para mantener la cohesión del módulo.
*   **Reglas de Negocio (`domain/rules.py`)**:
    *   Validaciones de cantidad positiva.
    *   Prohibición de stock negativo en salidas.
    *   Requerimiento de motivos para ajustes.
*   **Commands (`application/commands/`)**:
    *   `record_entry_cmd`: Aumenta stock, crea movimiento.
    *   `record_exit_cmd`: Disminuye stock, valida no-negativo.
    *   `adjust_to_count_cmd`: Ajuste por inventario físico.
*   **Queries (`application/queries/`)**:
    *   Optimized SQL queries para dashboards y listados.

### 2.2. Bounded Context Contact (`core/src/contact`)

Módulo de negocio completo (Bounded Context) que gestiona la conversación comercial y las propuestas de pedido.

*   **Modelos (`models.py`)**:
    *   `Contact`: Información del cliente/proveedor (WhatsApp ID, Zona, Tipo).
    *   `ConversationState`: **OneToOne** con Contact. Mantiene el estado de la conversación (Stage) y última orden.
    *   `OrderModel` / `OrderItemModel`: Propuestas de pedidos.
*   **Gestión de Estado (`modules/conversations`)**:
    *   Garantiza que todo contacto tenga un estado de conversación.
    *   Transiciones de estado (ej. `E1_MIN_DATA` -> `E2_PRODUCT_SELECTION`).
*   **Pedidos (`modules/orders`)**:
    *   Generación de propuestas de pedido.
    *   `kiosk_template.py`: Lógica para presentar productos disponibles (Validación de SKU con Regex).

## 3. Flujos Críticos Implementados

### 3.1. Transición E1 -> E2 (Conversación)
1.  **Upsert Contact**: Se busca o crea el contacto por WhatsApp ID.
2.  **State Guarantee**: Si no existe `ConversationState`, se crea automáticamente en `E1_MIN_DATA`.
3.  **Set Stage**: Se actualiza el stage a `E2_PRODUCT_SELECTION`.
4.  **Create Proposal**: Se genera una orden borrador (`PROPOSED`).
5.  **Validation**: Se valida la integridad de los items (SKU, cantidad) usando `InvalidTemplateItem`.

### 3.2. Gestión de Errores y Atomicidad
*   **Custom Exceptions**: `ContactNotFound`, `MissingMinData`, `InvalidTemplateItem` permiten un manejo de errores preciso en la API.
*   **Atomic Transactions**: Los comandos de inventario y creación de órdenes usan `transaction.atomic()` para asegurar que no queden datos inconsistentes en caso de error.

## 4. Comandos de Gestión

### `demo_task1`
Comando para demostración y validación del flujo E1->E2.

```bash
python manage.py demo_task1 --whatsapp "123456" --name "Demo User" --zone "CABA" --type "Kiosco"
```

Argumentos:
*   `--whatsapp`: ID del usuario (Requerido).
*   `--name`: Nombre del usuario (Requerido).
*   `--zone`: Zona del cliente (Requerido).
*   `--type`: Tipo de negocio (Requerido).

## 5. Configuración del Proyecto

*   **`sys.path`**: Configurado en `settings/base.py` para incluir `core/src`, permitiendo importaciones directas como `import inventory` y `import contact`.
*   **Apps**:
    *   `inventory`: Configurada en `core/src/inventory/apps.py`.
    *   `contact`: Configurada en `core/src/contact/apps.py`.
*   **API Configuration (`config/api.py`)**:
    *   Centraliza el registro de routers.
    *   Importa `contact_router` desde `contact.routes`.
    *   Importa `inventory_router` desde `inventory.routes`.

## 6. Reglas de Arquitectura

### 6.1. Router Pattern (Opción 2: Modular Feature Routers)
Cada módulo (`inventory`, `contact`) expone su propio router en `routes.py`. La capa `api/` (en `config/api.py`) solo actúa como wiring, registrando estos routers.

### 6.2. Regla de Oro para Routers
Los archivos `routes.py` dentro de los módulos tienen una restricción estricta de dependencias:
*   **Permitido**: Importar Schemas (DTOs) y Application Layer (Commands/Queries).
*   **PROHIBIDO**: Importar Modelos (ORM) o Repositorios directamente. La lógica de negocio y persistencia debe estar encapsulada.

## 7. Próximos Pasos Sugeridos
*   Refactorizar `inventory/routes.py` para eliminar dependencias directas de repositorios (cumplir Regla de Oro).
*   Implementar autenticación robusta para el módulo de contactos.
*   Expandir la lógica de templates para incluir precios y promociones dinámicas.
*   Conectar los pedidos confirmados (`OrderModel`) con los movimientos de stock (`StockMovement`).
