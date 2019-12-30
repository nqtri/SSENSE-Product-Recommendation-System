import boto3
from io import StringIO
import pandas as pd
from ast import literal_eval


def combine(event, context):
  combined_df = combine_csv()
  file_name = f"all_info.csv"
  save_file_to_s3('ssense-mens-product-scrape', combined_df, file_name)

def combine_csv():
    
    df_list = []
    
    for i in range(0,4): #accessories
        df_list.append(fetch_url(f'accessories_info_{i}.csv'))
    
    for i in range(0,2): #bags
        df_list.append(fetch_url(f'bags_info_{i}.csv'))
    
    for i in range(0,13): #clothing
        df_list.append(fetch_url(f'clothing_info_{i}.csv'))
        
    for i in range(0,3): #shoe
        df_list.append(fetch_url(f'shoes_info_{i}.csv'))
    
    
    full_df = pd.concat(df_list)
    
    full_df['creation-date'] = pd.to_datetime(full_df['creation-date']).dt.date

    full_df['sub-category'] = full_df['sub-category'].apply(lambda x: x.replace('-',' '))

    full_df['origin'] = full_df['origin'].fillna('Imported')

    full_df['composition'] = full_df['composition'].astype(str)

    full_df[['full-price','sale-price','discount-percent']] = pd.DataFrame(full_df['price'].apply(lambda x: literal_eval(x)).tolist(), index=full_df.index)

    full_df['remaining-sizes'] = full_df['size'].apply(lambda x: [i[0] for i in literal_eval(x) if i[1]])

    full_df = full_df[['creation-date','sub-category','brand', 'name', 'sku', 'description',
                   'origin', 'composition', 'full-price','sale-price','discount-percent',
                   'remaining-sizes', 'image']]

    price_condition = (full_df['discount-percent'] == 0)

    full_df['sale-price'][price_condition] = full_df['full-price'][price_condition]
     
    return full_df


def fetch_url(url):
    
    client = boto3.client('s3')
    obj = client.get_object(Bucket='ssense-mens-product-scrape', Key= url) 
    body = obj['Body']
    csv_string = body.read().decode('utf-8')

    return pd.read_csv(StringIO(csv_string), sep='|',header = 0)

def save_file_to_s3(bucket, dataframe, file_name):
    # Create buffer
    csv_buffer = StringIO()
    # Write dataframe to buffer
    dataframe.to_csv(csv_buffer, sep="|", index=False)
    # Create S3 object
    s3_resource = boto3.resource("s3")
    # Write buffer to S3 object
    s3_resource.Object(bucket, file_name).put(Body=csv_buffer.getvalue())

