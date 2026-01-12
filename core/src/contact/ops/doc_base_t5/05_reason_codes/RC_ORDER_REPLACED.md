# Reason Code: ORDER_REPLACED

**Código**: `RC_ORDER_REPLACED`
**Severidad**: Baja

## Ficha Técnica

*   **Definición**: Existe un pedido más reciente o duplicado que reemplaza al actual.
*   **Causa Típica**: El cliente creó un pedido nuevo para corregir el anterior en lugar de solicitar edición.
*   **Qué se pide al cliente**: Confirmación de cuál pedido mantener (solo si hay duda).
    *   *Template*: [`TPL-REV-04`](../06_templates/TPL-REV-04_ORDER_REPLACED.md)
*   **Resolución Permitida**:
    *   `CANCELLED`: Se cancela el pedido viejo/duplicado (manteniendo activo el nuevo).
*   **Deadline Sugerido**: Inmediato.
