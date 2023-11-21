SELECT 
    ROW_NUMBER() OVER (ORDER BY State Code) AS id
    State_Code AS state_name,
    SUM(Total_Population) AS total_population,
    SUM(Male_Population) AS male_population,
    SUM(Female_Population) AS female_population,
    SUM(Number_of_Veterans) AS number_of_veterans,
    SUM(Foreign_born) AS foreign_born,
    AVG(Median_Age) AS median_age,
    AVG(Average_Household_Size) AS average_household_size
FROM demographic_table;