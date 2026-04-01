-- Supplier Credit Profile Query
-- Purpose: Aggregates credit behaviour metrics per supplier for risk assessment and clustering

SELECT
    DATE_FORMAT(po.po_month, '%Y-%m') AS period_month,
    s.supplier_id,
    s.supplier_name,
    t.supplier_category,
   
    COUNT(DISTINCT po.order_id) AS order_volume,
    COUNT(DISTINCT req.credit_request_id) AS credit_request_count,
    COUNT(DISTINCT item.po_item_id) AS credited_line_count,
   
  -- Preventable credits (supplier fault)
    SUM(CASE
        WHEN r.reason_desc IN (
            'Incorrectly Supplied - Wrong Part',
            'Item Damaged',
            'Incorrectly Supplied - Wrong Model',
            'Incorrectly Supplied - Wrong Side'
        ) THEN 1 ELSE 0
    END) AS preventable_credit_lines,
   
    ROUND(
        100.0 * SUM(CASE
            WHEN r.reason_desc IN (
                'Incorrectly Supplied - Wrong Part',
                'Item Damaged',
                'Incorrectly Supplied - Wrong Model',
                'Incorrectly Supplied - Wrong Side'
            ) THEN 1 ELSE 0
        END) / NULLIF(COUNT(DISTINCT item.po_item_id), 0),
        1
    ) AS pct_preventable_of_credited_lines,

    -- Customer-driven credits
    SUM(CASE
        WHEN r.reason_desc IN (
            'No Longer Required',
            'Job Cancelled',
            'Changed Method of Repair',
            'Duplicate',
            'Return Code 2.Incorrectly ordered by repairer'
        ) THEN 1 ELSE 0
    END) AS customer_driven_credit_lines,
   
  -- Key pricing signal: preventable credits per 1,000 orders
    ROUND(
        1000.0 * SUM(CASE
            WHEN r.reason_desc IN (
                'Incorrectly Supplied - Wrong Part',
                'Item Damaged',
                'Incorrectly Supplied - Wrong Model',
                'Incorrectly Supplied - Wrong Side'
            ) THEN 1 ELSE 0
        END) / NULLIF(COUNT(DISTINCT po.order_id), 0),
        2
    ) AS preventable_credits_per_1000_orders,
   
    ROUND(
        100.0 * COUNT(DISTINCT item.po_item_id) / NULLIF(COUNT(DISTINCT po.order_id), 0),
        2
    ) AS pct_orders_with_credit_line

FROM purchase_order po
INNER JOIN supplier s ON s.supplier_id = po.supplier_id
INNER JOIN supplier_type t ON t.type_id = s.type_id
LEFT JOIN purchase_order_item item ON item.order_id = po.order_id 
    AND item.credit_reason_id IS NOT NULL
LEFT JOIN credit_reason r ON r.reason_id = item.credit_reason_id
LEFT JOIN credit_request req ON req.order_id = po.order_id

WHERE po.po_month >= '2024-06'
  AND po.po_month <= '2025-12'
  AND s.type_id IN (3,4,5,6)
  AND s.supplier_name NOT LIKE '(T)%'

GROUP BY
    period_month,
    supplier_id,
    supplier_name,
    supplier_category

ORDER BY 
    period_month DESC,
    preventable_credits_per_1000_orders DESC,
    credited_line_count DESC;
