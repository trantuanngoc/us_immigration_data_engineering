SELECT 
    ROW_NUMBER() OVER (ORDER BY Country) AS id,
    Country AS country,
    CountryCode as country_code
    AVG(AverageTemperature) AS average_temperature
FROM temp_table
WHERE AverageTemperature IS NOT NULL
GROUP BY Country;
