# WebScraping


This repo pulls 'for sale' posts from various cities across the United States and stores this data in a local MySql database. 
This database is integrated into a GUI allowing for users to enter a search term and select a city for comparison. 

To scrape the data and store into a local DB, go to scripts -> craigslist -> craigslist_for_sale_USAX (where X is whatever number posted)
To run the GUI, go to the same file location and run -> craigslist_GUIX

An image of the GUI can be found in the output folder. 



My machine requires that data is in the Output folder for it to be uploaded to MySQL, so ensure this is appropriate on your device. 



Future work will be to create a Text Classification Model, so generalized posts pulled from 'craigslist_for_saleUSAX' can be categorized.
Data has been scraped for each city, from each category page. This data will be used to train and evaluate the model before it's deployed on all incoming new data.  
