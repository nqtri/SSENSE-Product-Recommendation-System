import re
import gensim
from nltk.stem import WordNetLemmatizer, SnowballStemmer


def lemmatize_stemming(text):
    stemmer = SnowballStemmer("english")
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    text= re.sub("(\r|\n|-|&|approx|supplier|length|height)+"," ",text,flags=re.IGNORECASE) 
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 2:
            result.append(lemmatize_stemming(token))
    return " ".join(result)


def preprocess_composition(text):
    text= re.sub("(Upper|Sole|Body|Trim|Lining|Fill|American|Outer|fabric)"," ",text,flags=re.IGNORECASE) 
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 2:
            result.append(lemmatize_stemming(token))
    return " ".join(result)


if __name__ == '__main__':
    
    sample_text = '''
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
    
    print(preprocess(sample_text))
    print(preprocess_composition("100% cotton, metal"))
    