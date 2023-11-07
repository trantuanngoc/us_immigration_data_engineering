CREATE SCHEMA IF NOT EXISTS img_staging;
CREATE TABLE img_staging.country_dim (
    id INT PRIMARY KEY,
    country_name VARCHAR(255),
    country_code CHAR(2),
    average_temperature DECIMAL(5, 2)
);
CREATE TABLE img_staging.visa_dim (
    id INT PRIMARY KEY,
    visa_type VARCHAR(255),
    visa_issuer VARCHAR(255),
    visa_category_code CHAR(2),
    visa_category_name VARCHAR(255)
);
CREATE TABLE img_staging.us_port_dim (
    id INT PRIMARY KEY,
    airport_name VARCHAR(255),
    airport_type VARCHAR(255),
    iata_code CHAR(3),
    municipality VARCHAR(255),
    region VARCHAR(255),
    country VARCHAR(255),
    continent VARCHAR(255),
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    elevation_ft INT
);
CREATE TABLE img_staging.travel_mode_dim (
    id INT PRIMARY KEY,
    mode_code CHAR(2),
    airline VARCHAR(255),
    flight_number VARCHAR(255),
    mode_name VARCHAR(255)
);
CREATE TABLE img_staging.us_city_dim (
    id INT PRIMARY KEY,
    city_name VARCHAR(255),
    state_name VARCHAR(255),
    median_age DECIMAL(5, 2),
    male_population INT,
    female_population INT,
    veteran_number INT,
    foreign_born INT,
    state_code CHAR(2),
    race VARCHAR(255),
    count INT
);
CREATE TABLE img_staging.date_dim (
    id INT PRIMARY KEY,
    day INT,
    month INT,
    year INT
);
CREATE TABLE img_staging.immigration (
    id INT PRIMARY KEY,
    visa_id INT,
    us_port_id INT,
    us_city_id INT,
    country_id INT,
    travel_mode_id INT,
    application_date_id INT,
    departure_date_id INT,
    ins_number INT,
    admission_number INT,
    applicant_age INT,
    applicant_birth_year INT,
    gender VARCHAR(10),
    occupation VARCHAR(255),
    residence_country VARCHAR(255),
    arrival_state VARCHAR(255),
    status_flag_id INT
);
