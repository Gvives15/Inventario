Máquinas de estados (ops_status)

### Referencias de código
- **Dominio**: [order_status.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/modules/orders/domain/order_status.py) (Estado Comercial)
- **Ops**: [models.py](file:///c:/Users/germa/OneDrive/Documentos/Programas/inventario/core/src/contact/models.py#L51) (Ops Status + Reason Codes)

- Estados
  - CONFIRMED, REQUIRES_REVIEW, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, PAID, CANCELLED, REPLACED
- Transiciones permitidas (principales)
  - CONFIRMED → {PREPARING, REQUIRES_REVIEW, CANCELLED}
  - PREPARING → {READY, REQUIRES_REVIEW, CANCELLED}
  - READY → {OUT_FOR_DELIVERY, REQUIRES_REVIEW, CANCELLED}
  - OUT_FOR_DELIVERY → {DELIVERED, REQUIRES_REVIEW}
  - DELIVERED → {PAID}
  - REQUIRES_REVIEW → {PREPARING, CANCELLED}
- Terminales
  - CANCELLED, REPLACED, PAID
- Validaciones
  - Resolver REVIEW exige estar en REQUIRES_REVIEW
  - PAID solo válido después de DELIVERED
  - REQUIRES_REVIEW exige review_reason_code

