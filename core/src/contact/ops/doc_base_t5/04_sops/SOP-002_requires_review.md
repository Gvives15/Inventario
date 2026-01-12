# SOP-002 — Requires Review

**Estado**: Active (v0.2 T5)
**Responsable**: Ops Lead
**DoD**: Todo pedido en Review debe tener `review_reason_code`, una nota explicativa y un plan de resolución (deadline).

---

## 1. Definición y Trigger

Un pedido entra en estado `REQUIRES_REVIEW` cuando ocurre una excepción que impide su flujo normal hacia `PREPARING`.

**Triggers (Cómo entra):**
1.  **Automático**: El sistema detecta anomalías (ej. SKU desconocido, zona fuera de rango).
    *   *Setea*: `ops_status=REQUIRES_REVIEW`, `review_reason_code=<AUTO_CODE>`.
2.  **Manual**: El operador detecta un problema en un pedido confirmado.
    *   *Acción*: Admin → Order → Action: "Send to Review".
    *   *Setea*: `ops_status=REQUIRES_REVIEW`, `review_reason_code=MANUAL_REVIEW`.

**Campos Obligatorios:**
*   `review_reason_code`: Código estandarizado del problema (ver [Reason Codes](../05_reason_codes/00_reason_codes_index.md)).
*   `note` (Opcional al entrar, obligatorio al resolver): Contexto adicional.

---

## 2. Gestión de la Cola (Admin)

Los pedidos en revisión **NO** se gestionan desde la lista general de órdenes. Tienen su propio tablero.

**Ubicación**: Admin → **Review Queue** (bajo Contact).

**Visualización y Prioridad:**
La cola se ordena por urgencia (`review_deadline_at` ASC).
1.  **Overdue** (Rojo): Deadline vencido. Prioridad máxima.
2.  **Pending** (Amarillo): Deadline futuro. Gestionar antes de vencimiento.
3.  **No Deadline** (Gris): Sin fecha límite. "Deuda operativa" (debe asignarse fecha).

**Filtros Rápidos:**
*   `Pending`: Pedidos activos con fecha futura.
*   `Overdue`: Pedidos vencidos.
*   `No deadline`: Pedidos sin clasificación de tiempo.

---

## 3. Resolución

El objetivo es sacar el pedido de `REQUIRES_REVIEW` lo antes posible.

### Acciones de Resolución
Desde la **Review Queue**, selecciona los pedidos y ejecuta:

1.  **Resolve REVIEW → PREPARING**
    *   *Cuándo*: El problema se solucionó y el pedido puede prepararse.
    *   *Requisito*: Ingresar **Nota de Resolución** obligatoria.
    *   *Ejemplo*: "Cliente confirmó cambio de sabor. Stock ajustado."

2.  **Resolve REVIEW → CANCELLED**
    *   *Cuándo*: No se puede cumplir el pedido o el cliente desistió.
    *   *Requisito*: Ingresar **Nota de Resolución** obligatoria.
    *   *Ejemplo*: "Cliente no acepta costo de envío extra."

### Gestión de Tiempos (SLAs)
Si no se puede resolver inmediatamente, establece un deadline para seguimiento:
*   **Set deadline +24h**: Problemas leves (ej. esperar respuesta de cliente).
*   **Set deadline +72h**: Problemas complejos (ej. reposición de stock).

---

## 4. Auditoría y Trazabilidad

Cada movimiento en este SOP genera un registro inmutable en `OrderOpsEventModel`.

| Acción | Evento Generado | Datos Clave |
| :--- | :--- | :--- |
| Entra a Review | `to_review` | `from_status=CONFIRMED`, `reason_code=...` |
| Resolución | `resolve_review` | `to_status=PREPARING/CANCELLED`, `note="<Texto>"` |
| Cambio Deadline | (Implicit Update) | `review_deadline_at` modificado |

**Verificación:**
*   Revisar historial en el admin de la orden (inline `Order Ops Events`).
