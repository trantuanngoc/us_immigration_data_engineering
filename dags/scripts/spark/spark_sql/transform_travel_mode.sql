SELECT 
    ROW_NUMBER() OVER (ORDER BY i94mode) AS id,
    i94mode AS mode_code,  
    airline,
    fltno AS flight_number,
    CASE 
        WHEN i94mode = 1 THEN 'Air'
        WHEN i94mode = 2 THEN 'Sea'
        WHEN i94mode = 3 THEN 'Land'
        ELSE 'Other'
    END AS mode_name
FROM immigration_table; 