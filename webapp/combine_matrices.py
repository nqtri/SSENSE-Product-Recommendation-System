import numpy as np 

def combine_matrices(category_matrix, brand_matrix, nmf_matrix, color_matrix, origin_matrix,
              composition_matrix, size_matrix, price_matrix):
    
    return np.concatenate((category_matrix, brand_matrix, nmf_matrix, color_matrix, origin_matrix,
              composition_matrix, size_matrix,
              price_matrix),axis = 1)

if __name__ == '__main__':
    
    print("To combine all vectorized matrices")