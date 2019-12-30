# SSENSE Product Recommendation System

SSENSE (https://www.ssense.com/en-ca) is one of my favorite e-commerce retailer, especially during sale season so personally I have a lot of interest in their product offerings. Together with the plan to scrape data from the web and create my own dataset for machine learning projects, I decided to try scraping product data from SSENSE. 

In this 1st run, to limit the amount of runtime and to priority the exploratory data analysis and machine learning model building process, only men's products from the Canadian site were scraped. The next phase will be expanded to women's products and potentially their brand new cateogory for pets.


## Getting Started

There are several tasks involved in this project.

Firstly, data need to be scraped from the webpage of the retailer to obtain information for each product offering

Secondly, based on the extracted features of products from the web, feature engineering is performed on these features to extract essential data regarding to brands, origins, compositions, sizes, and to generate topics of the product description text.

Lastly, based on engineered features a similar product recommendation system is built to suggest other items in case a chosen product is sold out.

Another expansion is to make use of the image URLs to train a neural network to recognize products of certain designers.

### Data Scraping

The following main packages are used in the scraping process:

```
import boto3
from bs4 import BeautifulSoup
import requests
import json
from fake_useragent import UserAgent
```

The job was divided into 2 stages: 

##### 1/ Getting product URLs

This was done by looping through each category page to extract the JSON objects containing the URLs. The task is split into 4 categories and these are performed seperately under 4 AWS Lambda functions.

The URLs are stored as CSV files on AWS S3.

##### 2/ Getting product details (i.e. categories, brands, products names, prices, SKUs, descriptions, sizes, and image URLs)

After product URLs were obtained, requests were sent to access those URLs to obtain the product's detail, also in a JSON object. Because of the max runtime limit imposed on AWS Lambda (i.e. 15 mins), 23 AWS Lambda functions are called, each to scrape through approximately 1,500 product URLs.

The extracted information is stored as 23 CSV files on AWS S3, which is then combined and reformated with other Lambda functions.

### Data

At the time of scrapping, the data from the site includes original features such as:

* Number of Products: 28,992
* Categories: 88
  * Categories with most items: t-shirts
  * Categories with fewest items: waistcoats, tuxedos
* Brands: 438
  * Brands with most items: Gucci & Off-White
  * Brands with fewest items: Gosha Rubchinskiy & Éditions M.R
* Countries of Origin: 19+
* Max Price: $9,450
* Min Price: $9

