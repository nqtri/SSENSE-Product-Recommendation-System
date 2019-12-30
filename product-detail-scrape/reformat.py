import pandas as pd
from ast import literal_eval

full_df = pd.read_csv('all_info.csv', sep = '|', header = 0)

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

