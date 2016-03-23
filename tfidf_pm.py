import pdb
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import distance_metrics
from sklearn.metrics.pairwise import pairwise_distances

#from nltk import PorterStemmer
from nltk.corpus import stopwords

DATA_PATH = ('./pmc_data')
GENRE_FOLDERS = os.listdir(DATA_PATH)
ARTICLE_FILE_PATHS = []
ARTICLE_DOCUMENT_LIST = []


def load_articles():
    for genre_folder in GENRE_FOLDERS:
        genre_folder_path = os.path.join(DATA_PATH, genre_folder)
        genre_file_list = os.listdir(genre_folder_path)
        for article_file_title in genre_file_list:
            article_file_path = os.path.join(genre_folder_path, article_file_title)
            ARTICLE_FILE_PATHS.append(article_file_path)
            with open(article_file_path, 'rb') as f:
                document = f.read()
            ARTICLE_DOCUMENT_LIST.append(document)


# def open_article_files():
#     for article_file in ARTICLE_FILE_PATHS:
#         with open(article_file, 'rb') as f:
#             document = f.read()
#         ARTICLE_DOCUMENT_LIST.append((document))

load_articles()



#### TODO: process/load text from file




#### TODO: load text into TFIDF with sklearn
# STOP_WORDS = stopwords.words('english')

# vectorizer = TfidfVectorizer(stop_words=STOP_WORDS)





