/* All Goods and Prices */
SELECT postTitle, price
FROM craigslist_forsale_us;

/* 
	-- Search Term -- 
	Way too specific -- will not use this
*/
SELECT * 
FROM craigslist_forsale_us
WHERE postTitle LIKE 'dishwasher';

/* Search Term 2 */
SELECT * 
FROM craigslist_forsale_us
WHERE postTitle LIKE '% duck%';

SELECT * 
FROM craigslist_forsale_us
WHERE postTitle LIKE '% tool%' 
	AND price > 0;
    
SELECT * 
FROM craigslist_forsale_us
WHERE postTitle LIKE '% tool%' 
	AND price > 0
    AND price <= 10000;

SELECT * 
FROM craigslist_forsale_us
WHERE postTitle LIKE '% tool%' 
	AND price > 0
    AND price <= 10000
    AND city = 'cincinnati';

SELECT * 
FROM craigslist_forsale_us
WHERE postTitle LIKE '%guitar%' 
	AND price > 0
    AND city LIKE 'cincinnati';
    
SELECT * 
FROM craigslist_forsale_us
WHERE city = 'cincinnati'
AND neighborhood = 'burlington';

SELECT MAX(myKey) 
FROM craigslist_forsale_us;

SELECT MAX(myKey) 
FROM craigslist_forsale_categories;

SELECT price, count(price)
FROM craigslist_forsale_us
WHERE postTitle LIKE '%dresser%'
AND price > 0
GROUP BY price;

SELECT MAX(myKey) 
FROM craigslist_forsale_categories;

SELECT * FROM craigslist_forsale_us	
WHERE myKey > 112120;


SELECT DISTINCT city FROM craigslist_forsale_us;

SELECT * FROM webscraping.craigslist_forsale_us;

SET @@global.sql_mode= 'NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

SELECT *
FROM craigslist_forsale_us
WHERE postTitle LIKE '%tool%' 
	AND price > 0;

    
SELECT COUNT(myKey)
FROM craigslist_forsale_us
WHERE postTitle LIKE '%tool%' 
	AND price > 0
    AND city = 'altoona';

SELECT COUNT(myKey)
FROM craigslist_forsale_us
WHERE postTitle LIKE '% tool%'
AND price > 0;


SELECT * 
FROM craigslist_forsale_categories
WHERE subCategory LIKE '%tool%' 
AND postTitle LIKE '%tool%'
AND city LIKE 'houston';