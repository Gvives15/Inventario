# Reason Codes — Índice

| Code | Definición | Severidad | Decisión Típica |
| :--- | :--- | :--- | :--- |
| [`RC_SKU_UNKNOWN`](./RC_SKU_UNKNOWN.md) | SKU no reconocido en el pedido. | Alta | Corregir SKU o Cancelar ítems. |
| [`RC_ADDRESS_OUT_OF_ZONE`](./RC_ADDRESS_OUT_OF_ZONE.md) | Dirección fuera de zona de cobertura. | Alta | Cancelar o Acordar retiro. |
| [`RC_PAYMENT_ISSUE`](./RC_PAYMENT_ISSUE.md) | Problema con el pago o comprobante. | Alta | Reclamar pago o Cancelar. |
| [`RC_CUSTOMER_NOT_AVAILABLE`](./RC_CUSTOMER_NOT_AVAILABLE.md) | Cliente no responde para confirmar. | Media | Reintentar contacto (+24h). |
| [`RC_CHANGE_AFTER_CONFIRM`](./RC_CHANGE_AFTER_CONFIRM.md) | Cliente pide cambios tras confirmar. | Media | Editar pedido y re-confirmar. |
| [`RC_CANCEL_AFTER_CONFIRM`](./RC_CANCEL_AFTER_CONFIRM.md) | Cliente pide cancelar tras confirmar. | Media | Cancelar pedido. |
| [`RC_ORDER_REPLACED`](./RC_ORDER_REPLACED.md) | Pedido duplicado o reemplazado. | Baja | Cancelar anterior, mantener nuevo. |
| [`RC_MANUAL_REVIEW`](./RC_MANUAL_REVIEW.md) | Revisión manual genérica. | Variable | Investigar caso a caso. |
