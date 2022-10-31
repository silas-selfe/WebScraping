USE webscraping;

/* This is the table that houses all 'for-sale' data scraped for all categories */
CREATE TABLE craigslist_forsale_US2 (
myKey INT NOT NULL AUTO_INCREMENT,
datePosted datetime NOT NULL,
neighborhood VARCHAR(120) NULL,
city VARCHAR(75) NOT NULL,
postTitle VARCHAR(100) NOT NULL,
price int NULL,
postURL VARCHAR(120) NOT NULL,
PRIMARY KEY (myKey)
);

/* This initially was used to import initial for_sale data */
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/USAForSale7.2.csv'
INTO TABLE craigslist_forsale_us
CHARACTER SET latin1
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



CREATE TABLE craigslist_forsale_categories (
myKey INT NOT NULL AUTO_INCREMENT,
datePosted datetime NOT NULL,
category VARCHAR(30) NOT NULL,
subCategory VARCHAR(60) NOT NULL,
neighborhood VARCHAR(120) NULL,
city VARCHAR(75) NOT NULL,
postTitle VARCHAR(100) NOT NULL,
price INT NULL,
postURL VARCHAR(120) NOT NULL,
PRIMARY KEY (myKey)
);


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/USAForSaleCatTest6.csv'
INTO TABLE craigslist_forsale_categories
CHARACTER SET latin1
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



CREATE TABLE us_cities (
myKey INT NOT NULL AUTO_INCREMENT,
city VARCHAR(40) NOT NULL,
stateID VARCHAR(5) NOT NULL,
stateName VARCHAR(30) NOT NULL,
countyFips INT NOT NULL,
county_name VARCHAR(50) NOT NULL,
lat FLOAT NOT NULL,
lon FLOAT NOT NULL,
population INT NOT NULL,
popDensity INT NOT NULL,
military BOOL NOT NULL,
timezone VARCHAR(60) NOT NULL,
ranking INT NOT NULL,
zips VARCHAR(60) NOT NULL,
ID INT NOT NULL,
PRIMARY KEY(myKey)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/uscities.csv'
INTO TABLE us_cities
CHARACTER SET latin1
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


