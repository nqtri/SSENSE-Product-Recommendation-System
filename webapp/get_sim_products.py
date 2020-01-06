import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_distances
from sklearn.metrics.pairwise import euclidean_distances

def get_prod(sku_number, product_matrix,product_df, rank):
        
    index = product_df[product_df.sku == sku_number].index[0]
    dist1 = cosine_distances([product_matrix.iloc[index]],product_matrix)[:20]
    
    dist2 = euclidean_distances([product_matrix.iloc[index]],product_matrix)[:20]                                                                                                              
    dist = dist1*dist2
    
    top_i = list(np.argsort(dist)[0])[rank]

    #return product_df['sku'][top_i], product_df['brand'][top_i], product_df['name'][top_i], product_df['image'][top_i], product_df['sale-price'][top_i]
    return product_df.iloc[top_i]


def get_prod_2(new_matrix, product_matrix,product_df, rank):
    
    dist1 = cosine_distances(new_matrix,product_matrix)[:20]
    
    dist2 = euclidean_distances(new_matrix,product_matrix)[:20]                                                                                                              
    dist = dist1*dist2
            
    top_i = list(np.argsort(dist)[0])[rank+1]
    
    return product_df.iloc[top_i]

if __name__ == '__main__':
    
    #product_matrix = pd.read_csv('C:/Users/tring/Desktop/Projects/SSENSE Project/feature engineering/ssense_rec_df.csv', 
                         #sep='|', header = 0, dtype = {"sku" : "str", "full_price": "float64", "sale_price": "float64"} )
        
    #product_df = pd.read_csv('data/all_info.csv', sep = '|', header = 0)
    
    #product_df = pd.read_csv('data/all_info.csv', sep = '|', header = 0)
    
    import pickle

    with open(f'data/ssense_rec_df.pickle', 'rb') as f:
        product_matrix = pickle.load(f)
        f.close()

    with open(f'data/product_df.pickle', 'rb') as f:
        product_df = pickle.load(f)
        f.close()
    
    
    print(get_prod("192264M237035",product_matrix,product_df,3))
    