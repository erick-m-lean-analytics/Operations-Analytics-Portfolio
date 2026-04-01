-- repairer_override_groups.sql
-- Step 1: Repairer Override Behaviour Analysis
-- Identifies repairers performing manual edits and segments them into the four behavioural groups

-- Query 1: High-level Default vs Custom rule usage + manual edit rate
SELECT
    CASE
        WHEN d.insurer_id = 1 THEN 'Default Rule'
        WHEN d.insurer_id > 1 THEN 'Custom Rule'
        ELSE 'No Rule Assigned'
    END AS Rule_Segment,
    COUNT(DISTINCT d.repairer_id) AS Total_Repairers,
    COUNT(DISTINCT CASE WHEN i.is_manual_markup = 1 THEN d.repairer_id END) AS Manual_Editors,
    ROUND(
        COUNT(DISTINCT CASE WHEN i.is_manual_markup = 1 THEN d.repairer_id END) 
        / COUNT(DISTINCT d.repairer_id) * 100, 
    2) AS Percent_Manual_Behavior
FROM quote_draft d
JOIN quote_item_price i 
    ON d.quote_id = i.quote_id
WHERE d.quote_date >= (CURDATE() - INTERVAL 90 DAY)
  AND i.is_selected = 1
  AND d.status_id NOT IN (1, 3)
GROUP BY Rule_Segment;


-- Query 2: Further segmentation into the four behavioural groups
SELECT
    CASE
        WHEN Custom_Draft_Ratio = 100 THEN '1. Purely Custom (100% of Quotes)'
        WHEN Custom_Draft_Ratio >= 75 THEN '2. High Custom Adoption (>75%)'
        WHEN Custom_Draft_Ratio >= 25 THEN '3. Hybrid User (25% - 75%)'
        ELSE '4. Low Custom Adoption (<25%)'
    END AS Custom_Engagement_Level,
    COUNT(*) AS Shop_Count,
    AVG(Manual_Ratio) AS Avg_Manual_Rate
FROM (
    SELECT
        d.repairer_id,
        ROUND(SUM(CASE WHEN d.insurer_id > 1 THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS Custom_Draft_Ratio,
        ROUND(SUM(CASE WHEN i.is_manual_markup = 1 THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS Manual_Ratio
    FROM quote_draft d
    JOIN quote_item_price i 
        ON d.quote_id = i.quote_id
    WHERE d.quote_date >= (CURDATE() - INTERVAL 90 DAY)
      AND d.status_id NOT IN (1, 3)
      AND i.is_selected = 1
    GROUP BY d.repairer_id
) AS ShopStats
GROUP BY Custom_Engagement_Level
ORDER BY Custom_Engagement_Level ASC;
