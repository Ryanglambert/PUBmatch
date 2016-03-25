import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

with open('pubmed_tfidf_vectorizer.pkl', 'rb') as f:
    PUBMED_DOC_VECTORS = pickle.load(f)

with open('article_file_titles_list.pkl', 'rb') as f:
    ARTICLE_FILE_TITLES = pickle.load(f)




