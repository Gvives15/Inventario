# Reason Code: ADDRESS_OUT_OF_ZONE

**Código**: `RC_ADDRESS_OUT_OF_ZONE`
**Severidad**: Alta

## Ficha Técnica

*   **Definición**: La dirección de entrega proporcionada no coincide con ninguna zona de reparto activa o asignable.
*   **Causa Típica**: Cliente nuevo en zona lejana, error en el mapeo de coordenadas, o dirección incompleta.
*   **Qué se pide al cliente**: Confirmar dirección exacta o proponer punto de encuentro/retiro en sucursal.
    *   *Template*: [`TPL-REV-05`](../06_templates/TPL-REV-05_ADDRESS_OUT_OF_ZONE.md)
*   **Resolución Permitida**:
    *   `PREPARING`: Si se asigna una zona manualmente o se acuerda retiro.
    *   `CANCELLED`: Si la zona está fuera de cobertura logística.
*   **Deadline Sugerido**: +24h.
