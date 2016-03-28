import pdb 
import os
import pickle
from gensim import corpora, models, similarities, matutils, interfaces, utils
from nltk import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import numpy as np

STOP_WORDS = stopwords.words('english')


DATA_PATH = (u'./pmc_data/pmc_text_files/')
SAVE_LOCATION = './pmc_models_serialized/'
GENRE_FOLDERS = os.listdir(DATA_PATH)
ARTICLE_FILE_PATHS = []
ARTICLE_FILE_TITLES = []
ARTICLE_DOCUMENT_LIST = []

class PubmedCorpus(object):
    def __init__(self, data_folder=DATA_PATH):
        self.data_folder = data_folder
        self.dictionary = corpora.Dictionary()
        self.load_corpus()
        
    def __iter__(self):
        for root, dirs, files in os.walk(self.data_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'rb') as f:
                    doc = f.read()
                    doc_token_gen = utils.tokenize(doc, 
                                                  lowercase=True)
                    doc_tokenized = [i for i in doc_token_gen]
                    yield self.dictionary.doc2bow(doc_tokenized)
### TODO clean up redundancy    
    def load_corpus(self):
        for root, dirs, files in os.walk(self.data_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'rb') as f:
                    doc = f.read()
                    doc_token_gen = utils.tokenize(doc, 
                                                  lowercase=True)
                    doc_tokenized = [i for i in doc_token_gen]
                    self.dictionary.add_documents([doc_tokenized])


def to_unicode_or_bust(
        obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj
              
pubmed_corpus = PubmedCorpus()

pubmed_tfidf = models.TfidfModel(pubmed_corpus, normalize=True)
pubmed_tfidf.save(os.path.join(SAVE_LOCATION, 'pubmed_tfidf'))

pubmed_corpus_tfidf = pubmed_tfidf[pubmed_corpus]
pubmed_corpus_tfidf.save(os.path.join(SAVE_LOCATION, 'pubmed_corpus_tfidf'))

pubmed_lsi = models.LsiModel(pubmed_corpus_tfidf, 
                             id2word=pubmed_corpus.dictionary, 
                             num_topics=300)

pubmed_corpus_lsi = pubmed_lsi[pubmed_corpus_tfidf]
pubmed_lsi.save(os.path.join(SAVE_LOCATION, 'pubmed_lsi'))

pubmed_lsi.print_topics(2)

print("######### DONE!!!! ##########")
