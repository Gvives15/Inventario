# Reason Code: PAYMENT_ISSUE

**Código**: `RC_PAYMENT_ISSUE`
**Severidad**: Alta

## Ficha Técnica

*   **Definición**: El comprobante de pago es inválido, ilegible, no cubre el monto total o no se ha recibido.
*   **Causa Típica**: Comprobante falso, error de transferencia, olvido del cliente, o imagen borrosa.
*   **Qué se pide al cliente**: Reenviar comprobante válido o completar el saldo pendiente.
    *   *Template*: [`TPL-REV-07`](../06_templates/TPL-REV-07_PAYMENT_ISSUE.md)
*   **Resolución Permitida**:
    *   `PREPARING`: Al validar el pago completo (marcar como PAID luego).
    *   `CANCELLED`: Si no se regulariza el pago en el tiempo estipulado.
*   **Deadline Sugerido**: +24h.
