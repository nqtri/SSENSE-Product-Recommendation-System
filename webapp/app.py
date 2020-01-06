import flask
import pickle
import pandas as pd
from get_sim_products import get_prod, get_prod_2
from vectorizer import *
from combine_matrices import combine_matrices



#product_matrix = product_matrix.drop(['sku'],axis = 1)

#product_matrix = pd.read_csv('data/ssense_rec_df.csv', sep='|', header = 0)
        
#product_df = pd.read_csv('data/all_info.csv', sep = '|', header = 0)
    
#product_df = pd.read_csv('data/product_df.csv', sep = '|', header = 0)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
    
@app.route('/sku/', methods=['GET', 'POST'])

def sku():
    if flask.request.method == 'GET':
        return(flask.render_template('sku.html'))

    if flask.request.method == 'POST':
        #Use pickle to load in the vectorized data.
        with open(f'data/ssense_rec_df.pickle', 'rb') as f:
            product_matrix = pickle.load(f)
            f.close()

        with open(f'data/product_df.pickle', 'rb') as f:
            product_df = pickle.load(f)
            f.close()
        # Extract the input
        sku_number = flask.request.form['sku']

        prod_0 = get_prod(sku_number,product_matrix,product_df,1) #top 1
        prod_1 = get_prod(sku_number,product_matrix,product_df,2) #top 2
        prod_2 = get_prod(sku_number,product_matrix,product_df,3) #top 3
        
        return flask.render_template('sku.html',original_input=
                                      {'SKU': sku_number},
                                      sku_1 = prod_0[0], 
                                      brand_1 = prod_0[1],
                                      name_1 = prod_0[2],
                                      price_1 = prod_0[3],
                                      img_1 = prod_0[4],
                                      
                                      sku_2 = prod_1[0], 
                                      brand_2 = prod_1[1],
                                      name_2 = prod_1[2],
                                      price_2 = prod_1[3],
                                      img_2 = prod_1[4],
                                      
                                      sku_3 = prod_2[0], 
                                      brand_3 = prod_2[1],
                                      name_3 = prod_2[2],
                                      price_3 = prod_2[3],
                                      img_3 = prod_2[4]
                                      )
       
@app.route('/external/', methods=['GET', 'POST'])

def external():
    if flask.request.method == 'GET':
        return(flask.render_template('external.html'))


    if flask.request.method == 'POST':
        # Extract the input
        category = flask.request.form['category']
        brand = flask.request.form['brand']
        name = flask.request.form['name']
        description = flask.request.form['description']
        color = flask.request.form['color']
        origin = flask.request.form['origin']
        composition = flask.request.form['composition']
        size = flask.request.form['size']
        full_price = flask.request.form['full_price']
        sale_price = flask.request.form['sale_price']
        
        processed_cat = process_category(category)
        processed_brand = process_brand(brand)
        processed_detail = process_detail(name,description)
        processed_color = process_color(color)
        processed_origin = process_origin(origin)
        processed_composition = process_composition(composition)
        processed_size = process_size(size)
        processed_prices = process_prices(full_price,sale_price)
        
        combined_matrix = combine_matrices(processed_cat,processed_brand,processed_detail,
                                           processed_color,processed_origin,processed_composition,
                                           processed_size,processed_prices)
    
        #Use pickle to load in the vectorized data.
        with open(f'data/ssense_rec_df.pickle', 'rb') as f:
            product_matrix = pickle.load(f)
            f.close()

        with open(f'data/product_df.pickle', 'rb') as f:
            product_df = pickle.load(f)
            f.close()
        # Extract the input

        prod_0 = get_prod_2(combined_matrix,product_matrix,product_df,1) #top 1
        prod_1 = get_prod_2(combined_matrix,product_matrix,product_df,2) #top 2
        prod_2 = get_prod_2(combined_matrix,product_matrix,product_df,3) #top 3
        
        return flask.render_template('external.html',
                                      sku_1 = prod_0[0], 
                                      brand_1 = prod_0[1],
                                      name_1 = prod_0[2],
                                      price_1 = prod_0[3],
                                      img_1 = prod_0[4],
                                      
                                      sku_2 = prod_1[0], 
                                      brand_2 = prod_1[1],
                                      name_2 = prod_1[2],
                                      price_2 = prod_1[3],
                                      img_2 = prod_1[4],
                                      
                                      sku_3 = prod_2[0], 
                                      brand_3 = prod_2[1],
                                      name_3 = prod_2[2],
                                      price_3 = prod_2[3],
                                      img_3 = prod_2[4]
                                      )
    

if __name__ == '__main__':
    app.run(debug=True)