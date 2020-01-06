import pickle
from preprocess_text import preprocess, preprocess_composition
import pandas as pd
import numpy as np


feature_dir = "models/"

def process_category(text):
    
    with open(f'models/category_binarizer.pickle','rb') as f:
        category_mlb = pickle.load(f)
        f.close()
    
    processed_category = pd.Series(text).map(preprocess).str.split(" ")
    
    return category_mlb.transform(processed_category)


def process_brand(text):
    
    with open(f'models/brand_binarizer.pickle','rb') as f:
        brand_mlb = pickle.load(f)
        f.close()
    
    processed_brand = pd.Series(text).str.lower().str.split(",")
    
    return brand_mlb.transform(processed_brand)

def process_detail(name_text, description_text):
    
    with open(f'models/tfidf_vectorizer.pickle','rb') as f:
        tfidf_vectorizer_model = pickle.load(f)
        f.close()
    
    with open(f'models/nmf_model.pickle','rb') as f:
        nmf_model = pickle.load(f)
        f.close()
        
    processed_detail = pd.Series(preprocess(name_text+description_text))
    return nmf_model.transform(tfidf_vectorizer_model.transform(processed_detail))

def process_color(text):
    with open(f'models/color_binarizer.pickle','rb') as f:
        color_mlb = pickle.load(f)
        f.close()

    processed_color = pd.Series(text.replace(" ", "").lower()).str.split(",")
    return color_mlb.transform(processed_color)

def process_origin(text):
    with open(f'models/origin_binarizer.pickle','rb') as f:
        origin_mlb = pickle.load(f)
        f.close()
    
    processed_origin = pd.Series(text.lower()).str.split(",")
    return origin_mlb.transform(processed_origin)


def process_composition(text):
    with open(f'models/composition_binarizer.pickle','rb') as f:
        composition_mlb = pickle.load(f)
        f.close()
        
    processed_composition = pd.Series(preprocess_composition(text)).str.split()
    return composition_mlb.transform(processed_composition)


def process_size(size_text):
    
    with open(f'models/size_binarizer.pickle','rb') as f:
        size_mlb = pickle.load(f)
        f.close()
            
    processed_sizes = pd.Series(size_text.replace(" ", "").upper()).str.split(",")
    return size_mlb.transform(processed_sizes)

def process_prices(full_price, sale_price):
    with open(f'models/price_scaler.pickle','rb') as f:
        price_scaler = pickle.load(f)
        f.close()
    
    processed_prices = np.array([[full_price,sale_price]]).astype(float)
    return price_scaler.transform(processed_prices)


if __name__ == '__main__':
    
    name_sample = "Loopback Cotton-Jersey Zip-Up Hoodie"

    description_sample = '''
    Whether you're a bit of a collector or new to the look, 
    Reigning Champ offers a range of hoodies that are stylish, 
    comfortable and well-crafted, like this zip-up style. It is 
    made from cosy loopback cotton-jersey and finished with 
    bartack stitches to reinforce areas prone to wear. It's 
    ideally suited to days spent at home channel-surfing or when 
    it's your turn to head out for coffee and the weekend papers
    
    Black loopback cotton-jersey
    Drawstring hood, raglan sleeves, front pouch pockets, designer emblem, 
    ribbed side panels and trims, flatlock seams
    Two-way zip fastening
    '''
    
    print(process_category("zip hoodies"))
    print(process_brand('Gucci'))
    print(process_detail(name_sample,description_sample))
    print(process_color('black, blue'))
    print(process_origin('italy'))
    print(process_composition("100% cotton, metal"))
    print(process_size('S, M, XL'))
    print(process_prices(170,120))



