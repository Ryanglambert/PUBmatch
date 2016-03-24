import pdb
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora, models, similarities, matutils

#from nltk import PorterStemmer
from nltk.corpus import stopwords

DATA_PATH = ('./pmc_data/pmc_text_files/')
GENRE_FOLDERS = os.listdir(DATA_PATH)
ARTICLE_FILE_PATHS = []
ARTICLE_FILE_TITLES = []
ARTICLE_DOCUMENT_LIST = []


def load_articles():
    for genre_folder in GENRE_FOLDERS:
        genre_folder_path = os.path.join(DATA_PATH, genre_folder)
        genre_file_list = os.listdir(genre_folder_path)
        for article_file_title in genre_file_list:
            ARTICLE_FILE_TITLES.append(article_file_title)
            article_file_path = os.path.join(genre_folder_path, article_file_title)
            ARTICLE_FILE_PATHS.append(article_file_path)
            with open(article_file_path, 'rb') as f:
                document = f.read()
                ARTICLE_DOCUMENT_LIST.append(document)


load_articles()

# print "ARTICLE_DOCUMENT_LIST length: ", len(ARTICLE_DOCUMENT_LIST)
# print "ARTICLE_FILE_TITLES length: ", len(ARTICLE_FILE_TITLES)

#### TODO: load text into TFIDF with sklearn
STOP_WORDS = stopwords.words('english')

vectorizer = TfidfVectorizer(stop_words=STOP_WORDS)

pubmed_vectors = vectorizer.fit_transform(ARTICLE_DOCUMENT_LIST)

with open('pubmed_tfidf.pkl', 'w') as f:
    pickle.dump(pubmed_vectors, f)

print ARTICLE_DOCUMENT_LIST[0], ['\n'] * 10
print ARTICLE_DOCUMENT_LIST[3]


