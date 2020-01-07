import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_distances
from sklearn.metrics.pairwise import euclidean_distances

def get_prod(sku_number, product_matrix,product_sku, product_brand, product_name,
             product_price,product_img, rank):
    
    try:    
        index = np.where(product_sku==sku_number)
    
        dist1 = cosine_distances(product_matrix.iloc[index],product_matrix)[:20]
    
        dist2 = euclidean_distances(product_matrix.iloc[index],product_matrix)[:20]                                                                                                              
        dist = dist1*dist2
    
        top_i = list(np.argsort(dist)[0])[rank]
    
        return (product_sku[top_i],product_brand[top_i], product_name[top_i], 
                product_price[top_i], product_img[top_i])

    except ValueError:
        return ('No SKU Found','No SKU Found','No SKU Found',
                'No SKU Found','No SKU Found')
    


    #return product_df['sku'][top_i], product_df['brand'][top_i], product_df['name'][top_i], product_df['image'][top_i], product_df['sale-price'][top_i]


def get_prod_2(new_matrix, product_matrix,product_sku,product_brand, product_name,
             product_price,product_img, rank):
    
    dist1 = cosine_distances(new_matrix,product_matrix)[:20]
    
    dist2 = euclidean_distances(new_matrix,product_matrix)[:20]                                                                                                              
    dist = dist1*dist2
            
    top_i = list(np.argsort(dist)[0])[rank-1]
    
    return (product_sku[top_i],product_brand[top_i], product_name[top_i], 
                product_price[top_i], product_img[top_i])

if __name__ == '__main__':
    
    #product_matrix = pd.read_csv('C:/Users/tring/Desktop/Projects/SSENSE Project/feature engineering/ssense_rec_df.csv', 
                         #sep='|', header = 0, dtype = {"sku" : "str", "full_price": "float64", "sale_price": "float64"} )
        
    #product_df = pd.read_csv('data/all_info.csv', sep = '|', header = 0)
    
    #product_df = pd.read_csv('data/all_info.csv', sep = '|', header = 0)
    
    import pickle

    with open(f'data/ssense_rec_df.pickle', 'rb') as f:
        product_matrix = pickle.load(f)
        f.close()

    with open(f'data/product_sku.pickle', 'rb') as f:
        product_sku = pickle.load(f)
        f.close()
    with open(f'data/product_brand.pickle', 'rb') as f:
        product_brand = pickle.load(f)
        f.close()    
    with open(f'data/product_name.pickle', 'rb') as f:
        product_name = pickle.load(f)
        f.close()    
    with open(f'data/product_price.pickle', 'rb') as f:
        product_price = pickle.load(f)
        f.close()    
    with open(f'data/product_img.pickle', 'rb') as f:
        product_img = pickle.load(f)
        f.close()   
    
    
    print(get_prod("192168M237016",product_matrix,product_sku, product_brand, product_name,
             product_price,product_img,3))
    