SELECT 
    ROW_NUMBER() OVER (ORDER BY `State Code`) AS id
    `State Code` AS state_name,
    SUM(`Total Population`) AS total_population,
    SUM(`Male Population`) AS male_population,
    SUM(`Female Population`) AS female_population,
    SUM(`Number of Veterans`) AS number_of_veterans,
    SUM(`Foreign-born`) AS foreign_born,
    AVG(`Median Age`) AS median_age,
    AVG(`Average Household Size`) AS average_household_size
FROM demographic_table;