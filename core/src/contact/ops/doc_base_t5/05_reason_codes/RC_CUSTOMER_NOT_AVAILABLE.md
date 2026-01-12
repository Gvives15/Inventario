# Reason Code: CUSTOMER_NOT_AVAILABLE

**Código**: `RC_CUSTOMER_NOT_AVAILABLE`
**Severidad**: Media

## Ficha Técnica

*   **Definición**: El cliente no responde a los intentos de confirmación o coordinación de entrega.
*   **Causa Típica**: Cliente no atiende el teléfono, no responde WhatsApp, o dio número incorrecto.
*   **Qué se pide al cliente**: Confirmación de disponibilidad para recibir el pedido.
    *   *Template*: [`TPL-REV-06`](../06_templates/TPL-REV-06_CUSTOMER_NOT_AVAILABLE.md)
*   **Resolución Permitida**:
    *   `PREPARING`: Si el cliente responde y confirma.
    *   `CANCELLED`: Tras agotarse los intentos de contacto (generalmente 3).
*   **Deadline Sugerido**: +24h (para reintento).
