Failure Modes (típicos)

- Intento de PAID antes de DELIVERED → ValidationError.
- Resolver REVIEW desde estado no REQUIRES_REVIEW → ValidationError.
- REQUIRES_REVIEW sin reason_code → ValidationError.
- Duplicados de inbound (MessageEventLog) → marcado como SKIPPED_DUPLICATE.
- Outbound repetido el mismo día con mismo payload → dedupe y skip.

