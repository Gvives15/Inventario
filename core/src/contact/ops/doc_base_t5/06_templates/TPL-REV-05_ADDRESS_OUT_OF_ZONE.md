# Template: ADDRESS_OUT_OF_ZONE

**ID**: `TPL-REV-05`
**Reason Code**: `RC_ADDRESS_OUT_OF_ZONE`
**Canal**: WhatsApp
**Versión**: v1

## Ficha Técnica

*   **Trigger**: Dirección fuera de rango logístico.
*   **Variables Requeridas**:
    *   `customer_name`
    *   `address` (la dirección problemática)

## Mensaje (Copy & Paste)

```text
Hola {customer_name}, te escribimos por tu pedido.

Vemos que la dirección "{address}" nos figura fuera de nuestra zona de reparto habitual.

¿Tendrás alguna otra dirección dentro de zona, o preferís retirar por sucursal?

Avisanos y coordinamos.
```

## Reglas de Uso
*   Verificar mapa antes de enviar.
*   Ofrecer alternativas proactivamente (sucursal más cercana).
