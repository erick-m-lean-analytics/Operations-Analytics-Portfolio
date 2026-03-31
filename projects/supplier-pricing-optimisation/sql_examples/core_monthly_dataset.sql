-- Core Monthly Supplier Dataset Query
-- Purpose: Aggregates monthly supplier-level metrics for pricing analysis
-- Includes: order volume, GMV, credits, dominant tier, fees billed, and effective take-rate

SELECT
    s.supplier_id,
    s.supplier_name,
    ip.ledger_invoice_ref,
    t.supplier_category,
   
    -- Audit Trail
    DATE_FORMAT(ip.invoice_date, '%Y-%m-%d') AS invoice_date,
    DATE_FORMAT(po.po_month, '%Y-%m') AS report_month,
   
    -- Volume & Gross Merchandise Value
    COUNT(DISTINCT po.order_id) AS order_volume,
    ROUND(SUM(COALESCE(ped.gmv_gross, 0)), 2) AS gmv_gross,
    ROUND(SUM(COALESCE(ped.gmv_net, 0)), 2) AS gmv_net,
   
    -- Tier Data
    CASE
        WHEN SUM(ped.gold_count) > SUM(ped.blue_count) THEN 'Gold'
        WHEN SUM(ped.blue_count) > SUM(ped.gold_count) THEN 'Blue'
        ELSE 'Mixed'
    END AS dominant_tier,
    SUM(ped.gold_count) AS gold_orders_count,
    SUM(ped.blue_count) AS blue_orders_count,
   
    -- Credits
    SUM(ipd.credit_count) AS credit_transaction_count,
    ROUND(ABS(SUM(ipd.credit_value)), 2) AS credits_value,
   
    -- Revenue & Take Rate
    ROUND(SUM(ipd.fees_billed), 2) AS fees_billed,
    ROUND(SUM(ipd.fees_billed) / NULLIF(SUM(ped.gmv_gross), 0), 4) AS effective_take_rate,
    ROUND(SUM(ipd.fees_billed * (COALESCE(s.gst_rate, 0.10))), 2) AS gst_amount,
    ROUND(SUM(ipd.fees_billed * (1 + COALESCE(s.gst_rate, 0.10))), 2) AS total_billed_with_gst

FROM invoice_issued ip
-- Aggregate Invoice Data per PO/Invoice
INNER JOIN (
    SELECT
        order_id,
        invoice_issued_id,
        SUM(fee_amount) AS fees_billed,
        SUM(CASE WHEN fee_amount < 0 THEN 1 ELSE 0 END) AS credit_count,
        SUM(CASE WHEN fee_amount < 0 THEN fee_amount ELSE 0 END) AS credit_value
    FROM invoice_issued_data
    GROUP BY order_id, invoice_issued_id
) ipd ON ip.invoice_issued_id = ipd.invoice_issued_id

-- LEFT JOIN to capture GMV and Tier info from Payment Data
LEFT JOIN (
    SELECT
        order_id,
        MAX(gmv_gross) AS gmv_gross,
        MAX(gmv_net) AS gmv_net,
        MAX(is_gold_member) AS gold_count,
        MAX(is_blue_member) AS blue_count
    FROM payment_data
    GROUP BY order_id
) ped ON ped.order_id = ipd.order_id

INNER JOIN purchase_order po ON po.order_id = ipd.order_id
INNER JOIN supplier s ON s.supplier_id = ip.supplier_id
INNER JOIN supplier_type t ON t.type_id = s.type_id

WHERE
    s.type_id IN (3,4,5,6)
    AND s.supplier_name NOT LIKE '(T)%'
    AND ip.invoice_date >= '2024-01-01'
    AND ip.invoice_date <= '2025-12-31'

GROUP BY
    s.supplier_id,
    s.supplier_name,
    ip.ledger_invoice_ref,
    t.supplier_category,
    invoice_date,
    report_month

ORDER BY invoice_date DESC, ledger_invoice_ref ASC;
