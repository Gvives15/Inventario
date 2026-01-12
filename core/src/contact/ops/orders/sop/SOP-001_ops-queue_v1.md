---
id: SOP-001
title: Cola operativa de pedidos (operación mínima)
version: v1
owner: ops/orders
risk: ROJO
last_updated: 2026-01-09
system: [Order.ops_status, OrderOpsEvent, Django Admin]
---

## Objetivo
Operar pedidos confirmados sin perder ninguno: preparar, despachar, entregar y cobrar (solo en entrega).

## DoD (Definition of Done)
- [ ] Ningún pedido ops_status=CONFIRMED queda sin acción > 30 min.
- [ ] REQUIRES_REVIEW siempre con review_reason_code y nota si aplica.
- [ ] PAID solo después de DELIVERED.
- [ ] Cada cambio crea OrderOpsEvent.

## Estados operativos (ops_status)
CONFIRMED → PREPARING → READY → OUT_FOR_DELIVERY → DELIVERED → PAID
Excepciones: REQUIRES_REVIEW, CANCELLED, REPLACED (no manual)

## Rutina diaria (vos solo)
### Apertura (06:00)
- [ ] Filtrar ops_status=REQUIRES_REVIEW y resolver primero.
- [ ] Filtrar ops_status=CONFIRMED hoy y pasar a PREPARING o REVIEW.

### Ciclo (cada 30–60 min)
- [ ] CONFIRMED → PREPARING
- [ ] PREPARING → READY
- [ ] READY → OUT_FOR_DELIVERY
- [ ] OUT_FOR_DELIVERY → DELIVERED
- [ ] DELIVERED → PAID

### Cierre (20:30–21:00)
- [ ] OUT_FOR_DELIVERY: cerrar o anotar incidencia.
- [ ] REVIEW: acción definida (resolver/cancelar/reprogramar).
- [ ] Reporte rápido: counts por estado.

## Acciones en Admin
- PREPARING / READY / OUT_FOR_DELIVERY / DELIVERED / PAID / CANCELLED
- REQUIRES_REVIEW_GENERIC (MANUAL_REVIEW)
- REQUIRES_REVIEW (con motivo)

## Escalamiento (gatillos)
- SKU_UNKNOWN / CHANGE_AFTER_CONFIRM / CANCEL_AFTER_CONFIRM → REQUIRES_REVIEW
- ADDRESS_OUT_OF_ZONE → REQUIRES_REVIEW

## Evolución futura — Modo rápido (Wave Picking)

**Contexto:** cuando operemos 10+ pedidos por día y muchos kioscos acepten el pedido sin cambios, conviene pasar de “pedido por pedido” a “olas” (waves) para ahorrar tiempo.

### Qué es Wave Picking
En vez de preparar pedidos de a uno, se seleccionan varios pedidos CONFIRMED y se preparan en bloque:
1) pasar pedidos a PREPARING (batch)
2) generar pick list agregada por SKU (total por producto)
3) pickeo por categorías en una sola pasada
4) armado + rotulado por pedido
5) pasar todos a READY (batch)

### Requisito técnico mínimo (pendiente)
- Command: `pick_list` que genere lista agregada por SKU para pedidos en PREPARING (filtrable por fecha/estado).
- Output mínimo: `SKU | Nombre | total_qty | #pedidos` (opcional: order_ids donde aparece).
- Admin actions batch ya existen (PREPARING/READY), pero falta el pick list.

### DoD cuando se implemente
- [ ] El pick list se genera en < 2s para 10–50 pedidos.
- [ ] Reduce tiempo total de preparación sin aumentar errores.
- [ ] Auditoría intacta: OrderOpsEvent por transición.

**Nota:** Hasta implementar `pick_list`, se opera en modo “pedido por pedido” (v1).
