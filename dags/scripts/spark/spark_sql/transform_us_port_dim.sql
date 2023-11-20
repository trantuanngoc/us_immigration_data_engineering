SELECT
    ident AS id,
    name AS airport_name,
    SPLIT(type, '_')[0] AS airport_type,
    iata_code,
    local_code AS municipality,
    CAST(elevation_ft AS FLOAT) AS elevation_ft,
    CAST(SPLIT(coordinates, ', ')[1] AS FLOAT) AS latitude,
    CAST(SPLIT(coordinates, ', ')[0] AS FLOAT) AS longitude
FROM airport_table;