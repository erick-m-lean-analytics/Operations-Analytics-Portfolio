-- custom_markup_rules.sql
-- Step 2: Custom Markup Rules Identification
-- Analyses the actual markup rules being used by repairers on custom rulesets
-- Shows UI dropdown names (what the user sees) versus the underlying price logic

SELECT
    Consolidated_Insurer,
    Unique_Custom_Shops_Count,
    Custom_Shops_List,
    Quote_Volume,

    OEM,
    OEM_UI_Rule,

    AFT,
    AFT_UI_Rule,

    RECO,
    RECO_UI_Rule,

    PARA,
    PARA_UI_Rule,

    USED,
    USED_UI_Rule
FROM (
    SELECT
        CASE
            WHEN i.insurer_name LIKE 'Allianz%' THEN 'Allianz'
            WHEN i.insurer_name LIKE 'A&G%' OR i.insurer_name LIKE 'Auto % General%' THEN 'Auto & General'
            WHEN i.insurer_name LIKE 'Capital SMART%' THEN 'Capital SMART'
            WHEN i.insurer_name LIKE 'SUNCORP%' OR i.insurer_name LIKE 'Suncorp%' THEN 'SUNCORP'
            WHEN i.insurer_name LIKE 'RACQ%' THEN 'RACQ'
            WHEN i.insurer_name LIKE 'IAG%' OR i.insurer_name LIKE 'NRMA%' THEN 'IAG/NRMA'
            WHEN i.insurer_name LIKE 'QBE%' THEN 'QBE'
            WHEN i.insurer_name LIKE 'Youi%' THEN 'Youi'
            ELSE i.insurer_name
        END AS Consolidated_Insurer,

        COUNT(DISTINCT d.repairer_id) AS Unique_Custom_Shops_Count,
        GROUP_CONCAT(DISTINCT r.repairer_name ORDER BY r.repairer_name SEPARATOR ', ') AS Custom_Shops_List,
        COUNT(DISTINCT d.quote_id) AS Quote_Volume,

        -- UI Rule Names (what the user sees in the dropdown)
        oem_mo.option_name AS OEM_UI_Rule,
        aft_mo.option_name AS AFT_UI_Rule,
        reco_mo.option_name AS RECO_UI_Rule,
        para_mo.option_name AS PARA_UI_Rule,
        used_mo.option_name AS USED_UI_Rule,

        -- Underlying price values and logic
        i.oem_list AS OEM,
        oem_pm.price_method AS OEM_PriceMethod,
        i.after_market_markup AS AFT,
        aft_pm.price_method AS AFT_PriceMethod,
        i.recycled_markup AS RECO,
        reco_pm.price_method AS RECO_PriceMethod,
        i.parallel_markup AS PARA,
        para_pm.price_method AS PARA_PriceMethod,
        i.reco_markup AS USED,
        used_pm.price_method AS USED_PriceMethod

    FROM quote_draft d
    JOIN insurer i ON d.insurer_id = i.insurer_id
    JOIN quote_item_price qip ON d.quote_id = qip.quote_id
    JOIN repairer r ON d.repairer_id = r.repairer_id

    -- Joins to get friendly UI dropdown names
    LEFT JOIN ref_markup_option oem_mo ON i.oem_selected_option_id = oem_mo.markup_option_id
    LEFT JOIN ref_markup_option aft_mo ON i.after_market_selected_option_id = aft_mo.markup_option_id
    LEFT JOIN ref_markup_option reco_mo ON i.recycled_selected_option_id = reco_mo.markup_option_id
    LEFT JOIN ref_markup_option para_mo ON i.parallel_selected_option_id = para_mo.markup_option_id
    LEFT JOIN ref_markup_option used_mo ON i.reco_selected_option_id = used_mo.markup_option_id

    -- Joins to get price-method names
    LEFT JOIN ref_price_method oem_pm ON i.oem_selected_option_id = oem_pm.price_method_id
    LEFT JOIN ref_price_method aft_pm ON i.after_market_selected_option_id = aft_pm.price_method_id
    LEFT JOIN ref_price_method reco_pm ON i.recycled_selected_option_id = reco_pm.price_method_id
    LEFT JOIN ref_price_method para_pm ON i.parallel_selected_option_id = para_pm.price_method_id
    LEFT JOIN ref_price_method used_pm ON i.reco_selected_option_id = used_pm.price_method_id

    WHERE d.quote_date >= (CURDATE() - INTERVAL 90 DAY)
      AND d.insurer_id > 1
      AND d.status_id NOT IN (1, 3)
      AND qip.is_selected = 1
    GROUP BY
        Consolidated_Insurer,
        OEM_UI_Rule, AFT_UI_Rule, RECO_UI_Rule, PARA_UI_Rule, USED_UI_Rule,
        OEM, AFT, RECO, PARA, USED
) AS final
WHERE Consolidated_Insurer IN ('Allianz', 'SUNCORP', 'IAG/NRMA', 'Auto & General', 'RACQ', 'Youi', 'Capital SMART', 'QBE')
ORDER BY Consolidated_Insurer DESC;
