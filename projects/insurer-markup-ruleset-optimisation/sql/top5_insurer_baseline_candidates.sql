-- top5_insurer_baseline_candidates.sql
-- Step 3: Top 5 Insurer Candidate Selection
-- Identifies insurers with the highest number of repairers using custom rules
-- and quantifies the variation in markup rules to highlight standardisation opportunities

SELECT
    i.insurer_name AS Insurer,
    COUNT(DISTINCT r.repairer_id) AS Total_Unique_Repairers,
    AVG(r.default_markup_on_parts) AS Avg_Markup_Across_Network,
    -- This helps see if there is one common rule or if it's messy
    COUNT(DISTINCT r.default_markup_on_parts) AS Number_of_Different_Rule_Variations
FROM repairer r
JOIN insurer i ON r.insurer_id = i.insurer_id
WHERE r.insurer_id > 1          -- Exclude the 'Default/Standard' rule
GROUP BY i.insurer_name
ORDER BY Total_Unique_Repairers DESC
LIMIT 10;
