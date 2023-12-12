select 
fd.factoring_document_id,
fd.folio as folio_factura,
fd.credit_folio as folio_credito,
fd.total as factura_importe,
fd.currency as factura_moneda,
c.start_date as credito_fecha_inicio,
c.end_date as credito_fecha_fin,
fd.payment_date as fecha_pago,
fd.porcentaje_adelanto,
cl.amount as linea_limite,
cl.currency as linea_moneda_principal,
cl.start_date as credit_line_start_date,
cli.rfc as cliente_rf,
cli.entity_name as cliente_razon_social,
cli.tax_regime as cliente_regimen_fiscal,
cli.birthdate as cliente_fecha_nacimiento,
cli.sector as cliente_sector,
fd.receiver_rfc  as pagador_rfc,
fd.receiver_name  as pagador_nombre,
er1.exchange_value as exchange_value_invoice,
er2.exchange_value as exchange_value_credit_line
from blu.factoring_document fd 
inner join blu.credits c on c.credit_id = fd.credit_id 
inner join blu.credit_lines cl on cl.credit_line_id = fd.credit_line_id
inner join blu.clients cli on cli.client_id = fd.client_id
left join master.exchange_rates er1 on er1.exchange_date = c.start_date
left join master.exchange_rates er2 on er2.exchange_date = cl.start_date
where fd.payment_date is not null
--where fd.folio = '5212'
