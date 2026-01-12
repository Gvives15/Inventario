# Reason Code: SKU_UNKNOWN

**Código**: `RC_SKU_UNKNOWN`
**Severidad**: Alta

## Ficha Técnica

*   **Definición**: El pedido contiene un identificador de producto (SKU) que no existe en el catálogo activo.
*   **Causa Típica**: Error de tipeo del cliente, producto discontinuado, o fallo en el reconocimiento del bot.
*   **Qué se pide al cliente**: Aclaración sobre qué producto quería realmente.
    *   *Template*: [`TPL-REV-01`](../06_templates/TPL-REV-01_SKU_UNKNOWN.md)
*   **Resolución Permitida**:
    *   `PREPARING`: Si el cliente aclara y corregimos el ítem manualmente.
    *   `CANCELLED`: Si el producto no existe y el cliente desiste.
*   **Deadline Sugerido**: +24h.
