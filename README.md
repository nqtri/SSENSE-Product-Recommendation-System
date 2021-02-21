![Homepage](https://github.com/nqtri/SSENSE-Product-Recommendation-System/blob/master/image/homepage.png)


# SSENSE Product Recommendation System

[SSENSE](https://www.ssense.com/en-ca) is one of my favorite e-commerce retailers, especially during sale season so personally I have a lot of interest in their product offerings. Together with the plan to scrape data from the web and create my own dataset for machine learning projects, I decided to try scraping product data from SSENSE. 

In this initial run, to limit the amount of runtime and to prioritize the exploratory data analysis and machine learning model building process, only men's products from the Canadian site were scraped. The next phase will be expanded to women's products and potentially their brand new cateogory for pets.

**Final Product**: [ssense-recoengine.herokuapp.com](https://ssense-recoengine.herokuapp.com/)

## A. Motivation

With no available purchase or review data on SSENSE, only content-based recommendation engines are employed in this project. There are two use cases for a recommendation engine

* A product from SSENSE saved to the wishlist is sold out. Currently, whenever a soldout product on the wishlist is clicked on, user is either taken to the page of the same category and same designer or to the page of the product that still has other sizes left or in case sold out in all sizes, to the product page where user can put in an email notification request if it comes back in stock.

* A product from another site but user prefers to buy from SSENSE. There are other e-commerce sites that run the luxury retail business similar to SSENSE. Those include [Farfetch](https://www.farfetch.com), [END. Clothing](https://www.endclothing.com), and [Mr. Porter](https://www.mrporter.com). These sites offer products from similar designer spectrum as SSENSE but they are not based in Canada. This brings around to other potential issues with shipping, duty and tax, to return policy. For the peace of mind, many Canadian customers prefer buying the product or similar ones directly from SSENSE.

## B. Getting Started

There are several tasks involved in this project.

Firstly, data need to be scraped from the webpage of the retailer to obtain information for each product offering

Secondly, based on the extracted features of products from the web, feature engineering is performed on these features to extract essential data regarding to brands, origins, compositions, sizes, and to generate topics of the product description text.

Lastly, based on engineered features a similar product recommendation system is built to suggest other items in case a chosen product is sold out.

Another expansion is to make use of the image URLs to train a neural network to recognize products of certain designers.

### Workflow

![Project Workflow](https://github.com/nqtri/SSENSE-Product-Recommendation-System/blob/master/image/workflow.png)

## C. Data Scraping

The following main packages are used in the scraping process:

```
boto3
BeautifulSoup
requests
fake_useragent
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

## D. Feature Engineering

Some original features such as 'categories', 'brands', and 'origins' are already well classified and easy to encode using Multi-Label Binarizer. However, features containing more text such as 'names', 'description' are more complicated and need more analysis and engineering.

The following main packages are used in the feature engineering process:

```
gensim
nltk
sklearn.preprocessing
sklearn.feature_extraction.text
sklearn.decomposition
```

### Name & Description Features

Texts from 'name' and 'description' fields are combined and processed using text preprocessing techniques like lemmatization and stemming. Then, words describing colors are extracted from these texts to create another new feature for the recommendation system later.

Next, these texts are vectorized using TF-IDF (term frequency–inverse document frequency) & TF (term frequency) statistical measures in order to apply two different topic modelling techniques: Non-negative Matrix Factorization and Latent Dirichlet Allocation with limit to 50 topics.

Non-negative Matrix Factorization was chosen as the eventual topic modelling technique for this task as the topics generated under NMF generally are better generalized and it is easier to guess the general products they are referring to.

### Processed Data

After feature engineering stage, nine original features that were deemed useful for the recommendation system produces 1,069 new features that will be used to train the system.

* Sub Catogories: 116
* Brands: 397
* Text Topics: 50
* Colors: 35
* Countries of Origin: 19
* Materials: 292
* Remaining Sizes: 157

## E. Similar Product Recommendation System
The following main packages are used in the model building process:

```
sklearn.metrics.pairwise
```

In order to build a content-based recommendation engine, two methods are tested: Cosine Similarity and Euclidean Distances. I opted not to use another popular similarity measure called Jaccard Similarity for now as it looks for exact intersection of features while the model currently deals with prices, one of the most important features for the engine. $150 and $151 are pretty much the same and they lie close to each other on a vector but to under Jaccard measure, they are treated as different. 

### Cosine Similarity
Cosine similarity calculates similarity by measuring the cosine of angle between two vectors, in this case a vector containing data on the engineered features of a product.

### Euclidean Distance
Euclidean distance is similar to using a ruler to actually measure the distance between two points. There are potentially unlimted points on a plane with the same distance to an anchor point while the angle of their vectors would be very different.

### Hybrid Solution
Most recommendations from both models are pretty consistent with each other. However, since Consine Similarity looks at the angles of 2 vectors while Euclidean Distance looks at the actual distance between 2 points, I decided to employ a hybrid approach by taking the product of these two distances to yield better recommdendations for extreme cases.

## F. Web App Deployment - [ssense-recoengine.herokuapp.com](https://ssense-recoengine.herokuapp.com/)

The following main packages are used in the web app building and deployment:

```
flask
```

Web application on Heroku is built using **Flask** framework. The web app can take in either the SKU number of an existing product on SSENSE or text details of a product from other e-commerce sites and return **three** recommendations of similar products found on SSENSE. 

Details on web interface and instruction can be found under README file in the **webapp** folder.
