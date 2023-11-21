SELECT 
    TO_DATE(date) AS id,
    DAY(TO_DATE(date)) AS day,
    MONTH(TO_DATE(date)) AS month,
    YEAR(TO_DATE(date)) AS year,
    WEEKOFYEAR(TO_DATE(date)) AS week,
    DAYOFWEEK(TO_DATE(date)) AS weekday
FROM immigration_table;