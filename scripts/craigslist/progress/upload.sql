USE webscraping;
SELECT * FROM crglst_forsale_us; 

LOAD DATA INFILE '/Documents/ZenithAnalytica/Industries/WebScraping/data/USAForSale5.csv'
	INTO TABLE crglst_forsale_us
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;