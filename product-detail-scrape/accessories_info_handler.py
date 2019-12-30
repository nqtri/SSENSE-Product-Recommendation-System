import boto3
from io import StringIO
import json
import pandas as pd
from bs4 import BeautifulSoup # To parse the HTML content
import re
from ftfy import fix_text
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

main_page = 'https://www.ssense.com/en-ca'

#data_0 = pd.read_csv('accessories_url_1.csv',sep='|',header = 0)


def scrape0(event, context):
  data = fetch_url('accessories_url_0.csv')
  info = get_info_all(data)
  file_name = f"accessories_info_0.csv"
  save_file_to_s3('ssense-mens-product-scrape', info, file_name)
  
  return {'status': 'success'}

def scrape1(event, context):
  data = fetch_url('accessories_url_1.csv')
  info = get_info_all(data)
  file_name = f"accessories_info_1.csv"
  save_file_to_s3('ssense-mens-product-scrape', info, file_name)
  
  return {'status': 'success'}

def scrape2(event, context):
  data = fetch_url('accessories_url_2.csv')
  info = get_info_all(data)  
  file_name = f"accessories_info_2.csv"
  save_file_to_s3('ssense-mens-product-scrape', info, file_name)
  
  return {'status': 'success'}

def scrape3(event, context):
  data = fetch_url('accessories_url_3.csv')
  info = get_info_all(data)
  file_name = f"accessories_info_3.csv"
  save_file_to_s3('ssense-mens-product-scrape', info, file_name)
  
  return {'status': 'success'}

def scrape4(event, context):
  data = fetch_url('accessories_url_4.csv')
  info = get_info_all(data)
  file_name = f"accessories_info_4.csv"
  save_file_to_s3('ssense-mens-product-scrape', info, file_name)
  
  return {'status': 'success'}

def fetch_url(url):
    
    client = boto3.client('s3')
    obj = client.get_object(Bucket='ssense-mens-product-scrape', Key= url) 
    body = obj['Body']
    csv_string = body.read().decode('utf-8')

    return pd.read_csv(StringIO(csv_string), sep='|',header = 0)

def get_info_all(url_df):
    
    all_info = []
    for tuple in url_df.itertuples():
        product_url = main_page + tuple[2]

        try:
            product_info = get_info(product_url)
        except requests.Timeout:
            sleep(5)
            continue
        except requests.exceptions.ConnectionError:
            continue
        except IndexError:
            continue
        except KeyError:
            continue
        except AttributeError:
            continue
        except ValueError:            
            continue
            
        all_info.append(product_info)
    return pd.DataFrame(all_info)

def save_file_to_s3(bucket, dataframe, file_name):
    # Create buffer
    csv_buffer = StringIO()
    # Write dataframe to buffer
    dataframe.to_csv(csv_buffer, sep="|", index=False)
    # Create S3 object
    s3_resource = boto3.resource("s3")
    # Write buffer to S3 object
    s3_resource.Object(bucket, file_name).put(Body=csv_buffer.getvalue())

def get_info(product_url):
    product_page = session.get(product_url)
    product_soup = BeautifulSoup(product_page.content, 'html.parser')
    product_page.close()
    
    script = product_soup.find('script', text=re.compile('window\.INITIAL_STATE=', re.I|re.M))
    json_text = script.get_text()
    fixed_text = fix_text(json_text)
    
    data = json.loads(fixed_text[len('window.INITIAL_STATE='):])
    
    def get_size():
        test_size = []
        for i in data['products']['current']['sizes']:
            test_size.append((i['number'],i['inStock']))
        return test_size
    
    
    return {'creation-date': data['products']['current']['creationDate'],
            'sub-category': data['products']['current']['category']['seoKeyword']['en'],
            'brand': data['products']['current']['brand']['name'],
            'name': data['products']['current']['name'],
            'description': data['products']['current']['description'],
            'sku': data['products']['current']['sku'],
            'origin': data['products']['current']['countryOfOrigin'],
            'composition': data['products']['current']['composition'],
            'price': (data['products']['current']['price']['regular'],data['products']['current']['price']['sale'],data['products']['current']['price']['discount']),
            'size': get_size(),
            'image': json.loads(product_soup.find_all("script", {"type": "application/ld+json"})[0].get_text())['image'][0],
            'sale-enabled': data['context']['isSaleEnabled'],
            'sale-soon': data['context']['isSaleSoon']}