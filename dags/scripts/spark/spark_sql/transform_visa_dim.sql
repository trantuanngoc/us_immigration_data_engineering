SELECT 
    ROW_NUMBER() OVER (ORDER BY visatype) AS id
    visatype AS visa_type,
    visapost AS visa_issuer,
    i94visa AS visa_category_code  
FROM immigration_table;
