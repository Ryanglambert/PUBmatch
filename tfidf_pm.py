import pdb
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from gensim import corpora, models, similarities, matutils

DATA_PATH = ('./pmc_data/pmc_text_files/')
GENRE_FOLDERS = os.listdir(DATA_PATH)
ARTICLE_FILE_PATHS = []
ARTICLE_FILE_TITLES = []
ARTICLE_DOCUMENT_LIST = []

def load_articles():
    genre_folders_left = len(GENRE_FOLDERS)
    completed_genre_folders = 0
    for genre_folder in GENRE_FOLDERS:
        completed_genre_folders += 1
        genre_folder_path = os.path.join(DATA_PATH, genre_folder)
        genre_file_list = os.listdir(genre_folder_path)
        for article_file_title in genre_file_list:
            article_file_path = os.path.join(genre_folder_path, article_file_title)
            if os.path.isfile(article_file_path):
                ARTICLE_FILE_TITLES.append(article_file_title)
                ARTICLE_FILE_PATHS.append(article_file_path)
                with open(article_file_path, 'rb') as f:
                    document = f.read()
                    ARTICLE_DOCUMENT_LIST.append(document)

                print "done with: ", article_file_title
                print "progress: ", completed_genre_folders / float(genre_folders_left)
            else:
                sub_article_folder_list = os.listdir(article_file_path)
                for sub_article_file_title in sub_article_folder_list:
                    sub_article_file_path = os.path.join(article_file_path, 
                            sub_article_file_title)
                    ARTICLE_FILE_TITLES.append(sub_article_file_title)
                    ARTICLE_FILE_PATHS.append(sub_article_file_path)
                    with open(sub_article_file_path, 'rb') as f:
                        document = f.read()
                        ARTICLE_DOCUMENT_LIST.append(document)



def pickle_progress(progress_object, filename):
    print "{}, SUCCEEDS \n ########################".format(filename)
    with open(filename + ".pkl", 'w') as f:
        pickle.dump(progress_object, f)



load_articles()


### CountVectorize ###
count_vectorizer = CountVectorizer(stop_words='english')
count_vectorizer.fit(ARTICLE_DOCUMENT_LIST)
pubmed_vecs = count_vectorizer.transform(ARTICLE_DOCUMENT_LIST).transpose()
pickle_progress(pubmed_vecs, 'pubmed_vecs')
id2word = dict((v, k) for k, v in count_vectorizer.vocabulary_.iteritems())
pubmed_corpus = matutils.Sparse2Corpus(pubmed_vecs)


### TFIDF ###
pubmed_tfidf = models.TfidfModel(pubmed_corpus)
pickle_progress(pubmed_tfidf, 'pubmed_tfidf')
pubmed_tfidf_corpus = pubmed_tfidf[pubmed_corpus]
pickle_progress(pubmed_tfidf_corpus, 'pubmed_tfidf_corpus')


### SVD ###
lsi = models.LsiModel(pubmed_corpus, id2word=id2word, num_topics=200)
pubmed_lsi_corpus = lsi[pubmed_tfidf_corpus]
pickle_progress(pubmed_lsi_corpus, 'pubmed_lsi_corpus')







