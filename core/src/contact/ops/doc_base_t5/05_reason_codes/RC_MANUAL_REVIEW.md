# Reason Code: MANUAL_REVIEW

**Código**: `RC_MANUAL_REVIEW`
**Severidad**: Variable

## Ficha Técnica

*   **Definición**: El pedido requiere atención humana por una causa no tipificada en otros códigos específicos.
*   **Causa Típica**: Notas extrañas del cliente, sospecha de fraude, validación especial de stock o logística compleja.
*   **Qué se pide al cliente**: Depende del caso específico.
    *   *Template*: [`TPL-REV-08`](../06_templates/TPL-REV-08_MANUAL_REVIEW.md)
*   **Resolución Permitida**:
    *   `PREPARING`: Si se resuelve la incidencia favorablemente.
    *   `CANCELLED`: Si no es posible proceder.
*   **Deadline Sugerido**: +24h (evaluar según complejidad).
