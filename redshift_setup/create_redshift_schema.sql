DROP SCHEMA IF EXISTS sale_warehouse CASCADE;

CREATE SCHEMA sale_warehouse;

CREATE TABLE sale_warehouse.sale (
    sale_id VARCHAR(255) PRIMARY KEY,
    revenue DECIMAL(10, 3),
    profit DECIMAL(10, 3),
    quantity INT,
    shipping_cost DECIMAL(10, 3),

    product_id BIGINT,
    customer_id VARCHAR(255),
    shipping_zipcode INT,
    order_date DATE,
    shipment_id VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS sale_warehouse.product (
    product_id BIGINT PRIMARY KEY,
    product_name VARCHAR(255),
    sku INT,
    brand VARCHAR(255),
    category VARCHAR(255),
    product_size DECIMAL
);

CREATE TABLE IF NOT EXISTS sale_warehouse.shipment (
    shipment_id VARCHAR(255) PRIMARY KEY,
    shipping_mode VARCHAR(255),
    shipping_status VARCHAR(255),
    shipping_company VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS sale_warehouse.customer (
    customer_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    phone VARCHAR(255),
    age INT
);

CREATE TABLE IF NOT EXISTS sale_warehouse.location (
    shipping_zipcode INT PRIMARY KEY,
    city VARCHAR(45),
    state VARCHAR(45),
    country VARCHAR(45),
    shipping_address VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS sale_warehouse.time (
    date_id Date PRIMARY KEY,
    day INT,
    month INT,
    year INT
);

ALTER TABLE sale_warehouse.sale 
ADD CONSTRAINT fk_sale_product_prodID FOREIGN KEY (product_id)
REFERENCES sale_warehouse.product (product_id);

ALTER TABLE sale_warehouse.sale 
ADD CONSTRAINT fk_sale_customer_custID FOREIGN KEY (customer_id)
REFERENCES sale_warehouse.customer (customer_id);

ALTER TABLE sale_warehouse.sale 
ADD CONSTRAINT fk_sale_customer_shipmentID FOREIGN KEY (shipment_id)
REFERENCES sale_warehouse.shipment (shipment_id);

ALTER TABLE sale_warehouse.sale 
ADD CONSTRAINT fk_sale_customer_zipcode FOREIGN KEY (shipping_zipcode)
REFERENCES sale_warehouse.location (shipping_zipcode);

ALTER TABLE sale_warehouse.sale 
ADD CONSTRAINT fk_sale_customer_timeID FOREIGN KEY (order_date)
REFERENCES sale_warehouse.time (date_id);