import boto3
from io import StringIO
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup # To parse the HTML content
import requests # To fetch web content using HTTP requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from fake_useragent import UserAgent
from time import sleep

ua = UserAgent()
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
# AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
session.headers.update({'User-Agent': ua.random})

main_page = 'https://www.ssense.com'
accessories_link = ('Accessories', 'https://www.ssense.com/en-ca/men/accessories')
bags_link = ('Bags','https://www.ssense.com/en-ca/men/bags')
clothing_link = ('Clothing','https://www.ssense.com/en-ca/men/clothing')
shoes_link = ('Shoes','https://www.ssense.com/en-ca/men/shoes')

def scrape(event, context):
  data = scrape_all_url()
  split_data = split(data)
  
  for i, df in enumerate(split_data):
  
      file_name = f"clothing_url_{i}.csv"
      save_file_to_s3('ssense-mens-product-scrape', df, file_name)
  
  return {'status': 'success'}

def split(df): #Split data into managable chunks for further lambda functions to consume
    if len(df) % 1500: #1500 chunk size was achieved with trials and errors.
        chunks = (len(df) // 1500) + 1
    else:
        chunks = len(df) // 1500
    
    return np.array_split(df,chunks)

def save_file_to_s3(bucket, dataframe, file_name):
    # Create buffer
    csv_buffer = StringIO()
    # Write dataframe to buffer
    dataframe.to_csv(csv_buffer, sep="|", index=False)
    # Create S3 object
    s3_resource = boto3.resource("s3")
    # Write buffer to S3 object
    s3_resource.Object(bucket, file_name).put(Body=csv_buffer.getvalue())
    
def scrape_all_url():
    
    url_list = url_scrape(clothing_link)
        
    return pd.DataFrame(url_list, columns=['category', 'url'])

def url_scrape(category_tuple):
    cat_page = session.get(category_tuple[1])
    cat_soup = BeautifulSoup(cat_page.content, 'html.parser')
    cat_page.close()
    
     #first page
    
    try:
        last_page = int(cat_soup.find_all('li', class_='last-page')[0].get_text())
    except IndexError:
        last_page = 1
        
    result = cat_soup.find_all("script", {"type": "application/ld+json"})
    product_url_list = []
    
    for r in result:
        product_url_list.append([category_tuple[0],json.loads(r.get_text())['url']])
    
    #sub-sequent pages:
    if last_page != 1:
        
        for page in range(1,last_page):
            try:
                cat_page = session.get(category_tuple[1] + '?page=' + str(page+1))
            except requests.Timeout:
                sleep(10)
                continue
        
            cat_soup = BeautifulSoup(cat_page.content, 'html.parser')
            cat_page.close()
            result = cat_soup.find_all("script", {"type": "application/ld+json"})
        
            for r in result:
                product_url_list.append([category_tuple[0],json.loads(r.get_text())['url']])
            
    return product_url_list