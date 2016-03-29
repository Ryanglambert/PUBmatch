import pdb 
import os
import pickle
from gensim import corpora, models, similarities, matutils, interfaces, utils
from nltk.corpus import stopwords
import numpy as np
import sys
import multiprocessing
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

pool_size = multiprocessing.cpu_count() - 3
STOP_WORDS = stopwords.words('english')
DATA_PATH = (u'./pmc_data/pmc_text_files/')
SAVE_LOCATION = './pmc_models_serialized/'
open_times = []
read_times = []
tokenize_times = []
doc2bow_times = []
add_docs_times = []

class PubmedCorpus(object):
    def __init__(self, data_folder=DATA_PATH):
        self.data_folder = data_folder
        self.dictionary = corpora.Dictionary()
        self.load_corpus()
        
    def __iter__(self):
        pool = multiprocessing.Pool(pool_size)        
        for file_chunk in utils.chunkize(self.file_path_iter(), chunksize=1000, maxsize=20):
            docs = pool.imap(tokenized_from_file, file_chunk)
            for doc_tokenized in docs:
                yield self.dictionary.doc2bow(doc_tokenized)
        pool.terminate()     

### TODO clean up redundancy    

    def load_corpus(self):
        pool = multiprocessing.Pool(pool_size)
        for file_chunk in utils.chunkize(self.file_path_iter(), chunksize=1000 , maxsize=20):
            results = pool.imap(tokenized_from_file, file_chunk)
            self.dictionary.add_documents(results, prune_at=300000)
        pool.terminate()            

    def file_path_iter(self):
        for root, dirs, files in os.walk(self.data_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                yield file_path

def tokenized_from_file(file_path):
    with open(file_path, 'rb') as f:
        doc = f.read()
        doc_token_gen = utils.tokenize(doc, lowercase=True)
        doc_tokenized = [i for i in doc_token_gen if i not in STOP_WORDS]
        return doc_tokenized

def is_dist_or_not():
    dist_input = ''
    try:
        dist_input = sys.argv[1]
    except IndexError:
        pass
    if dist_input == 'distributed':
        dist_or_not = True
    else:
        dist_or_not = False
    return dist_or_not


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
print "################# STARTING LSI MODEL ###############"

pubmed_lsi = models.LsiModel(pubmed_corpus_tfidf, 
                             id2word=pubmed_corpus.dictionary, 
                             num_topics=1000,
                             chunksize=20000,
                             distributed=True)
print "################# STARTING LSI TRANSFORMATION #############"

pubmed_corpus_lsi = pubmed_lsi[pubmed_corpus_tfidf]
pubmed_lsi.save(os.path.join(SAVE_LOCATION, 'pubmed_lsi'))

# print "average open_times", np.mean(open_times), "n = ", len(open_times)
# print "average read_times", np.mean(read_times), "n = ", len(read_times)
# print "average tokenize_times", np.mean(tokenize_times), "n = ", len(tokenize_times)
# # print "average doc2bow_times", np.mean(doc2bow_times), "n = ", len(doc2bow_times)
# print "average add_docs_times", np.mean(add_docs_times), "n = ", len(add_docs_times)

print("######### DONE!!!! ##########")
