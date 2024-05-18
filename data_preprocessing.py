import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def preprocess_text(text, custom_stop_words):
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in string.punctuation]
    tokens = [word.lower() for word in tokens]
    stop_words = set(stopwords.words('english'))
    stop_words.update(custom_stop_words)
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)
