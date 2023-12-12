select 
ipl.created_at,
ipl.factoring_document_id,
ipl.response as prediction_result,
c.end_date as credito_fecha_fin,
fd.payment_date as fecha_pago,
(fd.payment_date - c.end_date) as days_late,
(case 
	when (fd.payment_date - c.end_date) < 0 then 1
	when (fd.payment_date - c.end_date) = 0 then 2
	when (fd.payment_date - c.end_date) < 7 then 3
	when (fd.payment_date - c.end_date) < 21 then 4
	else 5
end) as real_value
from invoice_prediction_log ipl 
inner join blu.factoring_document fd on fd.factoring_document_id  = ipl.factoring_document_id
inner join blu.credits c on c.credit_id = fd.credit_id 