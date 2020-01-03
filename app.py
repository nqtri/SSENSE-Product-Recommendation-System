import flask
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_distances


# Use pickle to load in the pre-trained model.
with open(f'feature engineering/ssense_rec_df.pickle', 'rb') as f:
    product_matrix = pickle.load(f)
    
product_df = pd.read_csv('C:/Users/tring/Desktop/SSENSE Project/eda/all_info.csv', sep = '|', header = 0)   
    
product_matrix = product_matrix.drop(['sku'],axis = 1)

def get_similar_product(sku_number, product_matrix):
    
    index = product_df[product_df.sku == sku_number].index[0]
    dist = cosine_distances(np.array([product_matrix.iloc[index]]),
                                np.array(product_matrix[~product_matrix.index.isin([index])]))

    top_i = list(np.argsort(dist)[0])[0]
    
    if top_i < index:
        top_i = top_i
    else:
        top_i = top_i +1 

    return product_df['sku'][top_i], product_df['brand'][top_i], product_df['name'][top_i]


# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        sku_number = flask.request.form['sku']

        rec_sku, rec_brand, rec_name = get_similar_product(sku_number,product_matrix)
        
        return flask.render_template('index.html',original_input=
                                      {'SKU': sku_number},
                                      sku_1 = rec_sku, 
                                      brand_1 = rec_brand,
                                      name_1 = rec_name)
        
if __name__ == '__main__':
    app.run()