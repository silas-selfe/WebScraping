
/* Table 2 */
SELECT city, count(postTitle), avg(price)
FROM craigslist_forsale_us
WHERE postTitle LIKE '%tool%'
AND price > 0
GROUP BY city;

/* Box Whisker Plot */
SELECT city, price
FROM craigslist_forsale_us
WHERE postTitle LIKE '%tool%'
AND price > 0;