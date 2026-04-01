-- pilot_repairer_selection.sql
-- Step 4: Pilot Repairer Identification
-- Selects high-volume repairers currently using the legacy Standard rule 
-- that would be strong candidates for testing the new baseline ruleset

SELECT
    r.repairer_name AS Repairer_Name,
    COALESCE(g.group_name, 'Independent') AS MSO_Group,
    COUNT(d.quote_id) AS Total_Quote_Volume,
    -- Labelled as 'Dominant Insurer' to represent the primary volume source
    COALESCE(
        (SELECT 
            CASE
                WHEN d2.insurer_name LIKE '%Allianz%' THEN 'Major Insurer A'
                WHEN d2.insurer_name LIKE '%Suncorp%' OR d2.insurer_name LIKE '%NRMA%' OR d2.insurer_name LIKE '%AAMI%' THEN 'Major Insurer B'
                WHEN d2.insurer_name LIKE '%A&G%' OR d2.insurer_name LIKE '%Auto % General%' THEN 'Major Insurer C'
                WHEN d2.claim_number LIKE '10%' THEN 'Major Insurer A'
                WHEN d2.claim_number LIKE 'S%' OR d2.claim_number LIKE 'M%' THEN 'Major Insurer B'
                ELSE 'Other'
            END
         FROM quote_draft d2
         WHERE d2.repairer_id = d.repairer_id
           AND d2.quote_date >= (CURDATE() - INTERVAL 90 DAY)
           AND d2.insurer_name IS NOT NULL
           AND d2.insurer_name != ''
         GROUP BY d2.insurer_name
         ORDER BY COUNT(*) DESC 
         LIMIT 1),
        'Manual Entry / Misc'
    ) AS Dominant_Insurer,
    ROUND(COUNT(d.quote_id) / 90, 1) AS Avg_Quotes_Per_Day
FROM quote_draft d
JOIN repairer r ON d.repairer_id = r.repairer_id
LEFT JOIN repairer_group g ON g.group_id = r.group_id
WHERE d.quote_date >= (CURDATE() - INTERVAL 90 DAY)
  AND d.insurer_id = 1        -- Legacy 'Standard/Default' rule users
  AND d.status_id NOT IN (1, 3)
GROUP BY r.repairer_name, g.group_name
ORDER BY Total_Quote_Volume DESC
LIMIT 15;
