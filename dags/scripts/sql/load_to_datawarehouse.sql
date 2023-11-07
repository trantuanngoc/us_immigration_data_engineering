INSERT INTO immigration_dwh.country_dim (
    id,
    country_name,
    country_code,
    average_temperature)
SELECT 
    id,
    country_name,
    country_code,
    average_temperature
FROM img_staging.country_dim;

INSERT INTO immigration_dwh.visa_dim (
    id,
    visa_type,
    visa_issuer,
    visa_category_code,
    visa_category_name)
SELECT
    id,
    visa_type,
    visa_issuer,
    visa_category_code,
    visa_category_name
FROM img_staging.visa_dim;

INSERT INTO immigration_dwh.us_port_dim (
    id,
    airport_name,
    airport_type,
    iata_code,
    municipality,
    region,
    country,
    continent,
    latitude,
    longitude,
    elevation_ft)
SELECT
    id,
    airport_name,
    airport_type,
    iata_code,
    municipality,
    region,
    country,
    continent,
    latitude,
    longitude,
    elevation_ft
FROM img_staging.us_port_dim;

INSERT INTO immigration_dwh.travel_mode_dim (
    id,
    mode_code,
    airline,
    flight_number,
    mode_name)
SELECT
   id,
    mode_code,
    airline,
    flight_number,
    mode_name
FROM img_staging.travel_mode_dim;

INSERT INTO immigration_dwh.us_city_dim (
    id,
    city_name,
    state_name,
    median_age,
    male_population,
    female_population,
    veteran_number,
    foreign_born,
    state_code,
    race,
    count)
SELECT
    id,
    city_name,
    state_name,
    median_age,
    male_population,
    female_population,
    veteran_number,
    foreign_born,
    state_code,
    race,
    count
FROM img_staging.us_city_dim;

INSERT INTO immigration_dwh.date_dim (
    id,
    day,
    month,
    year)
SELECT
   id,
    day,
    month,
    year
FROM img_staging.date_dim;

INSERT INTO immigration_dwh.immigration (
    id,
    visa_id,
    us_port_id,
    us_city_id,
    country_id,
    travel_mode_id,
    application_date_id,
    departure_date_id,
    ins_number,
    admission_number,
    applicant_age,
    applicant_birth_year,
    gender,
    occupation,
    residence_country,
    arrival_state,
    status_flag_id)
SELECT
   id,
    visa_id,
    us_port_id,
    us_city_id,
    country_id,
    travel_mode_id,
    application_date_id,
    departure_date_id,
    ins_number,
    admission_number,
    applicant_age,
    applicant_birth_year,
    gender,
    occupation,
    residence_country,
    arrival_state,
    status_flag_id
FROM img_staging.immigration;



